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
import os
import sys
from dotenv import load_dotenv

try:
    from teams_notifier import send_teams_notification
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from teams_notifier import send_teams_notification

def test_teams_webhook():
    load_dotenv()
    msg = "François for DEVOPS Project check if my .env TEAMS_WEBHOOK_URL is set up correctly. Your Teams Webhook is configured correctly. 🎉"
    send_teams_notification(msg)

if __name__ == "__main__":
    test_teams_webhook()