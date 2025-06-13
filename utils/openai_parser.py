from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # Automatically loads .env from root
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_prompt_from_file(filepath="utils/system_prompt.txt"):
    with open(filepath, "r") as f:
        return f.read()

def call_openai_parser(resume_text: str) -> str:
    system_prompt = load_prompt_from_file()

    messages = [
        { "role": "system", "content": system_prompt },
        { "role": "user", "content": resume_text }
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages,
        temperature=0.0
    )

    return response.choices[0].message.content
