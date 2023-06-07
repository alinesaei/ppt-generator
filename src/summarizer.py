import openai
import os 

# Set up your OpenAI API credentials
openai.api_key = os.getenv('OPENAI_KEY')

# Function to generate text summaries using GPT-3
def generate_summary(text):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=text,
        max_tokens=150,
        temperature=0.3,
        n=1,
        stop=None,
    )
    summary = response.choices[0].text.strip()
    return summary
# i want to add a module to generate a summary for the presentation