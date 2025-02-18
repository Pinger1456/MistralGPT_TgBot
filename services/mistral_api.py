import os
import requests
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
MISTRAL_API_URL = os.getenv('MISTRAL_API_URL')

def get_mistral_response(user_message: str) -> str:
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-small",
        "messages": [{"role": "user", "content": f"Преимущественно отвечай на русском, если того требует контекст: {user_message}"}],
        "max_tokens": 32000,
        "temperature": 0.7
    }
    response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content'].strip()