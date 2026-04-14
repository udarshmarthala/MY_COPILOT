Explain the code in the currently active file in the IDE.

Steps:
1. Detect the active file using this priority order:
   a. If a file path was passed as an argument, use that: $ARGUMENTS
   b. Check the conversation context for a system-reminder that says "The user opened the file <path>" — the most recent one is the active file. Extract that path.
   c. If no such reminder exists, call mcp__ide__getDiagnostics and pick the most recently modified project file (ignore .venv/, vscode-userdata, vscode-terminal URIs).
2. If no file can be determined, ask the user which file they want explained.
3. Tell the user which file you are explaining, e.g. "Explaining: agent/ollama_client.py"
4. Read the file contents with the Read tool.
5. Run this bash command from the project root to get the explanation:
   `.venv/bin/python scripts/run_explain.py "<file_path>"`
6. Print the output as-is — it is already formatted.

If the venv isn't activated or the script fails, fall back to calling explain_code() directly by reading agent/ollama_client.py and invoking it inline.
