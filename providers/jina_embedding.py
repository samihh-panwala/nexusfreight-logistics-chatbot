import os
import requests
from dotenv import load_dotenv

load_dotenv()

JINA_API_KEY = os.getenv("JINA_API_KEY")
print("JINA_API_KEY =", JINA_API_KEY)

def get_embedding(text):

    response = requests.post(
        "https://api.jina.ai/v1/embeddings",
        headers={
            "Authorization": f"Bearer {JINA_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "jina-embeddings-v3",
            "task": "retrieval.query",
            "input": [text],
        },
    )

    response.raise_for_status()

    return response.json()["data"][0]["embedding"]