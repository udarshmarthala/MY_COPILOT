Fix a bug in a file given an error message.

Usage: /fix <file_path> | <error message>

Steps:
1. Parse $ARGUMENTS — split on the first ` | ` to get file_path and error_message.
2. If no arguments provided, ask the user: "Please provide a file path and error message: /fix <file_path> | <error message>"
3. Run from the project root:
   `.venv/bin/python scripts/run_fix.py "<file_path>" "<error_message>"`
4. Print the output as-is — it is already formatted.
