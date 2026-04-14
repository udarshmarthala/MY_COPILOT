"""
Called by the /fix slash command.
Usage:  python scripts/run_fix.py <file_path> "<error message>"
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
A Python file has a bug. Here is the code:

```
{code}
```

Here is the error:

```
{error}
```

Diagnose what is causing the error, then provide a fixed version of the code.
Format your response as:
1. **Diagnosis** — what is wrong and why
2. **Fix** — the corrected code in full"""


def main():
    if len(sys.argv) < 3:
        console.print("[bold red]Usage:[/bold red] python scripts/run_fix.py <file_path> \"<error message>\"")
        sys.exit(1)

    file_path = sys.argv[1]
    error_message = sys.argv[2]

    if not os.path.exists(file_path):
        console.print(f"[bold red]File not found:[/bold red] {file_path}")
        sys.exit(1)

    with open(file_path) as f:
        code = f.read()

    ext = os.path.splitext(file_path)[1].lstrip(".")
    lang = ext if ext else "text"

    console.print(Panel.fit("[bold cyan]my_copilot — /fix[/bold cyan]"))
    console.print(f"[dim]File:[/dim] {file_path}\n")

    console.print(Panel(
        Syntax(code.strip(), lang, theme="monokai", line_numbers=True),
        title="[bold]Source[/bold]",
        border_style="dim",
    ))

    console.print(Panel(
        f"[bold red]{error_message}[/bold red]",
        title="[bold]Error[/bold]",
        border_style="red",
    ))

    console.print("\n[bold yellow]Asking Gemma...[/bold yellow]\n")

    response = chat(PROMPT_TEMPLATE.format(code=code, error=error_message))

    console.print(Panel(
        Markdown(response),
        title="[bold green]Diagnosis & Fix[/bold green]",
        border_style="green",
    ))


if __name__ == "__main__":
    main()
