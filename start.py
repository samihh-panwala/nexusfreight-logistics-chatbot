import os
import subprocess

DB_FILE = "chroma_db/chroma.sqlite3"

if not os.path.exists(DB_FILE):
    print("ChromaDB not found. Building vector database...")
    subprocess.run(["python", "rag/vector_store.py"], check=True)
else:
    print("Existing ChromaDB found.")

subprocess.run([
    "uvicorn",
    "api.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    os.environ["PORT"]
], check=True)