<p align="center">
  <strong>Amphib 🐸</strong><br>
  <em>Amphib — a better breed of hiring agent.</em><br>
  Amphib reads a resume, checks what's real on GitHub, and gives you a verdict — fully offline if you want.
</p>

<p align="center">
  <a href="https://amphib.dev">
    <img alt="Website" src="https://img.shields.io/badge/web-amphib.dev-8B5CF6.svg">
  </a>
  <a href="https://www.python.org/downloads/release/python-3110/">
    <img alt="Python" src="https://img.shields.io/badge/python-3.11%2B-blue.svg">
  </a>
  <a href="LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-yellow.svg">
  </a>
</p>

Amphib ingests a resume PDF, extracts structured data with an LLM, cross-references GitHub for ground truth, and produces an explainable score. It runs locally with Ollama or uses Gemini — your data stays with you.

Amphib is built on [Hiring Agent](https://github.com/interviewstreet/hiring-agent) by HackerRank. We didn't just fork it — we're actively improving it, and every change is open source. If you like Hiring Agent, you'll love what's next.

## How it works

### 1. PDF → Text

`pymupdf_rag.py` and `pdf.py` turn PDF pages into Markdown. Headings, links, tables — everything survives.

### 2. Text → Structure

`pdf.py` feeds each section (work, education, skills, projects, awards) to an LLM using Jinja templates from `prompts/templates/`. The result is a typed `JSONResume` object.

### 3. GitHub → Proof

`github.py` finds the candidate's GitHub handle, fetches their profile and repos, classifies projects, and asks the LLM to pick the 7 most meaningful ones. No self-promotion without substance.

### 4. Structure → Score

`evaluator.py` scores across four axes — open source, personal projects, production experience, technical skills — plus bonus marks and deductions, all with cited evidence.

### 5. Score → Output

`score.py` prints a readable summary. With `DEVELOPMENT_MODE=True` it also writes to `resume_evaluations.csv` and caches intermediate results.

## Quick start

### Prerequisites

- Python 3.11+
- An LLM backend: [Ollama](https://ollama.com/) (local) or a [Gemini API key](https://aistudio.google.com/api-keys)

### Setup

```bash
git clone <your-repo-url> && cd amphib
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Pull a model (Ollama)

```bash
ollama pull gemma3:4b       # balanced
ollama pull gemma3:12b      # beefier
ollama pull gemma3:1b       # lightweight
```

### Run

```bash
cp .env.example .env        # edit your provider and key
python score.py resume.pdf
```

## Configuration

| Variable | Values | What it does |
|---|---|---|
| `LLM_PROVIDER` | `ollama` / `gemini` | Pick your backend |
| `DEFAULT_MODEL` | `gemma3:4b`, `gemini-2.5-pro`, ... | Model name |
| `GEMINI_API_KEY` | string | Required for Gemini |
| `GITHUB_TOKEN` | string | Optional — higher API rate limits |

`config.py` has one flag:

```python
DEVELOPMENT_MODE = True   # caches results, exports CSV
```

## Project layout

```
.
├── config.py                  # dev mode toggle
├── evaluator.py               # scoring engine
├── github.py                  # GitHub fetch + classification
├── llm_utils.py               # provider init + cleanup
├── models.py                  # pydantic schemas + provider wrappers
├── pdf.py                     # LLM-based section parser
├── prompt.py                  # provider → template routing
├── prompts/
│   ├── template_manager.py
│   └── templates/             # Jinja prompts
│       ├── awards.jinja
│       ├── basics.jinja
│       ├── education.jinja
│       ├── github_project_selection.jinja
│       ├── projects.jinja
│       ├── resume_evaluation_criteria.jinja
│       ├── resume_evaluation_system_message.jinja
│       ├── skills.jinja
│       ├── system_message.jinja
│       └── work.jinja
├── pymupdf_rag.py             # PDF → Markdown
├── score.py                   # CLI entry point
├── transform.py               # JSON normalisation
└── requirements.txt
```

## Provider details

**Ollama** — set `LLM_PROVIDER=ollama`, pick any model. The wrapper calls `ollama.chat` directly.

**Gemini** — set `LLM_PROVIDER=gemini`, provide your key, pick a model like `gemini-2.0-flash`. Responses are adapted to a unified format.

## License

[MIT](LICENSE) © HackerRank

## Acknowledgments

Amphib is built on [Hiring Agent](https://github.com/interviewstreet/hiring-agent) by HackerRank. Their open-source work made this possible — and we're committed to keeping it going.
