#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import sys
import requests
from dotenv import load_dotenv

# Ensure stdout handles UTF-8 correctly
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment configuration
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")

def send_teams_notification(message):
    """Sends a message to the configured Microsoft Teams Webhook URL."""
    if os.getenv("ENABLE_TEAMS", "true").lower() != "true":
        print("⏭️ Teams alerts are disabled (ENABLE_TEAMS is false). Bypassing.")
        return True

    if not TEAMS_WEBHOOK_URL:
        print("❌ TEAMS_WEBHOOK_URL is not set.")
        sys.exit(1)

    payload = {
        "text": message
    }

    try:
        response = requests.post(TEAMS_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print(f"✅ Teams notification sent successfully. Status: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send Teams notification. Error details:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        send_teams_notification(" ".join(sys.argv[1:]))
    else:
        print("Usage: python teams_notifier.py 'Your message here'")
