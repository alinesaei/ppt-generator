import openai
from openai import Completion
import os
from dotenv import load_dotenv


load_dotenv()
# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_KEY')

def generate_content(input, prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (prompt)},
            {"role": "user", "content": ("The user wants a presentation about " + input)}
        ],
        temperature=0.5,
    )

    return response['choices'][0]['message']['content']