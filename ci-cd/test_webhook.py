#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import requests
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# MICROSOFT TEAMS WEBHOOK INTEGRATION TESTER
# -----------------------------------------------------------------------------
# This script reads Microsoft Teams Webhook URL from the .env configuration and
# posts a test payload to verify successful connection.
# -----------------------------------------------------------------------------
def test_teams_webhook():
    # 1. Load variables from the .env file
    load_dotenv()
    
    # 2. Fetch the Teams integration webhook URL
    webhook_url = os.getenv("TEAMS_WEBHOOK_URL")

    if not webhook_url:
        print("Error: Could not find TEAMS_WEBHOOK_URL in the .env file.")
        return

    # 3. Create the test message payload (Teams expects a 'text' field)
    payload = {
        "text": "François for DEVOPS Project check if my .env TEAMS_WEBHOOK_URL is set up correctly. Your Teams Webhook is configured correctly. 🎉"
    }

    # Print a masked version of the URL to stdout for security auditing
    print(f"Sending test message to: {webhook_url[:45]}...")
    
    try:
        # 4. Send the HTTP POST request to Microsoft Teams API
        response = requests.post(webhook_url, json=payload)
        
        # Raise exception if request failed (non-2xx response)
        response.raise_for_status() 
        
        print(f"Success! The webhook responded with status code: {response.status_code}")
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message. Error details:\n{e}")

if __name__ == "__main__":
    test_teams_webhook()