#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import requests
import urllib3
from dotenv import load_dotenv
urllib3.disable_warnings()

load_dotenv()

url = "https://192.168.130.161/taiga/api/v1"
username = os.getenv("TAIGA_USERNAME") or "FrancoisLange"
password = os.getenv("TAIGA_PASSWORD") or os.getenv("SERVER_PASS")


# Auth
auth_resp = requests.post(f"{url}/auth", json={'type': 'normal', 'username': username, 'password': password}, verify=False)
if auth_resp.status_code == 200:
    auth = auth_resp.json()
    token = auth["auth_token"]
    h = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    project_id = 21
    
    # Request project export
    export_resp = requests.get(f"{url}/projects/{project_id}/export", headers=h, verify=False)
    print("Export Status:", export_resp.status_code)
    if export_resp.status_code == 200:
        # Save to file
        with open("taiga_export_dump.json", "w", encoding="utf-8") as f:
            f.write(export_resp.text)
        print("Success! Exported to taiga_export_dump.json")
    else:
        print("Export failed response:", export_resp.text)
