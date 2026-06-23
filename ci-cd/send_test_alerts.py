#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import sys
import os
from dotenv import load_dotenv

# Ensure script directory is in PATH to allow sibling imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from mail_notifier import send_mail
    from discord_notifier import send_notification as send_discord
    from teams_notifier import send_teams_notification as send_teams
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def run_all_tests():
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

    print("🚀 Initiating Project Antigravity (DEVOP1) Alert Verification Stack...")
    
    test_message = "Project Antigravity DevOps Verification: Alert notifications stack is working! 🔔"

    print("\n--- 1. Testing Teams Webhook Alert ---")
    send_teams(test_message)

    print("\n--- 2. Testing Discord Webhook Alert ---")
    send_discord(test_message)

    print("\n--- 3. Testing SMTP Mail Alert (with Redirection) ---")
    send_mail(
        subject="[DEVOP1] System Integration Verification Alert",
        body=test_message,
        original_recipient="qa-notifications@devop1.internal"
    )

    print("\n✅ Verification sequence complete!")

if __name__ == "__main__":
    run_all_tests()
