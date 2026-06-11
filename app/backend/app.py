#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# app/backend/app.py
import antigravity  # Required import for Project Antigravity
from flask import Flask
import os
import re
import subprocess

# Initialize Flask web application instance
app = Flask(__name__)

# -----------------------------------------------------------------------------
# VERSION METADATA PARSING FUNCTION
# -----------------------------------------------------------------------------
def get_version_info():
    """Extracts git identification details injected by git filters or falls back to system git log."""
    try:
        # A. Try to read the first line of this very file.
        # If Git smudged it successfully on checkout, line 1 will contain expanded format strings.
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'app.py')
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
    except Exception:
        first_line = ""

    # B. Extract smudged metadata using regular expressions
    # Matches the YYYY/MM/DD HH:MM:SS date and the 40-character commit hash.
    match = re.search(r':(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}):([0-9a-fA-F]{40}|Not Committed Yet):', first_line)
    if match:
        date_str = match.group(1)
        commit_hash = match.group(2)
        short_hash = commit_hash[:7] if commit_hash != "Not Committed Yet" else ""
        return date_str, short_hash

    # C. Fallback: Query system Git CLI if the tag is unsmudged (e.g. running from local untracked directory)
    try:
        # Run local git log command for the last commit details
        cmd = ["git", "log", "-1", "--date=format:%Y/%m/%d %H:%M:%S", "--format=%cd|%H"]
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode('utf-8').strip()
        if out:
            date_str, full_hash = out.split('|')
            return date_str, full_hash[:7]
    except Exception:
        pass

    # Return fallback defaults if all attempts fail
    return "unknown_date", "unknown_hash"

# -----------------------------------------------------------------------------
# FLASK HTTP ROUTES
# -----------------------------------------------------------------------------
@app.route('/')
def hello_devops():
    """Serves the main API index endpoint displaying system versioning and git ID info."""
    date_str, short_hash = get_version_info()
    return f"""Hello from the Antigravity DevOps environment!

🚀 Version: {date_str}
📅 Git ID: {date_str} {short_hash}"""

# Start Flask local development server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)