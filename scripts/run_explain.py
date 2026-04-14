"""
Called by the /explain slash command.
Usage:  python scripts/run_explain.py <file_path>
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from agent.ollama_client import chat

console = Console()

PROMPT_TEMPLATE = """\
Explain what this code does in simple terms, then list any potential issues you see.

```
{code}
```"""


def main():
    if len(sys.argv) < 2:
        console.print("[bold red]Usage:[/bold red] python scripts/run_explain.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        console.print(f"[bold red]File not found:[/bold red] {file_path}")
        sys.exit(1)

    with open(file_path) as f:
        code = f.read()

    # Detect language from extension for syntax highlighting
    ext = os.path.splitext(file_path)[1].lstrip(".")
    lang = ext if ext else "text"

    console.print(Panel.fit(f"[bold cyan]my_copilot — /explain[/bold cyan]"))
    console.print(f"[dim]File:[/dim] {file_path}\n")

    console.print(Panel(
        Syntax(code.strip(), lang, theme="monokai", line_numbers=True),
        title="[bold]Source[/bold]",
        border_style="dim",
    ))

    console.print("\n[bold yellow]Asking Gemma...[/bold yellow]\n")

    response = chat(PROMPT_TEMPLATE.format(code=code))

    console.print(Panel(
        Markdown(response),
        title="[bold green]Explanation & Issues[/bold green]",
        border_style="green",
    ))


if __name__ == "__main__":
    main()
