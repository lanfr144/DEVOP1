#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import requests
from dotenv import load_dotenv

def test_teams_webhook():
    # 1. Load the .env file
    load_dotenv()
    
    # 2. Fetch the webhook URL
    webhook_url = os.getenv("TEAMS_WEBHOOK_URL")

    if not webhook_url:
        print("Error: Could not find TEAMS_WEBHOOK_URL in the .env file.")
        return

    # 3. Create the message payload
    payload = {
        "text": "François for DEVOPS Project check if my .env TEAMS_WEBHOOK_URL is set up correctly. Your Teams Webhook is configured correctly. 🎉"
    }

    # 4. Send the POST request to Microsoft Teams
    print(f"Sending test message to: {webhook_url[:45]}...") # Prints a masked version of the URL
    
    try:
        response = requests.post(webhook_url, json=payload)
        
        # Check if the request was successful
        response.raise_for_status() 
        
        print(f"Success! The webhook responded with status code: {response.status_code}")
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message. Error details:\n{e}")

if __name__ == "__main__":
    test_teams_webhook()