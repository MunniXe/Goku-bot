from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_goku(messages):
    response = client.chat.completions.create(
    model= "meta-llama/llama-4-maverick-17b-128e-instruct",
    messages = messages
    )
    return response.choices[0].message.content