import ollama


DEFAULT_MODEL = "gemma:latest"


def chat(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """Send a prompt to the model and return the response text."""
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


def stream_chat(prompt: str, model: str = DEFAULT_MODEL):
    """Stream a response token by token. Yields string chunks."""
    for chunk in ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    ):
        yield chunk["message"]["content"]


def explain_code(snippet: str, model: str = DEFAULT_MODEL) -> str:
    """Ask the model to explain what a code snippet does."""
    prompt = f"Explain what the following code does, clearly and concisely:\n\n```\n{snippet}\n```"
    return chat(prompt, model=model)


def autocomplete_code(snippet: str, cursor_pos: int, model: str = DEFAULT_MODEL) -> str:
    """Return a completion suggestion for the code at cursor_pos."""
    before = snippet[:cursor_pos]
    after = snippet[cursor_pos:]
    prompt = (
        "You are a code autocomplete engine. "
        "Complete the code at the <CURSOR> marker. "
        "Output ONLY the inserted text — no explanations, no markdown fences, no surrounding code.\n\n"
        f"{before}<CURSOR>{after}"
    )
    raw = chat(prompt, model=model)
    # Strip any accidental markdown fences Gemma may add
    lines = raw.strip().splitlines()
    lines = [l for l in lines if not l.startswith("```")]
    return "\n".join(lines).strip()
