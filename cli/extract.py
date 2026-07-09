import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.tree import Tree

from core import Amphib
from core.config import settings

from core.parsers import PDFParser
from core.prompt import JinjaPromptProvider
from core.prompt import PromptTemplate
from core.providers.chat import OpenRouterProvider

console = Console()


def _render_basics(basics: dict):
    name = basics.get("name", "Unknown")
    email = basics.get("email", "")
    phone = basics.get("phone", "")
    url = basics.get("url", "")
    summary = basics.get("summary", "")
    loc = basics.get("location")
    loc = _as_dict(loc)
    city = loc.get("city", "")
    country = loc.get("countryCode", "")

    parts = [f"[bold]{name}[/]"]
    if email:
        parts.append(f"[cyan]{email}[/]")
    if phone:
        parts.append(f"[cyan]{phone}[/]")
    if url:
        parts.append(f"[link={url}]{url}[/link]")
    if city:
        parts.append(f"{city}, {country}" if country else city)

    info = "\n".join(parts)
    console.print(Panel(info, title="Candidate", border_style="cyan"))

    if summary:
        console.print(Panel(str(summary), title="Summary", border_style="dim"))

    profiles = _as_list(basics.get("profiles"))
    if profiles:
        t = Table(title="Profiles")
        t.add_column("Network", style="cyan")
        t.add_column("Username")
        t.add_column("URL")
        for p in profiles:
            p = _as_dict(p)
            t.add_row(p.get("network", ""), p.get("username", ""), p.get("url", ""))
        console.print(t)


def _as_dict(val):
    return val if isinstance(val, dict) else {}


def _render_work(entries: list):
    if not entries:
        return
    tree = Tree(f"[bold]Work Experience[/] ({len(entries)})")
    for w in entries:
        w = _as_dict(w)
        name = w.get("name", "")
        position = w.get("position", "")
        start = w.get("startDate", "")
        end = w.get("endDate", "")
        summary = w.get("summary", "")
        highlights = _as_list(w.get("highlights"))

        label = f"[cyan]{position}[/] @ [bold]{name}[/]"
        if start or end:
            label += f"  [dim]{start} – {end}[/dim]"
        branch = tree.add(label)
        if summary:
            branch.add(str(summary))
        for h in highlights:
            branch.add(f"• {h}")
    console.print(tree)


def _render_education(entries: list):
    if not entries:
        return
    table = Table(title=f"Education ({len(entries)})")
    table.add_column("Institution", style="cyan")
    table.add_column("Degree")
    table.add_column("Field")
    table.add_column("Dates")
    table.add_column("Score")
    for e in entries:
        e = _as_dict(e)
        table.add_row(
            e.get("institution", ""),
            e.get("studyType", ""),
            e.get("area", ""),
            f"{e.get('startDate', '') or ''} – {e.get('endDate', '') or ''}",
            e.get("score", ""),
        )
    console.print(table)


def _render_skills(entries: list):
    if not entries:
        return
    table = Table(title=f"Skills ({len(entries)} categories)")
    table.add_column("Category", style="cyan")
    table.add_column("Skills")
    for s in entries:
        s = _as_dict(s)
        keywords = s.get("keywords", [])
        table.add_row(s.get("name", ""), ", ".join(keywords) if keywords else "")
    console.print(table)


def _render_projects(entries: list):
    if not entries:
        return
    tree = Tree(f"[bold]Projects[/] ({len(entries)})")
    for p in entries:
        p = _as_dict(p)
        name = p.get("name", "")
        desc = p.get("description", "")
        techs = _as_list(p.get("technologies"))
        url = p.get("url", "")

        label = f"[cyan]{name}[/]"
        if url:
            label += f"  [dim link={url}]{url}[/dim]"
        branch = tree.add(label)
        if desc:
            branch.add(str(desc))
        if techs:
            branch.add(f"[dim]Tech:[/] {', '.join(techs)}")
    console.print(tree)


def _render_awards(entries: list):
    if not entries:
        return
    table = Table(title=f"Awards ({len(entries)})")
    table.add_column("Title", style="cyan")
    table.add_column("Awarder")
    table.add_column("Date")
    for a in entries:
        a = _as_dict(a)
        table.add_row(a.get("title", ""), a.get("awarder", ""), a.get("date", ""))
    console.print(table)


def _as_list(val):
    return val if isinstance(val, list) else []


def extract(file_path: str):
    with console.status("[bold green]Parsing PDF..."):
        runner = Amphib(
            parser=PDFParser(),
            model_provider=OpenRouterProvider(settings.openrouter_api_key),
            prompt_provider=JinjaPromptProvider(),
        )
    with console.status("[bold green]Extracting resume data..."):
        prompt = PromptTemplate.EXTRACT.value
        response = runner.run(file_path=file_path, prompt_name=prompt)

    cleaned = response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1] if "\n" in cleaned else cleaned[3:]
        cleaned = cleaned.rsplit("```", 1)[0].strip()

    try:
        data = json.loads(cleaned)
        basics = data.get("basics")
        if isinstance(basics, dict):
            _render_basics(basics)
        _render_work(_as_list(data.get("work")))
        _render_education(_as_list(data.get("education")))
        _render_skills(_as_list(data.get("skills")))
        _render_projects(_as_list(data.get("projects")))
        _render_awards(_as_list(data.get("awards")))
    except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
        msg = "[yellow]Could not parse data. Showing raw response:[/]"
        console.print(msg)
        console.print(Syntax(response, "json", word_wrap=True))
