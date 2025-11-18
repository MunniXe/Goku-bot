from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Send a simple test message
response = client.chat.completions.create(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    messages=[
        {"role": "system", "content": "You are Goku, a friendly anime companion bot."},
        {"role": "user", "content": "How did you beat Moro? Describe what happened"}
    ],
)

print(response.choices[0].message.content)
