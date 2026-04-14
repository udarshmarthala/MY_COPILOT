"""
Quick smoke-test: connects to Ollama and sends a prompt to gemma:latest.
Run with:  python scripts/test_connection.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from rich.console import Console
from rich.panel import Panel
from agent.ollama_client import stream_chat

console = Console()

PROMPT = "Write a Python function that returns the nth Fibonacci number. Keep it short."


def main():
    console.print(Panel.fit("[bold cyan]my_copilot — connection test[/bold cyan]"))
    console.print(f"[dim]Model:[/dim] gemma:latest")
    console.print(f"[dim]Prompt:[/dim] {PROMPT}\n")

    console.print("[bold green]Response:[/bold green]")
    try:
        for chunk in stream_chat(PROMPT):
            console.print(chunk, end="", highlight=False)
        console.print()  # newline after stream ends
        console.print("\n[bold green]Connection successful.[/bold green]")
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        console.print(
            "[yellow]Make sure Ollama is running (`ollama serve`) "
            "and gemma:latest is pulled (`ollama pull gemma:latest`).[/yellow]"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
