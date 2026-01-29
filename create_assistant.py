import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('VAPI_API_KEY')

url = f"https://api.vapi.ai/assistant/"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

system_prompt = "You are Tom, a friendly VapiBank customer support assistant. Help customers check balances and view recent transactions. Always verify identity with phone number first."
data = {
    "name": "Tom",
    "firstMessage": "Hello, you've reached VapiBank customer support! My name is Tom, how may I assist you today?",
    "model": {
        "provider": "openai",
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            }
        ]
    },
    "voice": {
        "provider": "11labs",
        "voiceId": "burt"
    }
}
response = requests.post(url, headers=headers, json=data)
assistant = response.json()
print(f"Assistant created with ID: {assistant['id']}")

