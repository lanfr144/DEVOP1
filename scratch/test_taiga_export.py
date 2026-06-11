#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import requests
import json
import urllib3
from dotenv import load_dotenv
urllib3.disable_warnings()

load_dotenv()

url = "https://192.168.130.161/taiga/api/v1"
username = os.getenv("TAIGA_USERNAME") or "FrancoisLange"
password = os.getenv("TAIGA_PASSWORD") or os.getenv("SERVER_PASS")


# Auth
auth_resp = requests.post(f"{url}/auth", json={'type': 'normal', 'username': username, 'password': password}, verify=False)
print("Auth:", auth_resp.status_code)
if auth_resp.status_code == 200:
    auth = auth_resp.json()
    token = auth["auth_token"]
    h = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    project_id = 21
    
    # Fetch user stories
    us = requests.get(f"{url}/userstories?project={project_id}", headers=h, verify=False).json()
    print("User Stories Count:", len(us))
    
    # Fetch milestones
    ms = requests.get(f"{url}/milestones?project={project_id}", headers=h, verify=False).json()
    print("Milestones Count:", len(ms))
    
    # Fetch tasks
    tasks = requests.get(f"{url}/tasks?project={project_id}", headers=h, verify=False).json()
    print("Tasks Count:", len(tasks))
