#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Ghost and Unused Files Audit Report

This report identifies ghost files, unused folders, and backup files detected inside the repository.

## 1. Summary of Findings

| Category | Count | Description |
| :--- | :--- | :--- |
| **Untracked Stale Files** | 3 | Files in the workspace directory not tracked by Git. |
| **Ignored Backup Files** | 2 | Files matching ignore rules or backup extensions (e.g. `.wbk` / `.docx`). |
| **Broken Symlinks / Reparse Points** | 0 | Reparse points with missing targets or size 0. |
| **Empty / Unused Placeholders** | 13 | Directories containing no files. |

---

## 2. Detailed Breakdown

### ⚠️ Untracked Stale Files
These files exist in the repository but have not been added to Git tracking.
- `DEVOP1`
- `docs/GHOST_FILES_REPORT.md`
- `local_tools/find_ghost_files.py`

### 📂 Ignored Backup/Temp Files
These backup or Word documents represent unused documentation or duplicate files.
- `documentation\Copie de secours de DEVOP1 - Project terms.wbk`
- `documentation\DEVOP1 - Project terms.docx`

### 🔗 Broken Symlinks / Reparse Points
Reparse points pointing to non-existent pathways, representing dead loops.
*None found.*

### 📁 Empty/Unused Directory Placeholders
Directories that do not contain any files or active modules.
- `app\dags`
- `app\frontend`
- `app\plugins`
- `app\logs\scheduler\2026-05-15`
- `app\logs\scheduler\2026-05-20`
- `app\logs\scheduler\2026-05-21`
- `app\logs\scheduler\2026-05-22`
- `app\logs\scheduler\2026-05-27`
- `app\logs\scheduler\2026-05-30`
- `app\logs\scheduler\2026-05-31`
- `ci-cd\jenkins`
- `monitoring\grafana`
- `monitoring\prometheus`

---

## 3. Recommendations & Action Plan

1. **Delete Stale/Broken Reparse Points**: Remove the root `DEVOP1` reparse point to prevent shell looping or backup failures.
2. **Purge Ignored Document Backups**: The `.wbk` backup file under `documentation/` can be safely deleted. Keep `DEVOP1 - Project terms.docx` only if it represents the primary requirement sheet.
3. **Manage Empty Folders**: Keep empty placeholder directories like `app/dags` and `app/plugins` only if Apache Airflow requires them structurally. Otherwise, remove them to keep the directory tree clean.
