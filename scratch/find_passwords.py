#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# scratch/find_passwords.py
import os

workspace = r"c:\Users\lanfr144\Documents\DEVOP1\antigravity\DEVOP1"

def load_env_targets():
    """Parses .env to dynamically extract passwords and webhook URLs to search for."""
    env_path = os.path.join(workspace, ".env")
    passwords = []
    hooks = []
    
    if not os.path.exists(env_path):
        print(f"Error: .env not found at {env_path}")
        return passwords, hooks
        
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, val = line.split('=', 1)
                key = key.strip()
                val = val.strip()
                
                # Check for password patterns
                if any(suffix in key for suffix in ["PASS", "PASSWORD", "AUTHKEY", "PRIVKEY"]):
                    if val and val not in passwords:
                        passwords.append(val)
                # Check for hook/URL patterns
                elif any(suffix in key for suffix in ["WEBHOOK", "URL"]):
                    # Ignore generic/non-secret variables
                    if val and "http" in val and val not in hooks:
                        hooks.append(val)
                        
    return passwords, hooks

def search():
    passwords, hooks = load_env_targets()
    targets = passwords + hooks
    print(f"Loaded passwords to search: {passwords}")
    print(f"Loaded webhooks to search: {hooks}")
    
    IGNORE_DIRS = {".git", ".venv", "node_modules", "logs", ".gemini", ".vscode", "app/logs"}
    IGNORE_FILES = {".env", ".env.example", "DEVOP1"}

    results = []
    for root, dirs, files in os.walk(workspace):
        rel_root = os.path.relpath(root, workspace)
        if any(ignored in rel_root.replace('\\', '/').split('/') for ignored in IGNORE_DIRS):
            continue
        
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if file in IGNORE_FILES:
                continue
            
            filepath = os.path.join(root, file)
            try:
                if os.path.islink(filepath) or not os.path.isfile(filepath):
                    continue
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for target in targets:
                        if target in content:
                            f.seek(0)
                            for idx, line in enumerate(f, 1):
                                if target in line:
                                    results.append((os.path.relpath(filepath, workspace), idx, target, line.strip()))
            except Exception:
                pass
                
    print(f"\nFound {len(results)} occurrences of target passwords/hooks in codebase:")
    for filepath, line_num, target, line_content in results:
        print(f"{filepath}:{line_num} - Found '{target}' - {line_content}")

if __name__ == "__main__":
    search()
