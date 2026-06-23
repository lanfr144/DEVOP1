#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import requests
import sys

# -----------------------------------------------------------------------------
# DISCORD NOTIFICATION SCRIPT
# -----------------------------------------------------------------------------
# This script sends notification messages to Discord chat channels using Webhooks.
# The webhook URL is retrieved from the host environment variables.
# -----------------------------------------------------------------------------

# Ensure stdout handles UTF-8 correctly
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Retrieve the webhook integration URL from environment variables
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_notification(message):
    """Posts a message to the configured Discord channel webhook."""
    if os.getenv("ENABLE_DISCORD", "true").lower() != "true":
        print("⏭️ Discord alerts are disabled (ENABLE_DISCORD is false). Bypassing.")
        return

    if not DISCORD_WEBHOOK_URL:
        print("❌ DISCORD_WEBHOOK_URL is not set.")
        sys.exit(1)
        
    # JSON payload structure expected by Discord API
    payload = {"content": message}
    
    # Send POST request containing JSON string
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.ok:
        print("✅ Discord notification sent successfully.")
    else:
        print(f"❌ Failed to send Discord notification: {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    # If the user passes text as command line arguments, send it
    if len(sys.argv) > 1:
        send_notification(" ".join(sys.argv[1:]))
    else:
        print("Usage: python discord_notifier.py 'Your message here'")