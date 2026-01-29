import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('VAPI_API_KEY')
assistant_id = os.getenv('VAPI_ASSISTANT_ID')

def test_assistant_with_call(assistant_id):
    url = "https://api.vapi.ai/call"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "assistantId": assistant_id,
        "customer": {
            "number": "+1234567890"  # Your test number
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:            
        print(f"Test call created: {call['id']}")
        call = response.json()
        with open("test_assistant.jsonl", "a") as json_file:
            json_file.write(json.dumps(call) + "\n")
        
        return call

    else:
        print(f"Failed Request!, Status Code: {response.status_code}")
        fail = response.json()
        with open("test_assistant.jsonl", "a") as json_file:
            json_file.write(json.dumps(fail) + "\n")

        pass
        

# Create a test call
test_call = test_assistant_with_call(assistant_id)
