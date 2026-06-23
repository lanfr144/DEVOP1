#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import sys
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Ensure stdout handles UTF-8 correctly
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment configuration
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_mail(subject, body, original_recipient="alert@company.internal"):
    """
    Sends an email using the SMTP settings. 
    Redirects ALL emails to EMAIL_USER as requested to prevent external leaks.
    """
    if os.getenv("ENABLE_MAIL", "true").lower() != "true":
        print("⏭️ Mail alerts are disabled (ENABLE_MAIL is false). Bypassing.")
        return True

    if not EMAIL_USER or not EMAIL_PASS:
        print("❌ EMAIL_USER or EMAIL_PASS is not set in environment variables.")
        sys.exit(1)

    # Redirection logic
    target_recipient = EMAIL_USER
    print(f"🔄 Redirection active: Overriding target recipient '{original_recipient}' -> '{target_recipient}'")

    # Create message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = target_recipient
    msg['X-Original-To'] = original_recipient

    try:
        # Establish secure connection
        print(f"Connecting to SMTP server {EMAIL_HOST}:{EMAIL_PORT}...")
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=5)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        
        # Send
        server.sendmail(EMAIL_USER, [target_recipient], msg.as_string())
        server.quit()
        print(f"✅ Mail sent successfully to {target_recipient} (Redirected from {original_recipient}).")
        return True
    except Exception as e:
        print(f"❌ Failed to send mail: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        message_body = " ".join(sys.argv[1:])
    else:
        message_body = "Test email from Project Antigravity (DEVOP1) alerting engine."
    
    send_mail(
        subject="[DEVOP1] Alert Telemetry Test",
        body=message_body,
        original_recipient="devops-team@company.internal"
    )
