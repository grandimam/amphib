<p align="center">
  <strong>Amphib</strong><br>
  <em>See through the resume. The truth is in the details.</em><br>
  Reads a resume, extracts what matters, and shows you the full picture.
</p>

<p align="center">
  <a href="https://amphib.dev">
    <img alt="Website" src="https://img.shields.io/badge/web-amphib.dev-8B5CF6.svg">
  </a>
  <a href="https://www.python.org/downloads/release/python-3110/">
    <img alt="Python" src="https://img.shields.io/badge/python-3.12%2B-blue.svg">
  </a>
  <a href="LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-yellow.svg">
  </a>
</p>

Our goal: take what HackerRank's [Hiring Agent](https://github.com/interviewstreet/hiring-agent) started and build on top of it. Better CLI, better output, cleaner code. Everything stays open source.

Install it with `pip install -e .` and the `amphib` command is available anywhere in your terminal. Or use the one-liner above.

Amphib turns a resume PDF into Markdown, runs it through LLM pipelines for layout analysis, data extraction, and scoring, then shows the results in a rich terminal UI.

## Commands

```bash
amphib analyze <resume.pdf>     # Analyze resume layout
amphib extract <resume.pdf>     # Extract structured data (JSON Resume)
amphib evaluate <resume.pdf>    # Score resume across 4 categories
```

### analyze (layout analysis)

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃             Layout Analysis                     ┃
┃  Layout:    Two Column                          ┃
┃  Method:    Column boundary detection           ┃
┃  Confidence: high                               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Section Order
├─ Header
├─ Summary
├─ Experience
├─ Education
├─ Skills
└─ Projects

Subsections with Columns
┌──────────────┬─────────┬────────────────┬──────────┐
│ Subsection   │ Columns │ Items          │ Evidence │
├──────────────┼─────────┼────────────────┼──────────┤
│ Skills       │    2    │ Python, Go,... │ Sidebar  │
└──────────────┴─────────┴────────────────┴──────────┘
```

### extract (structured data)

```
╭────────────────────────────────╮
│  Jane Doe                      │
│  fauzan@example.com            │
│  github.com/fauzan             │
╰────────────────────────────────╯

Work Experience (3)
├─ Senior Engineer @ Acme Corp    2021-03 – present
│  └─ Led team of 5, built microservice infra
├─ Software Engineer @ Beta Inc   2018-06 – 2021-02
│  └─ Built REST APIs, reduced latency 40%
└─ Junior Dev @ Gamma LLC         2016-01 – 2018-05
   └─ Maintained legacy app

Skills (4 categories)
┌──────────────┬──────────────────────────┐
│ Category     │ Skills                   │
├──────────────┼──────────────────────────┤
│ Languages    │ Python, TypeScript, Go   │
│ Frameworks   │ React, FastAPI, Next.js  │
│ Tools        │ Docker, Kubernetes       │
│ Databases    │ Postgres, Redis          │
└──────────────┴──────────────────────────┘

Education (1)
┌──────────────┬────────┬───────┬──────────────┬───────┐
│ Institution  │ Degree │ Field │ Dates        │ Score │
├──────────────┼────────┼───────┼──────────────┼───────┤
│ MIT          │ BSc    │ CS    │ 2012 – 2016  │ 3.8   │
└──────────────┴────────┴───────┴──────────────┴───────┘
```

### evaluate (scoring)

```
╭──────────────────────────────────────╮
│  Resume Evaluation: Fauzan           │
╰──────────────────────────────────────╯

Category Scores
┌──────────────────┬─────────┬──────────────────────┬──────────────────┐
│ Category         │  Score  │ Bar                  │ Evidence         │
├──────────────────┼─────────┼──────────────────────┼──────────────────┤
│ Open Source      │  18/35  │ █████░░░░░░ 51%      │ 2 minor PRs      │
│ Self Projects    │  24/30  │ ████████░░ 80%       │ Strong portfolio │
│ Production       │  15/25  │ █████░░░░░░ 60%      │ 3 yrs exp        │
│ Technical Skills │   8/10  │ ██████████ 80%       │ Broad stack      │
├──────────────────┼─────────┼──────────────────────┼──────────────────┤
│ Total            │  65/100 │                      │                  │
│ Bonus: +5  Deductions: -2 │                      │ Final: 68/120    │
└──────────────────┴─────────┴──────────────────────┴──────────────────┘

╭─── Bonus Points (+5) ──────────────────────────────╮
│ Notable volunteer work, blog, GSoC participation   │
╰────────────────────────────────────────────────────╯

╭─── Deductions (-2) ────────────────────────────────╮
│ Missing GitHub links for 1 project                 │
╰────────────────────────────────────────────────────╯

╭─── Key Strengths ──────────────────────────────────╮
│ • Strong full-stack engineering experience         │
│ • Complex personal projects with real-world impact │
│ • Broad technical skills across the stack          │
╰────────────────────────────────────────────────────╯

╭─── Areas for Improvement ──────────────────────────╮
│ • Limited open source contributions                │
│ • Consider enhancing technical communication       │
╰────────────────────────────────────────────────────╯
```

## How it works

```
PDF → Markdown → LLM → Structured Data → Rich TUI
│                  │            │
│ pymupdf4llm     │ Jinja      │ Typer + Rich
│                 │ templates  │
```

### 1. PDF → Text
`PDFParser` uses `pymupdf4llm` to convert PDF pages to clean Markdown. Headings, links, and tables all survive the round trip.

### 2. Text → Structured Data
The `core.Amphib` orchestrator sends the Markdown to an LLM with Jinja2 system prompts from `core/prompts/`. Each command (`analyze`, `extract`, `evaluate`) uses a different prompt template.

### 3. Rich TUI Output
Results render with `rich`: tables, trees, panels, color-coded score bars, and progress spinners while the LLM works.

## Quick start

### One-liner (Linux / macOS)

```bash
curl -sSL https://raw.githubusercontent.com/grandimam/amphib/main/install.sh | bash
```

Or if you prefer `wget`:

```bash
wget -qO- https://raw.githubusercontent.com/grandimam/amphib/main/install.sh | bash
```

This installs to `~/.amphib`, creates a venv, and symlinks the `amphib` command to `~/.local/bin/amphib`.

### Prerequisites

- Python 3.12+
- An [OpenRouter](https://openrouter.ai/) API key

### Setup

```bash
git clone <your-repo-url> && cd amphib
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

### Configure

```bash
cp .env.example .env   # then edit .env with your OpenRouter API key
```

### Run on the sample resume

```bash
amphib analyze examples/java-engineer.pdf
amphib extract examples/java-engineer.pdf
amphib evaluate examples/java-engineer.pdf
```

## Configuration

| Variable | Default | What it does |
|---|---|---|
| `OPENROUTER_API_KEY` | _required_ | OpenRouter API key |
| `MODEL_NAME` | `openrouter/openai/gpt-3.5-turbo` | LLM model to use |
| `PROMPT_DIR` | `prompts` | Directory with `.jinja` templates |

## Project layout

```
.
├── main.py                     # CLI entry point (Typer)
├── cli/
│   ├── analyze.py              # Layout analysis command
│   ├── extract.py              # Structured extraction command
│   └── evaluate.py             # Scoring command
├── core/
│   ├── __init__.py             # Amphib orchestrator
│   ├── config.py               # Pydantic settings
│   ├── constants.py            # Role/content constants
│   ├── parsers.py              # PDFParser (pymupdf4llm)
│   ├── prompt.py               # JinjaPromptProvider
│   ├── schemas.py              # Pydantic schemas (GitHub)
│   ├── types.py                # Type aliases
│   └── providers/
│       ├── base.py             # Provider protocols
│       ├── chat.py             # OpenRouterProvider
├── core/prompts/
│   ├── layout.jinja            # Layout analysis prompt
│   ├── extract.jinja           # Structured extraction prompt
│   └── evaluate.jinja          # Resume scoring prompt
├── pyproject.toml
├── uv.lock
└── requirements.txt
```

## What we fixed from Hiring Agent

We started from HackerRank's [Hiring Agent](https://github.com/interviewstreet/hiring-agent) and rebuilt most of it. Here is what we think it got wrong:

**Too many entry points.** Hiring Agent had `score.py`, `pdf.py`, `github.py` all doing overlapping things. You had to dig through the code to figure out which script to run. Amphib has three commands: `analyze`, `extract`, `evaluate`. One entry point (`main.py`), consistent flags.

**No feedback while it runs.** You ran `score.py` and stared at a blank terminal for 30 seconds. Amphib shows a spinner with status messages so you know it is actually working.

**Raw JSON dumps.** The output was unformatted JSON blobs. Amphib renders tables, trees, panels, and color-coded bars so you can actually read the results.

**Single-use architecture.** The old code mixed PDF parsing, LLM calls, GitHub fetching, and scoring into one tangled flow. Amphib splits these into a `core` module with clean interfaces. You can swap parsers, model providers, or prompt loaders without rewriting everything.

**Prompt templates scattered.** Templates were spread across files with no clear naming convention. Amphib keeps them in `prompts/` with one file per command. The `JinjaPromptProvider` loads them automatically.

**Template variables were not being passed.** The `{{ text_content }}` variables in the prompts rendered as empty strings because nobody called `template.render()` with the resume text. The resume was sent in the user message but the system prompt had a blank where the resume should have been. Amphib passes the parsed text into the template so the LLM sees the full context.

**GitHub overreach.** Hiring Agent spends a lot of effort fetching GitHub profiles and classifying repos. That is useful but it should not be the main pipeline. Amphib keeps GitHub as a separate provider you can call if you want, not something baked into every resume scan.

We are not done. There is more to fix. But every change stays open source.

## License

[MIT](LICENSE) © HackerRank

## Acknowledgments

Amphib is built on [Hiring Agent](https://github.com/interviewstreet/hiring-agent) by HackerRank. Their open-source work made this possible. We are committed to keeping it going.
