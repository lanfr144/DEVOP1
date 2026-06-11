The current version is #ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

---
name: git-commit
description: Enforces strict Git governance, Taiga tracking, branching strategies, and file metadata standards.
---

# Git Commit Governance Skill

When analyzing git commits, pull requests, or branch merges, you must strictly enforce the following rules:

## 1. Commit Messages & Tracking
- **Taiga Integration:** Every commit message MUST start with the specific Taiga task/story tag (e.g., `TG-123`, `US#123`, or `[#123]`) to update the task status. You must ensure a Git hook is actively verifying this format and rejecting non-compliant commits.

## 2. Branching Strategy & Segregation of Duties
- **Pipeline Flow:** Verify the code progresses strictly through three branches: `development` -> `test` (or `integration`) -> `production`.
- **WARNING - Segregation of Duties:** Since the current team size is small, DO NOT block the merge. Instead, **provide a warning** if the user attempting to promote/merge the code is the same user who originally authored the code, or if they are bypassing a branch.
- **WARNING - Cross-Branch Promotion:** You must issue a warning if the same user is attempting to promote files from one branch directly to another without proper review gates.

## 3. File Metadata & Formatting
- **Header Tag Requirement:** Verify that every file contains the exact identity tag format: `@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$`. Ensure it adapts the comment syntax appropriate for the file's language (e.g., `#` for Python/Shell, `//` or `/* */` for JavaScript/TypeScript, `--` for SQL, `::` or `REM` for Batch).
- **Line Endings:** Only Line Feed (LF) is allowed (Carriage Return Line Feed (CRLF) is strictly forbidden), with the exception of Windows batch files (`*.bat`), which must use CRLF. Exception: For executable scripts requiring a shebang (e.g., #!/bin/bash or #!/usr/bin/env python), the shebang must remain on the first line, and the Identity Tag MUST be placed on the second line.