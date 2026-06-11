#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import argparse
import requests
import yaml
import sys
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# STEP 1: LOAD ENVIRONMENT CONFIGURATION
# -----------------------------------------------------------------------------
# Read keys from local .env config
load_dotenv()

TAIGA_API_URL = "https://api.taiga.io/api/v1"
TAIGA_USERNAME = os.getenv("TAIGA_USERNAME")
TAIGA_PASSWORD = os.getenv("TAIGA_PASSWORD")
PROJECT_ID = os.getenv("TAIGA_PROJECT_ID")

# -----------------------------------------------------------------------------
# STEP 2: AUTHENTICATE WITH TAIGA API
# -----------------------------------------------------------------------------
def authenticate_taiga():
    """Sends credentials to Taiga authentication endpoint and obtains token."""
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

# -----------------------------------------------------------------------------
# STEP 3: API REQUEST HEADERS GENERATOR
# -----------------------------------------------------------------------------
def get_headers(token):
    """Formats standard HTTP headers with bearer auth token."""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

# -----------------------------------------------------------------------------
# STEP 4: FETCH EXISTING TAIGA INFRASTRUCTURE DATA
# -----------------------------------------------------------------------------
def get_existing_milestones(headers):
    """Fetches all existing sprints (milestones) for the project to prevent duplicates."""
    response = requests.get(f"{TAIGA_API_URL}/milestones?project={PROJECT_ID}", headers=headers)
    response.raise_for_status()
    # Returns a dictionary mapping sprint name to its ID
    return {m["name"]: m["id"] for m in response.json()}

def get_existing_user_stories(headers):
    """Fetches all user stories for the project to prevent duplicates."""
    response = requests.get(f"{TAIGA_API_URL}/userstories?project={PROJECT_ID}", headers=headers)
    response.raise_for_status()
    # Returns a dictionary mapping user story subject to its ID
    return {us["subject"]: us["id"] for us in response.json()}

def get_existing_tasks(headers):
    """Fetches all tasks in the project to prevent duplicates."""
    response = requests.get(f"{TAIGA_API_URL}/tasks?project={PROJECT_ID}", headers=headers)
    response.raise_for_status()
    # Returns a dictionary mapping task subject to its ID
    return {t["subject"]: t["id"] for t in response.json()}

# -----------------------------------------------------------------------------
# STEP 5: CREATE TAIGA ENTITIES (Idempotent helpers)
# -----------------------------------------------------------------------------
def create_taiga_milestone(name, headers):
    """Invokes Taiga API POST command to create a new Sprint (Milestone)."""
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
    """Invokes Taiga API POST command to create a new User Story inside a Sprint."""
    payload = {
        "subject": title,
        "project": PROJECT_ID,
        "milestone": milestone_id
    }
    response = requests.post(f"{TAIGA_API_URL}/userstories", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["id"]

def create_taiga_task(subject, user_story_id, headers):
    """Invokes Taiga API POST command to create a new Task nested under a User Story."""
    payload = {
        "subject": subject,
        "project": PROJECT_ID,
        "user_story": user_story_id
    }
    response = requests.post(f"{TAIGA_API_URL}/tasks", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["id"]

# -----------------------------------------------------------------------------
# STEP 6: YAML PARSING AND TAIGA POPULATION DRIVER
# -----------------------------------------------------------------------------
def populate_taiga(yaml_file):
    """Reads project sprints/stories/tasks definition YAML and populates Taiga idempotently."""
    print(f"🚀 Antigravity Sequence Initiated. Reading {yaml_file}...")
    
    token = authenticate_taiga()
    headers = get_headers(token)
    
    print("🔄 Fetching existing Taiga data to prevent duplicates...")
    existing_milestones = get_existing_milestones(headers)
    existing_stories = get_existing_user_stories(headers)
    existing_tasks = get_existing_tasks(headers)
    
    # Load and parse yml data structure
    with open(yaml_file, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        
    # Iterate through milestones (sprints) in the parsed YAML
    for sprint in data.get('sprints', []):
        name = sprint['name']
        if name in existing_milestones:
            print(f"\n⏭️  Skipping existing Sprint: {name}")
            milestone_id = existing_milestones[name]
        else:
            print(f"\n🆕 Creating Sprint: {name}")
            milestone_id = create_taiga_milestone(name, headers)
            existing_milestones[name] = milestone_id
            
        # Iterate user stories within the sprint
        for story in sprint.get('user_stories', []):
            title = story['title']
            if title in existing_stories:
                print(f"  -> ⏭️  Skipping existing User Story: {title}")
                story_id = existing_stories[title]
            else:
                print(f"  -> 🆕 Creating User Story: {title}")
                story_id = create_taiga_user_story(title, milestone_id, headers)
                existing_stories[title] = story_id
                
            # Iterate tasks nested under the user story
            for task in story.get('tasks', []):
                if task in existing_tasks:
                    print(f"      -> ⏭️  Skipping existing Task: {task}")
                else:
                    print(f"      -> 🆕 Creating Task: {task}")
                    create_taiga_task(task, story_id, headers)
                    existing_tasks[task] = True

    print("\n✅ Taiga population complete! All Sprints, Stories, and Tasks are live.")

# -----------------------------------------------------------------------------
# STEP 7: WIKI SYNCHRONIZATION FUNCTIONALITY
# -----------------------------------------------------------------------------
def get_existing_wiki_pages(headers):
    """Queries Taiga for all existing wiki pages on the project."""
    response = requests.get(f"{TAIGA_API_URL}/wiki?project={PROJECT_ID}", headers=headers)
    response.raise_for_status()
    # Returns slug mapping to {id, version} for updates
    return {wp["slug"]: {"id": wp["id"], "version": wp["version"]} for wp in response.json()}

def create_wiki_page(slug, content, headers):
    """Sends POST command to create a new Wiki page slug on Taiga."""
    payload = {
        "project": PROJECT_ID,
        "slug": slug,
        "content": content
    }
    response = requests.post(f"{TAIGA_API_URL}/wiki", json=payload, headers=headers)
    if not response.ok:
        print(f"❌ Taiga API Wiki Create Error: {response.text}")
    response.raise_for_status()
    print(f"  -> 🆕 Created Wiki Page: {slug}")

def update_wiki_page(page_id, slug, content, version, headers):
    """Sends PUT command to update an existing Wiki page on Taiga, supplying current version."""
    payload = {
        "project": PROJECT_ID,
        "slug": slug,
        "content": content,
        "version": version
    }
    response = requests.put(f"{TAIGA_API_URL}/wiki/{page_id}", json=payload, headers=headers)
    if not response.ok:
        print(f"❌ Taiga API Wiki Update Error: {response.text}")
    response.raise_for_status()
    print(f"  -> 🔄 Updated Wiki Page: {slug}")

def sync_wiki(wiki_dir):
    """Syncs markdown files in the specified directory to Taiga Wiki pages."""
    print(f"🚀 Taiga Wiki Sync Sequence Initiated. Reading from {wiki_dir}...")
    
    token = authenticate_taiga()
    headers = get_headers(token)
    
    print("🔄 Fetching existing Taiga Wiki pages...")
    existing_wiki = get_existing_wiki_pages(headers)
    
    if not os.path.exists(wiki_dir):
        print(f"❌ Error: Wiki directory does not exist: {wiki_dir}")
        return
        
    # Process all markdown files in target directory
    for filename in os.listdir(wiki_dir):
        if not filename.endswith(".md"):
            continue
            
        file_path = os.path.join(wiki_dir, filename)
        if not os.path.isfile(file_path):
            continue
            
        # Standardize slug (home page uses 'home', others use file basename)
        name_without_ext = os.path.splitext(filename)[0]
        if name_without_ext == "wiki_content":
            slug = "home"
        else:
            slug = name_without_ext
            
        print(f"\nProcessing wiki file: {filename} (slug: {slug})")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # If slug page exists, update it. Otherwise, create it.
        if slug in existing_wiki:
            page_info = existing_wiki[slug]
            update_wiki_page(page_info["id"], slug, content, page_info["version"], headers)
        else:
            create_wiki_page(slug, content, headers)
            
    print("\n✅ Taiga Wiki sync complete!")

# -----------------------------------------------------------------------------
# STEP 8: ARGUMENT PARSING AND SCRIPT ROUTING
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Ensure stdout handles UTF-8 correctly
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(description="Antigravity DevOps Automation")
    parser.add_argument("--populate", help="Path to the YAML file to populate Taiga", type=str)
    parser.add_argument("--wiki", help="Path to the directory containing markdown wiki files", type=str)
    args = parser.parse_args()

    # Route execution based on CLI parameters
    if args.populate:
        if not TAIGA_USERNAME or not TAIGA_PASSWORD or not PROJECT_ID:
            print("❌ Error: Missing TAIGA_USERNAME, TAIGA_PASSWORD, or TAIGA_PROJECT_ID in environment.")
        else:
            populate_taiga(args.populate)
    elif args.wiki:
        if not TAIGA_USERNAME or not TAIGA_PASSWORD or not PROJECT_ID:
            print("❌ Error: Missing TAIGA_USERNAME, TAIGA_PASSWORD, or TAIGA_PROJECT_ID in environment.")
        else:
            sync_wiki(args.wiki)
    else:
        print("Antigravity engine idle. Use --populate <file.yml> or --wiki <dir> to run.")