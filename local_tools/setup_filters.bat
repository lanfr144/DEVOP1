::ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
@echo off
:: This script configures Git custom filters and hooks for Project Antigravity.
:: It is designed to run in a Windows command prompt or PowerShell.

:: 1. Clean filter: This runs when you stage a file ('git add'). It replaces expanded headers with neutral placeholders to prevent merge conflicts.
:: We use the absolute path to the filter script as requested by project specifications.
@git config filter.ident-dynamic.clean "python \"%~dp0git-ident-filter.py\" clean"

:: 2. Smudge filter: This runs when you checkout or pull files. It injects the actual author, committer, dates, and commit hash metadata.
:: The '%%f' placeholder represents the path of the file being processed by Git.
@git config filter.ident-dynamic.smudge "python \"%~dp0git-ident-filter.py\" smudge %%f"

:: 3. Universal date format: Forces git log to display dates in the YYYY/MM/DD HH:MM:SS format.
@git config log.date "format:%%Y/%%m/%%d %%H:%%M:%%S"

:: 4. Commit Message Hook: Installs the hook that checks if commit messages contain a valid Taiga Task ID prefix (e.g. TG-123).
@copy /Y local_tools\commit-msg .git\hooks\commit-msg >nul

@echo ✅ Git Filters and commit-msg hook configured with absolute paths for Windows.