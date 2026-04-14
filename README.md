# my_copilot

A local AI coding agent powered by [Gemma](https://ollama.com/library/gemma) via [Ollama](https://ollama.com).  
No external API keys. No usage costs. Runs entirely on your machine.

## Planned capabilities

- **Code autocomplete** — context-aware completions in your editor
- **Codebase chat** — ask questions about your project's code
- **Autonomous agent** — fix bugs and write features on request

## Project layout

```
my_copilot/
├── agent/                  # Core agent logic
│   ├── __init__.py
│   └── ollama_client.py    # Thin wrapper around the Ollama Python SDK
├── scripts/
│   └── test_connection.py  # Smoke-test: verifies Ollama + gemma:latest works
├── tests/                  # Unit / integration tests (pytest)
├── requirements.txt
└── README.md
```

## Setup

**1. Install Ollama**

Download from https://ollama.com and start the server:

```bash
ollama serve
```

**2. Pull the model**

```bash
ollama pull gemma:latest
```

**3. Install Python dependencies**

```bash
pip install -r requirements.txt
```

## Smoke test

Verify everything is wired up:

```bash
python scripts/test_connection.py
```

You should see a streamed response from Gemma printed to the terminal.

## Tech stack

| Layer | Choice |
|-------|--------|
| LLM runtime | Ollama |
| Model | Gemma (local) |
| Language | Python 3.10+ |
| Terminal UI | Rich |
