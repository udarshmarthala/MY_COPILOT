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
