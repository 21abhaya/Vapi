import os
import requests

from dotenv import load_dotenv

load_dotenv()

vapi_api_key = os.getenv('VAPI_API_KEY')
print("apiKEY:", vapi_api_key)

def upload_file(file_path):
    url = "https://api.vapi.ai/file"
    headers = {"Authorization": f"Bearer {vapi_api_key}"}
    
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, headers=headers, files=files)
        return response.json()

# Upload both files
accounts_file = upload_file("accounts.csv")
transactions_file = upload_file("transactions.csv")

print(f"Accounts file ID: {accounts_file['id']}")
print(f"Transactions file ID: {transactions_file['id']}")

