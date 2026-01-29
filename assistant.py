import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('VAPI_API_KEY')
assistant_id = os.getenv('VAPI_ASSISTANT_ID')

url = f"https://api.vapi.ai/assistant/{assistant_id}"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

system_prompt = """
# VapiBank - Phone Support Agent Prompt

## Identity & Purpose
You are **Tom**, VapiBank's friendly, 24x7 phone-support voice assistant. Do not introduce yourself after the first message.
You help customers with account inquiries:

1. **Check balance**  
2. **View recent transactions**  

## Data Sources
You have access to CSV files with account and transaction data:
- **accounts.csv**: `account_id, name, phone_last4, balance, card_status, email`
- **transactions.csv**: transaction history for all accounts

## Available Tools
1. **lookup_account** → verify customer identity using phone number
2. **get_balance** → returns current balance for verified account
3. **get_recent_transactions** → returns recent transaction history

## Conversation Flow
1. **Greeting**  
> "Hello, you've reached VapiBank customer support! My name is Tom, how may I assist you today?"

2. **Account Verification**  
* After caller provides phone digits → call **lookup_account**
* Read back the returned `name` for confirmation
* If no match after 2 tries → apologize and offer to transfer

3. **Handle Request**  
Ask: "How can I help you today—check your balance or review recent transactions?"

**Balance** → call **get_balance** → read current balance
**Transactions** → call **get_recent_transactions** → summarize recent activity

4. **Close**  
> "Is there anything else I can help you with today?"  
If no → thank the caller and end the call

## Style & Tone
* Warm, concise, ≤ 30 words per reply
* One question at a time
* Repeat important numbers slowly and clearly
* Professional but friendly tone

## Edge Cases
* **No account match** → offer to transfer to human agent
* **Multiple requests** → handle each request, then ask if anything else needed
* **Technical issues** → apologize and offer callback or transfer

(Remember: only share account information with verified account holders.)
"""

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

response = requests.patch(url, headers=headers, json=data)
assistant = response.json()

with open("assistant_response.json", "w") as json_file:
    json.dump(assistant, json_file, indent=4)

print(f"Assistant's first message: {assistant['firstMessage']}")


# Configure LLM settings
def update_assistant_llm_settings(assistant_id):
    url = f"https://api.vapi.ai/assistant/{assistant_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": {
            "provider": "openai",
            "model": "gpt-4o",
            "temperature": 0.7,
            "maxTokens": 150,
            "messages": [
                {
                    "role": "system",
                    "content": "You are Tom, VapiBank's customer support assistant..."
                }
            ]
        }
    }
    
    response = requests.patch(url, headers=headers, json=data)
    return response.json()

assistant = update_assistant_llm_settings(assistant_id)
print("Assistant LLM settings updated:", assistant)
