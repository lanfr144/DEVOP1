#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# local_tools/find_ghost_files.py
import os
import subprocess
import sys

# -----------------------------------------------------------------------------
# STEP 1: DEFINE ROOT DIRECTORY AND PATHS
# -----------------------------------------------------------------------------
workspace = r"c:\Users\lanfr144\Documents\DEVOP1\antigravity\DEVOP1"
report_path = os.path.join(workspace, "docs", "GHOST_FILES_REPORT.md")

# -----------------------------------------------------------------------------
# STEP 2: SCANNING LOGIC FOR GHOST FILES
# -----------------------------------------------------------------------------
def scan_ghost_files():
    """Scans the repository to identify untracked, ignored, temporary, or unused files."""
    print("[INFO] Starting Ghost File Scan...")
    
    untracked_files = []
    ignored_backups = []
    broken_symlinks = []
    empty_directories = []
    
    # A. Retrieve untracked files via Git CLI
    try:
        out = subprocess.check_output(["git", "status", "--porcelain"], stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore')
        for line in out.splitlines():
            if line.startswith("?? "):
                file_rel = line[3:].strip()
                untracked_files.append(file_rel)
    except Exception as e:
        print(f"[WARNING] Could not execute git status: {e}")

    # B. Walk filesystem to inspect files for backup extensions, empty folders, and reparse points
    for root, dirs, files in os.walk(workspace):
        # Skip git metadata directory
        if ".git" in root.split(os.sep):
            continue
            
        # Check if directories are empty (unused placeholders)
        for d in dirs:
            dir_full = os.path.join(root, d)
            if d in [".git", "venv", ".venv", "node_modules"]:
                continue
            try:
                if not os.listdir(dir_full):
                    rel_dir = os.path.relpath(dir_full, workspace)
                    empty_directories.append(rel_dir)
            except Exception:
                pass

        # Check files for backup extensions or broken symlinks
        for f in files:
            file_full = os.path.join(root, f)
            rel_file = os.path.relpath(file_full, workspace)
            
            # Identify backup files by extension
            if f.endswith((".wbk", ".docx", ".bak", ".tmp", ".old")):
                ignored_backups.append(rel_file)
                
            # Check for broken symlinks
            try:
                if os.path.islink(file_full):
                    if not os.path.exists(file_full) or os.path.getsize(file_full) == 0:
                        broken_symlinks.append(rel_file)
            except Exception:
                pass

        # Check directories that are symlinks/reparse points
        for d in dirs:
            dir_full = os.path.join(root, d)
            rel_dir = os.path.relpath(dir_full, workspace)
            try:
                if os.path.islink(dir_full):
                    if not os.path.exists(dir_full):
                        broken_symlinks.append(rel_dir)
            except Exception:
                pass

    # Ensure the root 'DEVOP1' link is cataloged if it acts as a loop/reparse point
    root_devop1 = os.path.join(workspace, "DEVOP1")
    if os.path.exists(root_devop1) and "DEVOP1" not in broken_symlinks:
        try:
            attrs = subprocess.check_output(f'powershell -Command "(Get-Item \'{root_devop1}\').Attributes"', shell=True).decode().strip()
            if "ReparsePoint" in attrs:
                broken_symlinks.append("DEVOP1")
        except Exception:
            pass

    # C. Compile the Markdown Report
    print(f"[INFO] Compiling report and saving to {report_path}...")
    
    report_content = f"""#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Ghost and Unused Files Audit Report

This report identifies ghost files, unused folders, and backup files detected inside the repository.

## 1. Summary of Findings

| Category | Count | Description |
| :--- | :--- | :--- |
| **Untracked Stale Files** | {len(untracked_files)} | Files in the workspace directory not tracked by Git. |
| **Ignored Backup Files** | {len(ignored_backups)} | Files matching ignore rules or backup extensions (e.g. `.wbk` / `.docx`). |
| **Broken Symlinks / Reparse Points** | {len(broken_symlinks)} | Reparse points with missing targets or size 0. |
| **Empty / Unused Placeholders** | {len(empty_directories)} | Directories containing no files. |

---

## 2. Detailed Breakdown

### ⚠️ Untracked Stale Files
These files exist in the repository but have not been added to Git tracking.
{chr(10).join([f"- `{f}`" for f in untracked_files]) if untracked_files else "*None found.*"}

### 📂 Ignored Backup/Temp Files
These backup or Word documents represent unused documentation or duplicate files.
{chr(10).join([f"- `{f}`" for f in ignored_backups]) if ignored_backups else "*None found.*"}

### 🔗 Broken Symlinks / Reparse Points
Reparse points pointing to non-existent pathways, representing dead loops.
{chr(10).join([f"- `{f}`" for f in broken_symlinks]) if broken_symlinks else "*None found.*"}

### 📁 Empty/Unused Directory Placeholders
Directories that do not contain any files or active modules.
{chr(10).join([f"- `{f}`" for f in empty_directories]) if empty_directories else "*None found.*"}

---

## 3. Recommendations & Action Plan

1. **Delete Stale/Broken Reparse Points**: Remove the root `DEVOP1` reparse point to prevent shell looping or backup failures.
2. **Purge Ignored Document Backups**: The `.wbk` backup file under `documentation/` can be safely deleted. Keep `DEVOP1 - Project terms.docx` only if it represents the primary requirement sheet.
3. **Manage Empty Folders**: Keep empty placeholder directories like `app/dags` and `app/plugins` only if Apache Airflow requires them structurally. Otherwise, remove them to keep the directory tree clean.
"""

    # Ensure parent docs directory exists
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print("[SUCCESS] Ghost file audit report generated successfully!")

if __name__ == "__main__":
    scan_ghost_files()
