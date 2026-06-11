#!/usr/bin/env python
#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import requests
import json
import sys
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# STEP 1: LOAD ENVIRONMENT CONFIGURATION
# -----------------------------------------------------------------------------
# Reads local .env parameters to get Taiga authentication and project info.
load_dotenv()

TAIGA_API_URL = "https://api.taiga.io/api/v1"
TAIGA_USERNAME = os.getenv("TAIGA_USERNAME")
TAIGA_PASSWORD = os.getenv("TAIGA_PASSWORD")
PROJECT_ID = os.getenv("TAIGA_PROJECT_ID")

# -----------------------------------------------------------------------------
# STEP 2: TAIGA API AUTHENTICATION FUNCTION
# -----------------------------------------------------------------------------
def authenticate_taiga():
    """Authenticates with the Taiga REST API using normal credential payload."""
    print("[INFO] Authenticating with Taiga...")
    payload = {
        "type": "normal",
        "username": TAIGA_USERNAME,
        "password": TAIGA_PASSWORD
    }
    # Send a POST request to /auth endpoint
    response = requests.post(f"{TAIGA_API_URL}/auth", json=payload)
    response.raise_for_status() # Raise exception for HTTP error statuses
    return response.json().get("auth_token")

# -----------------------------------------------------------------------------
# STEP 3: API HEADER GENERATOR
# -----------------------------------------------------------------------------
def get_headers(token):
    """Generates standard request headers with bearer token authorization."""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

# -----------------------------------------------------------------------------
# STEP 4: MAIN PROJECT CLOSURE AND EXPORT LOGIC
# -----------------------------------------------------------------------------
def main():
    # Verify environment has all credentials needed
    if not TAIGA_USERNAME or not TAIGA_PASSWORD or not PROJECT_ID:
        print("[ERROR] Missing Taiga credentials in .env")
        sys.exit(1)

    # Perform authentication and build requests header
    token = authenticate_taiga()
    headers = get_headers(token)

    # A. Retrieve all User Stories to locate the target one
    print("[INFO] Fetching user stories...")
    r = requests.get(f"{TAIGA_API_URL}/userstories?project={PROJECT_ID}&page_size=100", headers=headers)
    r.raise_for_status()
    user_stories = r.json()
    
    target_us_id = None
    target_subject = "As a team, we need enhanced communication and documentation."
    
    # Locate the ID of the documentation user story
    for us in user_stories:
        if us["subject"] == target_subject:
            target_us_id = us["id"]
            break
            
    # Fallback to avoid crashes if the target story wasn't found
    if not target_us_id and user_stories:
        target_us_id = user_stories[0]["id"]
        print(f"[WARNING] Target story not found. Using fallback story ID: {target_us_id}")
    elif not target_us_id:
        print("[ERROR] No user stories found in the project.")
        sys.exit(1)
    else:
        print(f"[INFO] Found target user story ID: {target_us_id}")

    # B. Create the documentation task if it doesn't exist yet
    task_subject = "Create skill directory setup and configuration guide"
    
    # Retrieve all tasks to check for duplication
    print("[INFO] Checking if documentation task already exists...")
    r = requests.get(f"{TAIGA_API_URL}/tasks?project={PROJECT_ID}&page_size=100", headers=headers)
    r.raise_for_status()
    tasks = r.json()
    
    task_exists = False
    for t in tasks:
        if t["subject"] == task_subject:
            task_exists = True
            break
            
    # If the task doesn't exist, create it dynamically
    if not task_exists:
        print(f"[INFO] Creating task: '{task_subject}'...")
        task_payload = {
            "subject": task_subject,
            "project": int(PROJECT_ID),
            "user_story": target_us_id
        }
        r = requests.post(f"{TAIGA_API_URL}/tasks", json=task_payload, headers=headers)
        r.raise_for_status()
        print("[SUCCESS] Task created successfully!")
        
        # Re-fetch tasks list to include the newly created one in subsequent iterations
        r = requests.get(f"{TAIGA_API_URL}/tasks?project={PROJECT_ID}&page_size=100", headers=headers)
        r.raise_for_status()
        tasks = r.json()
    else:
        print("[INFO] Documentation task already exists.")

    # C. Fetch and close all tasks (Task closed status ID: 8901961)
    print(f"[INFO] Closing {len(tasks)} tasks...")
    for t in tasks:
        tid = t["id"]
        # Skip if already closed
        if t["status"] == 8901961:
            print(f"  - Task already closed: {t['subject']}")
            continue
        print(f"  - Closing task: {t['subject']} (ID: {tid}, Version: {t.get('version')})")
        # PATCH update to change status to closed
        r = requests.patch(f"{TAIGA_API_URL}/tasks/{tid}", json={"status": 8901961, "version": t["version"]}, headers=headers)
        if not r.ok:
            print(f"[ERROR] Failed to close task {tid}: {r.text}")
        r.raise_for_status()

    # D. Close all User Stories (User story Done status ID: 10832456)
    r = requests.get(f"{TAIGA_API_URL}/userstories?project={PROJECT_ID}&page_size=100", headers=headers)
    r.raise_for_status()
    user_stories = r.json()
    
    print(f"[INFO] Closing {len(user_stories)} user stories...")
    for us in user_stories:
        usid = us["id"]
        if us["status"] == 10832456:
            print(f"  - Story already closed: {us['subject']}")
            continue
        print(f"  - Closing story: {us['subject']} (ID: {usid}, Version: {us.get('version')})")
        # PATCH update to change status to Done
        r = requests.patch(f"{TAIGA_API_URL}/userstories/{usid}", json={"status": 10832456, "version": us["version"]}, headers=headers)
        if not r.ok:
            print(f"[ERROR] Failed to close story {usid}: {r.text}")
        r.raise_for_status()

    # E. Close all Sprints/Milestones
    print("[INFO] Fetching Sprints...")
    r = requests.get(f"{TAIGA_API_URL}/milestones?project={PROJECT_ID}&page_size=100", headers=headers)
    r.raise_for_status()
    milestones = r.json()

    print(f"[INFO] Closing {len(milestones)} milestones...")
    for m in milestones:
        mid = m["id"]
        if m["closed"]:
            print(f"  - Milestone already closed: {m['name']}")
            continue
        print(f"  - Closing milestone: {m['name']} (ID: {mid}, Version: {m.get('version')})")
        # PATCH update to mark closed as true
        r = requests.patch(f"{TAIGA_API_URL}/milestones/{mid}", json={"closed": True, "version": m["version"]}, headers=headers)
        if not r.ok:
            print(f"[ERROR] Failed to close milestone {mid}: {r.text}")
        r.raise_for_status()

    # F. Export final project state to docs/taiga_export.json
    print("[INFO] Fetching final project state for export...")
    
    r = requests.get(f"{TAIGA_API_URL}/milestones?project={PROJECT_ID}&page_size=100", headers=headers)
    final_milestones = r.json()
    
    r = requests.get(f"{TAIGA_API_URL}/userstories?project={PROJECT_ID}&page_size=100", headers=headers)
    final_stories = r.json()
    
    r = requests.get(f"{TAIGA_API_URL}/tasks?project={PROJECT_ID}&page_size=100", headers=headers)
    final_tasks = r.json()

    # Structure the export payload for project records
    export_data = {
        "project_id": PROJECT_ID,
        "sprints": [
            {
                "id": m["id"],
                "name": m["name"],
                "estimated_start": m["estimated_start"],
                "estimated_finish": m["estimated_finish"],
                "closed": m["closed"]
            } for m in final_milestones
        ],
        "user_stories": [
            {
                "id": us["id"],
                "subject": us["subject"],
                "status_id": us["status"],
                "is_closed": us["is_closed"],
                "milestone": us["milestone"]
            } for us in final_stories
        ],
        "tasks": [
            {
                "id": t["id"],
                "subject": t["subject"],
                "status_id": t["status"],
                "is_closed": t["is_closed"],
                "user_story": t["user_story"]
            } for t in final_tasks
        ]
    }

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    export_path = os.path.join(base_dir, "docs", "taiga_export.json")
    
    # Save the structured dict as JSON to disk
    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=4, ensure_ascii=False)

    print(f"\n[SUCCESS] Project closure complete. Saved export to: {export_path}")

if __name__ == "__main__":
    main()