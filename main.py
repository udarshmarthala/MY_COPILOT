"""
Entry point for the my_copilot autocomplete feature.
Usage:  echo "<code>" | python main.py <cursor_pos>
        cat myfile.py | python main.py 42
"""

import sys
from agent.ollama_client import autocomplete_code

if __name__ == "__main__":
    snippet = sys.stdin.read()
    cursor_pos = int(sys.argv[1]) if len(sys.argv) > 1 else len(snippet)
    print(autocomplete_code(snippet, cursor_pos))
