#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import subprocess

workspace = r"c:\Users\lanfr144\Documents\DEVOP1\antigravity\DEVOP1"

def check():
    unsmudged = []
    try:
        # Run git ls-files to get all tracked files
        cmd = ["git", "ls-files"]
        tracked_files = subprocess.check_output(cmd, cwd=workspace, stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore').splitlines()
    except Exception as e:
        print(f"Error getting tracked files: {e}")
        return

    for rel_path in tracked_files:
        filepath = os.path.join(workspace, rel_path)
        try:
            if not os.path.isfile(filepath):
                continue
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            lines = content.splitlines()
            if not lines:
                continue
                
            # Look for format tag in the first two lines (due to shebang compatibility)
            has_tag = False
            tag_line = ""
            for line in lines[:2]:
                if '$Format:' in line:
                    has_tag = True
                    tag_line = line
                    break
                    
            if has_tag:
                # Check if it contains unexpanded placeholders in the tag line
                if '%an' in tag_line or '%ae' in tag_line or '%ad' in tag_line:
                    unsmudged.append(rel_path)
        except Exception:
            pass
            
    print(f"Found {len(unsmudged)} files with unexpanded format headers:")
    for u in unsmudged:
        print(u)

if __name__ == "__main__":
    check()
