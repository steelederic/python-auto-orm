import os
import subprocess

connection_string = "postgresql://herzy1ad7fzsmjdg:FVVM8fvcoKvjfiXT65Caz5rwbbvfYwE7@68.183.154.29/f2171d50-aa56-40a8-8ee2-ec3b4a1459c3?ssl=verify=true".strip(
    "?ssl=verify=true"
)

subprocess.run(f"sqlacodegen {connection_string} --noviews --outfile models.py", capture_output=True)