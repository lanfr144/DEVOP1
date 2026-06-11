#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# app/backend/app.py
import antigravity  # Requirement fulfilled!
from flask import Flask
import os
import re
import subprocess

app = Flask(__name__)

def get_version_info():
    # Try to parse from the first line of this file (which Git smudges)
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'app.py')
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
    except Exception:
        first_line = ""

    match = re.search(r'\$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$', first_line)
    if match:
        parts = match.group(1).split(':')
        if len(parts) >= 9 and not parts[0].startswith('%an'):
            date_str = parts[2]
            commit_hash = parts[6]
            short_hash = commit_hash[:7] if commit_hash else ""
            return date_str, short_hash

    # Fallback to local Git if not smudged
    try:
        cmd = ["git", "log", "-1", "--date=format:%Y/%m/%d %H:%M:%S", "--format=%ad|%H"]
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode('utf-8').strip()
        if out:
            date_str, full_hash = out.split('|')
            return date_str, full_hash[:7]
    except Exception:
        pass

    return "unknown_date", "unknown_hash"

@app.route('/')
def hello_devops():
    date_str, short_hash = get_version_info()
    return f"""Hello from the Antigravity DevOps environment!

🚀 Version: {date_str}
📅 Git ID: {date_str} {short_hash}"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)