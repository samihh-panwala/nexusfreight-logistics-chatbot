from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def generate_response(messages):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not configured.")

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0.3,
        max_tokens=800
    )

    return response.choices[0].message.content