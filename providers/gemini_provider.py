import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

def generate_response(messages):

    prompt = ""

    for msg in messages:
        prompt += f"{msg['role']}:\n{msg['content']}\n\n"

    response = model.generate_content(prompt)

    return response.text