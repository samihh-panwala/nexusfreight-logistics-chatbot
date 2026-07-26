import os
import subprocess

subprocess.run([
    "uvicorn",
    "api.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    os.environ.get("PORT", "8000")
], check=True)