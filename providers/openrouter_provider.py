from openai import OpenAI
from config import OPENROUTER_API_KEY

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


def generate_response(messages):

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0.3,
        max_tokens=800
    )

    return response.choices[0].message.content