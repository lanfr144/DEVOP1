import os
import sys

REPLACEMENTS = [
    ("your_discord_webhook_url_here", "your_discord_webhook_url_here"),
    ("your_discord_channel_url_here", "your_discord_channel_url_here"),
    ("your_teams_webhook_url_here", "your_teams_webhook_url_here"),
    ("mysql://dev_user:your_password_here@localhost:4306/devop1_db", "mysql://dev_user:your_password_here@localhost:4306/devop1_db"),
    ("mysql://xau:your_password_here@localhost:4306/xau", "mysql://xau:your_password_here@localhost:4306/xau"),
    ("your_email_password_here", "your_email_password_here"),
    ("your_email@example.com", "your_email@example.com"),
    ("your_authkey_here", "your_authkey_here"),
    ("your_privkey_here", "your_privkey_here"),
    ("your_taiga_password_here", "your_taiga_password_here"),
    ("your_db_password_here", "your_db_password_here"),
    ("your_windows_user_here", "your_windows_user_here"),
    ("your_username_here", "your_username_here"),
    ("your_admin_user_here", "your_admin_user_here")
]

def main():
    # Replace sensitive values in all tracked files except inside .git
    for root, dirs, files in os.walk('.'):
        if '.git' in root.split(os.sep):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            # Skip python virtual environments, binaries, or local environment configurations
            if 'venv' in file_path or '.venv' in file_path or file == '.env' or file.startswith('.env.') or file.endswith(('.png', '.ttf', '.tar', '.gz', '.pdf')):
                continue
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                changed = False
                for target, replacement in REPLACEMENTS:
                    if target in content:
                        content = content.replace(target, replacement)
                        changed = True
                
                if changed:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
            except Exception:
                pass

if __name__ == '__main__':
    main()
