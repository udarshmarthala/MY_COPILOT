# CLAUDE.md — my_copilot

Everything you need to understand, run, and contribute to this project.

---

## What this project is

**my_copilot** is a local AI coding agent — think GitHub Copilot, but running
entirely on your machine with no external API calls and no usage costs.

The model is **Gemma**, served locally via **Ollama**. All inference happens
on-device. The project is written in Python and is being built incrementally:
starting from a minimal Ollama wrapper, growing toward a full coding agent that
can autocomplete code, answer questions about a codebase, and autonomously fix
bugs or write features.

---

## Tech stack

| Layer | Tool | Notes |
|-------|------|-------|
| LLM runtime | [Ollama](https://ollama.com) | Serves models locally over HTTP |
| Model | `gemma:latest` | Default; swappable via `DEFAULT_MODEL` |
| Language | Python 3.10+ | |
| Terminal UI | [Rich](https://github.com/Textualize/rich) | Panels, Markdown rendering, syntax highlighting |
| HTTP (transitive) | httpx + pydantic | Pulled in by the `ollama` SDK |

---

## Folder structure

```
my_copilot/
├── agent/                   # Core agent logic — import from here
│   ├── __init__.py
│   └── ollama_client.py     # All Ollama interactions live here
│
├── scripts/                 # Runnable demos and smoke-tests
│   ├── test_connection.py   # Verifies Ollama is up; streams a response
│   └── test_explain.py      # Demonstrates explain_code() with Rich output
│
├── tests/                   # Pytest test suite (mostly empty right now)
│   └── __init__.py
│
├── .venv/                   # Local virtual environment (not committed)
├── requirements.txt
├── README.md
└── CLAUDE.md                # This file
```

### `agent/ollama_client.py` — current public API

```python
chat(prompt, model)          # Send a prompt, return full response string
stream_chat(prompt, model)   # Send a prompt, yield response chunks
explain_code(snippet, model) # Wrap a code snippet in an explain prompt, return string
```

All three accept an optional `model` arg that defaults to `DEFAULT_MODEL = "gemma:latest"`.

---

## Setup

```bash
# 1. Start Ollama (if not already running)
ollama serve

# 2. Pull the model
ollama pull gemma:latest

# 3. Create and activate the virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Verify everything works

```bash
python scripts/test_connection.py   # streams a Fibonacci response
python scripts/test_explain.py      # explains a binary search function
```

If Ollama is already running (port 11434 in use), skip `ollama serve` — that
error just means the server is already up.

---

## Coding conventions

**Keep functions small and single-purpose.** Each function in `ollama_client.py`
does exactly one thing. New capabilities should follow the same pattern: one
function, one job.

**Type hints on all function signatures.**
```python
# good
def explain_code(snippet: str, model: str = DEFAULT_MODEL) -> str:

# bad
def explain_code(snippet, model=DEFAULT_MODEL):
```

**Docstrings on every public function.** One line is enough if the name is
clear. Use the imperative mood ("Send a prompt…", not "Sends a prompt…").

**No unnecessary abstraction.** Don't create base classes, registries, or
plugin systems until there are at least three concrete things that need them.
Duplicate two lines of code rather than prematurely abstracting them.

**Rich for all terminal output in scripts.** Use `Panel`, `Markdown`, and
`Syntax` from Rich — not plain `print()` — so output is consistently readable.
`Syntax` should use the `"monokai"` theme with `line_numbers=True`.

**Don't add error handling inside `agent/`.** The client functions let
exceptions propagate. Scripts handle errors at their boundary and print
friendly messages with Rich.

**No external API calls.** Everything routes through Ollama. If a feature
would require an internet connection, reconsider the design.

---

## Current status

| Area | Status |
|------|--------|
| Ollama connection | Working |
| Streaming responses | Working |
| Code explanation | Working |
| Formatted terminal output | Working |
| Tests | Scaffolded, not yet written |
| Chat history / multi-turn | Not started |
| Codebase context (RAG) | Not started |
| Bug fixing agent | Not started |
| Editor integration | Not started |

---

## What to build next (rough order)

1. **Multi-turn chat** — extend `ollama_client.py` to maintain a message
   history list so conversations have context across turns.

2. **Code generation** — a `generate_code(description)` function that turns
   a plain-English description into a Python function.

3. **Codebase context** — read files from the project directory and include
   relevant snippets in the prompt so Gemma can answer questions about *this*
   codebase specifically.

4. **Bug fixer** — given a function and an error message, ask Gemma to produce
   a corrected version.

5. **Interactive CLI** — a REPL loop (`python -m agent`) where you can chat,
   paste code, and get explanations without editing scripts.

6. **Tests** — pytest unit tests for `agent/ollama_client.py`, mocking Ollama
   responses so tests run offline.

---

## Key decisions and why

**Ollama over direct model loading** — Ollama handles model management,
quantization, and GPU offloading transparently. We don't need to deal with
`transformers` or CUDA setup.

**`gemma:latest` as the default** — small enough to run on a laptop, capable
enough for code tasks. The model is swappable everywhere via the `model=`
parameter.

**Rich for terminal UI** — Gemma's responses are Markdown. Rendering them with
`rich.markdown.Markdown` makes them immediately readable without building a web
UI.

**`scripts/` separate from `agent/`** — scripts are throwaway demos and
smoke-tests; `agent/` is the importable library. Keeping them separate means
scripts can be deleted or changed without touching core logic.
