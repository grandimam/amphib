import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich import box

from core import KarakHire
from core.config import settings

from core.parsers import PDFParser
from core.prompt import JinjaPromptProvider
from core.prompt import PromptTemplate
from core.providers.chat import OpenRouterProvider

console = Console()


def _score_bar(score: float, maximum: int, width: int = 12) -> str:
    filled = round((score / maximum) * width) if maximum > 0 else 0
    filled = min(filled, width)
    bar = "█" * filled + "░" * (width - filled)
    pct = (score / maximum) * 100 if maximum > 0 else 0
    return f"{bar} {score:.0f}/{maximum} ({pct:.0f}%)"


def _score_color(score: float, maximum: int) -> str:
    pct = (score / maximum) * 100 if maximum > 0 else 0
    if pct >= 75:
        return "green"
    if pct >= 50:
        return "yellow"
    return "red"


def _as_dict(val, default=None):
    if isinstance(val, dict):
        return val
    return default if default is not None else {}


def _as_list(val):
    if isinstance(val, list):
        return val
    return []


def evaluate(file_path: str):
    with console.status("[bold green]Parsing PDF..."):
        runner = KarakHire(
            parser=PDFParser(),
            model_provider=OpenRouterProvider(settings.openrouter_api_key),
            prompt_provider=JinjaPromptProvider(),
        )
    with console.status("[bold green]Evaluating resume..."):
        prompt = PromptTemplate.EVALUATE.value
        response = runner.run(file_path=file_path, prompt_name=prompt)

    # Strip markdown code fences if present
    cleaned = response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1] if "\n" in cleaned else cleaned[3:]
        cleaned = cleaned.rsplit("```", 1)[0].strip()

    try:
        data = json.loads(cleaned)
    except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
        msg = "[yellow]Could not parse data. Showing raw response:[/]"
        console.print(msg)
        console.print(Syntax(response, "json", word_wrap=True))
        return

    scores = _as_dict(data.get("scores"))
    bonus = _as_dict(data.get("bonus_points"))
    deductions = _as_dict(data.get("deductions"))
    strengths = _as_list(data.get("key_strengths"))
    improvements = _as_list(data.get("areas_for_improvement"))
    candidate = data.get("candidate_name", "")

    # Diagnostic: if scores are all zero, show raw response
    total_score = sum(
        _as_dict(scores.get(k)).get("score", 0)
        for k in ("open_source", "self_projects", "production", "technical_skills")
    )
    if total_score == 0:
        console.print("[yellow]Scores are all zero. Raw LLM response:[/]")
        console.print(Syntax(response, "json", word_wrap=True))
        return

    header = "Resume Evaluation"
    if candidate:
        header += f" — [bold]{candidate}[/]"
    console.print(Panel(header, border_style="cyan"))

    st = Table(box=box.ROUNDED, title="Category Scores")
    st.add_column("Category", style="cyan")
    st.add_column("Score", justify="center")
    st.add_column("Bar", justify="left")
    st.add_column("Evidence")

    cat_labels = {
        "open_source": "Open Source",
        "self_projects": "Self Projects",
        "production": "Production",
        "technical_skills": "Technical Skills",
    }

    total_max = 0

    for key, label in cat_labels.items():
        cat = _as_dict(scores.get(key))
        s = cat.get("score", 0)
        m = cat.get("max", 0)
        evidence = cat.get("evidence", "")
        total_score += s
        total_max += m
        color = _score_color(s, m)
        bar = _score_bar(s, m)
        st.add_row(label, f"[{color}]{s:.0f}/{m}[/{color}]", bar, evidence)

    st.add_section()
    st.add_row(
        "[bold]Total[/]",
        f"[bold]{total_score:.0f}/{total_max:.0f}[/bold]",
        "",
        "",
    )

    bonus_total = bonus.get("total", 0)
    deduction_total = deductions.get("total", 0)
    final_score = total_score + bonus_total - deduction_total
    st.add_row(
        "",
        f"Bonus: +{bonus_total:.0f}  Deductions: -{deduction_total:.0f}",
        "",
        f"[bold]Final: {final_score:.0f}/120[/bold]",
    )

    console.print(st)

    if bonus_total:
        console.print(
            Panel(
                bonus.get("breakdown", ""),
                title=f"Bonus Points (+{bonus_total})",
                border_style="green",
            )
        )

    if deduction_total:
        console.print(
            Panel(
                deductions.get("reasons", ""),
                title=f"Deductions (-{deduction_total})",
                border_style="red",
            )
        )

    if strengths:
        text = "\n".join(f"• {s}" for s in strengths)
        console.print(Panel(text, title="Key Strengths", border_style="green"))
    if improvements:
        text = "\n".join(f"• {s}" for s in improvements)
        console.print(Panel(text, title="Areas for Improvement", border_style="yellow"))
