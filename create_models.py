import os
import subprocess
from app import connection_string

subprocess.run(f"sqlacodegen {connection_string} --noviews --outfile models.py", capture_output=True)
