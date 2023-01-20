import subprocess
from urllib.parse import urlsplit
import subprocess

connection_string = ""
parsed = urlsplit(connection_string)

username = parsed.username
password = parsed.password
host = parsed.hostname
port = parsed.port
database = parsed.path[1:]

subprocess.run(f"sqlacodegen postgresql://{username}:{password}@{host}/{database} --noviews --outfile models.py", shell=True)