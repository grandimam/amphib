#!/usr/bin/env python3
"""Render Jinja templates to HTML for GitHub Pages."""

import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

HERE = Path(__file__).parent
TEMPLATES = HERE / "templates"
OUTPUT = HERE
CSS_SRC = HERE / "assets" / "css"
CSS_DST = HERE / "assets" / "css"

PAGES = [
    ("index.jinja", "index.html", "index"),
    ("setup.jinja", "setup.html", "setup"),
    ("architecture.jinja", "architecture.html", "architecture"),
    ("cli.jinja", "cli.html", "cli"),
    ("configuration.jinja", "configuration.html", "configuration"),
    ("contributing.jinja", "contributing.html", "contributing"),
]


def main():
    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape(),
    )

    os.makedirs(CSS_DST, exist_ok=True)

    for template_name, output_name, page_id in PAGES:
        template = env.get_template(template_name)
        html = template.render(page=page_id)
        output_path = OUTPUT / output_name
        output_path.write_text(html, encoding="utf-8")
        print(f"  ✓  {output_name}")

    print("  ✓  assets/css/style.css (in place)")

    print(f"\nDone — {len(PAGES)} pages built.")


if __name__ == "__main__":
    main()
