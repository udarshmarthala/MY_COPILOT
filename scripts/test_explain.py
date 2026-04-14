"""
Demo: explain a code snippet and render the response with Rich.
Run with:  python scripts/test_explain.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from agent.ollama_client import explain_code

console = Console()

SNIPPET = """\
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
"""


def main():
    console.print(Panel.fit("[bold cyan]my_copilot — code explainer[/bold cyan]"))

    console.print(Panel(
        Syntax(SNIPPET.strip(), "python", theme="monokai", line_numbers=True),
        title="[bold]Code Snippet[/bold]",
        border_style="dim",
    ))

    console.print("\n[bold yellow]Asking Gemma...[/bold yellow]\n")

    explanation = explain_code(SNIPPET)

    console.print(Panel(
        Markdown(explanation),
        title="[bold green]Explanation[/bold green]",
        border_style="green",
    ))


if __name__ == "__main__":
    main()
