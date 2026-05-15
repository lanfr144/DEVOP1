import os
import requests
import sys

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_notification(message):
    if not DISCORD_WEBHOOK_URL:
        print("❌ DISCORD_WEBHOOK_URL is not set.")
        sys.exit(1)
        
    payload = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.ok:
        print("✅ Discord notification sent successfully.")
    else:
        print(f"❌ Failed to send Discord notification: {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        send_notification(" ".join(sys.argv[1:]))
    else:
        print("Usage: python discord_notifier.py 'Your message here'")
