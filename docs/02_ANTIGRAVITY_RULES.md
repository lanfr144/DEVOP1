# Behavioral Instruction Manual & Code Standards: DEVOP1

This file serves as the strict behavioral blueprint for the DEVOP1 system. Any AI agent (Antigravity) working on this codebase MUST adhere to these commands.

## 1. Mandatory File Identification Header (CRITICAL)
Every single source code, configuration, or scripting file generated MUST contain the following identification string dynamically formatted for its respective language, placed immediately after a comment marker at the top of the file.

**For Python, Shell (.sh), YAML, and Markdown files:**
```text
# ident @(#)$Format:PROJECT_NAME:FILE_NAME:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$
```

## 2. Git & Taiga Repository Synchronization (CRITICAL)
The Git repository "https://github.com/lanfr144/DEVOP1" and the Taiga repository "https://tree.taiga.io/project/ferro988-devop1/timeline" must be kept in sync with the project at all times!
No changes to project files are allowed without:
1. Creating a corresponding task in the Taiga repository.
2. Updating the task status accordingly.
3. Referencing the Taiga task ID (e.g. `TG-XXX`) inside the Git commit message comments to maintain a complete operational audit trail.
