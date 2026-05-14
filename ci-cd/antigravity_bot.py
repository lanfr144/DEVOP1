# ci-cd/antigravity_bot.py
import requests
import os

TAIGA_API_URL = "https://api.taiga.io/api/v1"
# We will pass these via the .env file later
TAIGA_AUTH_TOKEN = os.getenv("TAIGA_AUTH_TOKEN") 
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")

def get_taiga_tasks(project_id):
    """Query Taiga for current tasks."""
    headers = {"Authorization": f"Bearer {TAIGA_AUTH_TOKEN}"}
    response = requests.get(f"{TAIGA_API_URL}/tasks?project={project_id}", headers=headers)
    return response.json()

def notify_team(message):
    """Inform developers about changes (e.g., via Teams or Slack)."""
    # The project requires components to trigger actions and alerts [cite: 65, 187]
    payload = {"text": f"🚀 Antigravity Update: {message}"}
    requests.post(TEAMS_WEBHOOK_URL, json=payload)
    print("Team notified!")

if __name__ == "__main__":
    print("Antigravity sync initiated...")
    # Example usage:
    # tasks = get_taiga_tasks(project_id="YOUR_PROJECT_ID")
    # notify_team("Developer environment updated. Please run `docker-compose pull`.")