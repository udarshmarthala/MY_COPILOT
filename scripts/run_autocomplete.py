"""
Called by the /autocomplete slash command.
Usage:  python scripts/run_autocomplete.py <file_path> <cursor_pos>
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from agent.ollama_client import autocomplete_code

console = Console()


def main():
    if len(sys.argv) < 3:
        console.print("[bold red]Usage:[/bold red] python scripts/run_autocomplete.py <file_path> <cursor_pos>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        cursor_pos = int(sys.argv[2])
    except ValueError:
        console.print("[bold red]Error:[/bold red] cursor_pos must be an integer")
        sys.exit(1)

    if not os.path.exists(file_path):
        console.print(f"[bold red]File not found:[/bold red] {file_path}")
        sys.exit(1)

    with open(file_path) as f:
        code = f.read()

    if cursor_pos < 0 or cursor_pos > len(code):
        console.print(f"[bold red]Error:[/bold red] cursor_pos {cursor_pos} is out of range (0–{len(code)})")
        sys.exit(1)

    ext = os.path.splitext(file_path)[1].lstrip(".")
    lang = ext if ext else "text"

    console.print(Panel.fit("[bold cyan]my_copilot — /autocomplete[/bold cyan]"))
    console.print(f"[dim]File:[/dim] {file_path}  [dim]Cursor:[/dim] {cursor_pos}\n")

    console.print(Panel(
        Syntax(code.strip(), lang, theme="monokai", line_numbers=True),
        title="[bold]Source[/bold]",
        border_style="dim",
    ))

    console.print("\n[bold yellow]Asking Gemma...[/bold yellow]\n")

    suggestion = autocomplete_code(code, cursor_pos)

    console.print(Panel(
        Syntax(suggestion, lang, theme="monokai", line_numbers=False),
        title="[bold green]Suggestion[/bold green]",
        border_style="green",
    ))


if __name__ == "__main__":
    main()
