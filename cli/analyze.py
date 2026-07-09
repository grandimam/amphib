import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.tree import Tree

from core import Amphib

from core.parsers import PDFParser
from core.prompt import JinjaPromptProvider
from core.prompt import PromptTemplate
from core.providers.chat import OpenRouterProvider

from core.config import settings

console = Console()


def _as_dict(val):
    return val if isinstance(val, dict) else {}


def _as_list(val):
    return val if isinstance(val, list) else []


def _render_layout(data: dict):
    layout = data.get("overall_layout", "unknown").replace("_", " ").title()
    method = data.get("detection_method", "")
    confidence = data.get("confidence", "")

    meta = (
        f"[bold]Layout:[/] {layout}\n"
        f"[bold]Method:[/] {method}\n"
        f"[bold]Confidence:[/] {confidence}"
    )
    console.print(Panel(meta, title="Layout Analysis", border_style="cyan"))

    subs = _as_list(data.get("subsections_with_columns"))
    if subs:
        table = Table(title="Subsections with Columns")
        table.add_column("Subsection", style="cyan")
        table.add_column("Columns", justify="right")
        table.add_column("Items")
        table.add_column("Evidence")
        for s in subs:
            s = _as_dict(s)
            table.add_row(
                s.get("subsection_name", ""),
                str(s.get("column_count", "")),
                ", ".join(_as_list(s.get("items"))),
                s.get("evidence", ""),
            )
        console.print(table)

    order = _as_list(data.get("section_order"))
    if order:
        tree = Tree("[bold]Section Order[/]")
        for s in order:
            tree.add(str(s))
        console.print(tree)

    boundaries = _as_list(data.get("column_boundaries"))
    if boundaries:
        bt = Table(title="Column Boundaries")
        bt.add_column("Col #", justify="right")
        bt.add_column("Start Position")
        bt.add_column("Content Summary")
        for b in boundaries:
            b = _as_dict(b)
            bt.add_row(
                str(b.get("column_index", "")),
                b.get("start_position", ""),
                b.get("content_summary", ""),
            )
        console.print(bt)


def analyze(file_path: str):
    with console.status("[bold green]Parsing PDF..."):
        runner = Amphib(
            parser=PDFParser(),
            model_provider=OpenRouterProvider(settings.openrouter_api_key),
            prompt_provider=JinjaPromptProvider(),
        )
    with console.status("[bold green]Analyzing layout..."):
        prompt = PromptTemplate.LAYOUT.value
        response = runner.run(file_path=file_path, prompt_name=prompt)

    cleaned = response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1] if "\n" in cleaned else cleaned[3:]
        cleaned = cleaned.rsplit("```", 1)[0].strip()

    try:
        data = json.loads(cleaned)
        _render_layout(data)
    except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
        msg = "[yellow]Could not parse layout data. Showing raw response:[/]"
        console.print(msg)
        console.print(Syntax(response, "json", word_wrap=True))
