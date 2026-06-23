#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os

IGNORE_DIRS = {".git", ".venv", "node_modules", "logs", ".gemini", ".vscode", "app/logs"}
IGNORE_FILES = {".env", ".env.example", "DEVOP1"}

workspace = r"c:\Users\your_windows_user_here\Documents\DEVOP1\antigravity\DEVOP1"

def check():
    missing = []
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
                    if 'Format:LocalFoodAI:app.py' not in content:
                        missing.append(os.path.relpath(filepath, workspace))
            except Exception:
                pass
                
    print(f"Found {len(missing)} files missing the header comment:")
    for m in missing:
        print(m)

if __name__ == "__main__":
    check()
