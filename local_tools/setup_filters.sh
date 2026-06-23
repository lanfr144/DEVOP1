#!/bin/sh
#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# This script registers custom Git filters and hooks on Unix, WSL, or macOS environments.

# 1. Clean filter: Standardizes expansion headers to placeholder formats before code commits.
# Uses absolute path format as specified.
git config filter.ident-dynamic.clean "python3 \"C:/Users/your_windows_user_here/Documents/DEVOP1/antigravity/DEVOP1/local_tools/git-ident-filter.py\" clean"

# 2. Smudge filter: Replaces metadata placeholders on checkouts with actual author/committer data.
git config filter.ident-dynamic.smudge "python3 \"C:/Users/your_windows_user_here/Documents/DEVOP1/antigravity/DEVOP1/local_tools/git-ident-filter.py\" smudge %f"

# 3. Universal date format for git logs: sets date formatting.
git config log.date "format:%Y/%m/%d %H:%M:%S"

# 4. Git commit-msg hook: copies verification script and marks it executable.
cp local_tools/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg

echo "✅ Git Filters and commit-msg hook configured with absolute paths for Unix/WSL."