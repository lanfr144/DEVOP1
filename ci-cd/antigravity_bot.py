#ident @(#)$Format:PROJECT_NAME:FILE_NAME:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$
import os
import argparse
import requests
import yaml
import sys
from dotenv import load_dotenv

# Load local environment configuration
load_dotenv()

# Taiga API Configuration
TAIGA_API_URL = "https://api.taiga.io/api/v1"
TAIGA_USERNAME = os.getenv("TAIGA_USERNAME")
TAIGA_PASSWORD = os.getenv("TAIGA_PASSWORD")
PROJECT_ID = os.getenv("TAIGA_PROJECT_ID")

def authenticate_taiga():
    """Authenticates with Taiga using Username/Password and returns the auth token."""
    print("🔐 Authenticating with Taiga...")
    payload = {
        "type": "normal",
        "username": TAIGA_USERNAME,
        "password": TAIGA_PASSWORD
    }
    
    try:
        response = requests.post(f"{TAIGA_API_URL}/auth", json=payload)
        response.raise_for_status()
        token = response.json().get("auth_token")
        print("✅ Authentication successful!")
        return token
    except requests.exceptions.RequestException as e:
        print(f"❌ Authentication failed: {e}")
        sys.exit(1)

def get_headers(token):
    """Returns the authorization headers needed for API calls."""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def get_existing_milestones(headers):
    response = requests.get(f"{TAIGA_API_URL}/milestones?project={PROJECT_ID}", headers=headers)
    response.raise_for_status()
    return {m["name"]: m["id"] for m in response.json()}

def get_existing_user_stories(headers):
    response = requests.get(f"{TAIGA_API_URL}/userstories?project={PROJECT_ID}", headers=headers)
    response.raise_for_status()
    return {us["subject"]: us["id"] for us in response.json()}

def get_existing_tasks(headers):
    response = requests.get(f"{TAIGA_API_URL}/tasks?project={PROJECT_ID}", headers=headers)
    response.raise_for_status()
    return {t["subject"]: t["id"] for t in response.json()}

def create_taiga_milestone(name, headers):
    """Creates a Sprint (Milestone) in Taiga."""
    payload = {
        "name": name,
        "project": PROJECT_ID,
        "estimated_start": "2024-01-01", 
        "estimated_finish": "2026-06-24"
    }
    response = requests.post(f"{TAIGA_API_URL}/milestones", json=payload, headers=headers)
    if not response.ok:
        print(f"Taiga API Error: {response.text}")
    response.raise_for_status()
    return response.json()["id"]

def create_taiga_user_story(title, milestone_id, headers):
    """Creates a User Story and assigns it to a Sprint."""
    payload = {
        "subject": title,
        "project": PROJECT_ID,
        "milestone": milestone_id
    }
    response = requests.post(f"{TAIGA_API_URL}/userstories", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["id"]

def create_taiga_task(subject, user_story_id, headers):
    """Creates a Task under a specific User Story."""
    payload = {
        "subject": subject,
        "project": PROJECT_ID,
        "user_story": user_story_id
    }
    response = requests.post(f"{TAIGA_API_URL}/tasks", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["id"]

def populate_taiga(yaml_file):
    """Parses the YAML file and populates the Taiga project idempotently."""
    print(f"🚀 Antigravity Sequence Initiated. Reading {yaml_file}...")
    
    token = authenticate_taiga()
    headers = get_headers(token)
    
    print("🔄 Fetching existing Taiga data to prevent duplicates...")
    existing_milestones = get_existing_milestones(headers)
    existing_stories = get_existing_user_stories(headers)
    existing_tasks = get_existing_tasks(headers)
    
    with open(yaml_file, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        
    for sprint in data.get('sprints', []):
        name = sprint['name']
        if name in existing_milestones:
            print(f"\n⏭️  Skipping existing Sprint: {name}")
            milestone_id = existing_milestones[name]
        else:
            print(f"\n🆕 Creating Sprint: {name}")
            milestone_id = create_taiga_milestone(name, headers)
            existing_milestones[name] = milestone_id
            
        for story in sprint.get('user_stories', []):
            title = story['title']
            if title in existing_stories:
                print(f"  -> ⏭️  Skipping existing User Story: {title}")
                story_id = existing_stories[title]
            else:
                print(f"  -> 🆕 Creating User Story: {title}")
                story_id = create_taiga_user_story(title, milestone_id, headers)
                existing_stories[title] = story_id
                
            for task in story.get('tasks', []):
                if task in existing_tasks:
                    print(f"      -> ⏭️  Skipping existing Task: {task}")
                else:
                    print(f"      -> 🆕 Creating Task: {task}")
                    create_taiga_task(task, story_id, headers)
                    existing_tasks[task] = True

    print("\n✅ Taiga population complete! All Sprints, Stories, and Tasks are live.")

if __name__ == "__main__":
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(description="Antigravity DevOps Automation")
    parser.add_argument("--populate", help="Path to the YAML file to populate Taiga", type=str)
    args = parser.parse_args()

    if args.populate:
        if not TAIGA_USERNAME or not TAIGA_PASSWORD or not PROJECT_ID:
            print("❌ Error: Missing TAIGA_USERNAME, TAIGA_PASSWORD, or TAIGA_PROJECT_ID in environment.")
        else:
            populate_taiga(args.populate)
    else:
        print("Antigravity engine idle. Use --populate <file.yml> to run.")
