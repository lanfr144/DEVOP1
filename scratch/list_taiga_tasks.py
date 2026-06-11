#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TAIGA_API_URL = "https://api.taiga.io/api/v1"
TAIGA_USERNAME = os.getenv("TAIGA_USERNAME")
TAIGA_PASSWORD = os.getenv("TAIGA_PASSWORD")
PROJECT_ID = os.getenv("TAIGA_PROJECT_ID")

def list_tasks():
    payload = {
        "type": "normal",
        "username": TAIGA_USERNAME,
        "password": TAIGA_PASSWORD
    }
    response = requests.post(f"{TAIGA_API_URL}/auth", json=payload)
    response.raise_for_status()
    token = response.json().get("auth_token")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    r = requests.get(f"{TAIGA_API_URL}/tasks?project={PROJECT_ID}&page_size=100", headers=headers)
    r.raise_for_status()
    tasks = r.json()
    
    print(f"Retrieved {len(tasks)} tasks:")
    for t in tasks:
        # Taiga tasks have a 'ref' (reference number) and a 'subject'
        print(f"Task #{t['ref']} (ID: {t['id']}) - {t['subject']} - Status ID: {t['status']} - Closed: {t['is_closed']}")

if __name__ == "__main__":
    list_tasks()
