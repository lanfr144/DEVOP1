#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import requests
import json
import os
from datetime import datetime
import sys
from dotenv import load_dotenv

# Try to load env variables from project root
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Import Zabbix utility
try:
    from zabbix_utils import send_to_zabbix
except ImportError:
    # Fallback if run from parent dir without path modifications
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from zabbix_utils import send_to_zabbix

# Configuration
COOKIE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "session_cookies.json")
SITE = "https://www.spuerkeess.lu"
URL = SITE + "/fr/particuliers/epargner-investir/metaux-precieux/?action=ajax"
file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "metaux-precieux_" + (datetime.now().strftime("%Y%m%d_%H%M%S")))
session = requests.Session()

# Load cookies from file if they exist
if os.path.exists(COOKIE_FILE):
    with open(COOKIE_FILE, "r") as f:
        cookies_dict = json.load(f)
        session.cookies.update(cookies_dict)
else:
    # Initial setup using your provided values
    initial_cookies = {
        "dtCookie": "v_4_srv_4_sn_8B04893EB88646AD8E7D76F5A81E7AC4_app-3Ac0d4ef991776b9df_1_ol_0_perc_100000_mul_1",
        "BIGipServer~BCEE~PS-1141LBP28": "rd1141o00000000000000000000ffffc0a8162do80",
        "TS012a5450": "01166c61636f1eaa0b4ec0df16633c46713698785de6f416ecb7de61c75f5f539a28bfeb2f3c02430becbfedab7a4dc0f33e8851ac",
        "TS019193e9": "01166c61631dd9270d3b97e228bbac62082ea34410dddab18d996ea1e32bbb59e3be3bd52a3faa134adb4768eeeb46a07c24d56cd6",
        "dtPC": "4$210847492_817h2vDEPMKRGVCALELWCVDFRKEMHCMRHRHFHC-0e0",
        "rxvt": "1767212647667|1767210651399",
        "dtSa": "-",
        "rxVisitor": "1735820566471GVFEMETL7KBGACE09T59DR69LT8JU1IK",
        "stg_last_interaction": "Wed, 31 Dec 2025 19:52:03 GMT",
        "_pk_id.146e6c83-9e24-4651-81ea-c8e6a32ac132.aeaa": "8b819e0c290ab56e.1767210654.1.1767210654.1767210654.",
        "_pk_ses.146e6c83-9e24-4651-81ea-c8e6a32ac132.aeaa": "*"
    }
    session.cookies.update(initial_cookies)

# Define Headers and Multipart Data
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
    "Accept": "*/*",
    "x-dtpc": "4$210847492_817h2vDEPMKRGVCALELWCVDFRKEMHCMRHRHFHC-0e0"
}

data = {
    "formKey": (None, "precious.metal.filter"),
    "types": (None, "102,103,106,77,80,78,79,308,73,188,241,99,114,76,85,200"),
    "precious-metal-list-page": (None, "0"),
    "sorting": (None, "bcee")
}

# Execute Request
try:
    response = session.post(URL, headers=headers, files=data)
    response.raise_for_status()
    
    # Save updated cookies back to the file for the next run
    with open(COOKIE_FILE, "w") as f:
        json.dump(requests.utils.dict_from_cookiejar(session.cookies), f)
    
    json_class = json.loads(response.text.replace('"image":"','"image":"' + SITE ))
    
    output_filename = file_name + ".json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(json_class, f, indent=4)
        
    print(f"Request successful. Data saved to {output_filename}")
    send_to_zabbix("xau.trace", f"get_gold_price succeeded: {os.path.basename(output_filename)} created.")
    sys.exit(0)
    
except Exception as e:
    error_msg = f"get_gold_price failed: {str(e)}"
    sys.stderr.write(error_msg + "\n")
    send_to_zabbix("xau.error", error_msg)
    sys.exit(1)
