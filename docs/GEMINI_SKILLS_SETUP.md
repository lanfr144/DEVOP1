The current version is #ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🧠 Gemini Agent Skills Configuration & Setup Guide

This guide details the structure of the custom Gemini agent skills that drive code standards, reviewing criteria, and development standards across the repository.

---

## 📂 1. Directory Structure & Key Files

The skills are stored under the workspace configuration directory. They consist of seven sub-directories, each containing a `SKILL.md` file defining the specific instructions and persona guidelines:

```text
skills/
├── code-review/
│   └── SKILL.md      # Defines code correctness, edge cases, and style review guidelines.
├── doc-writer/
│   └── SKILL.md      # Directs documentation synchronization with source code edits.
├── expert-coach/
│   └── SKILL.md      # Mentoring rules, modularity principles, and header tag formats.
├── git-commit/
│   └── SKILL.md      # Branch pipeline flows and Taiga commit message integrations.
├── refactor-coach/
│   └── SKILL.md      # DRY principles, complexity reduction, and API preservation.
├── sql-optimizer/
│   └── SKILL.md      # Security, bind variables, auto-commit disable, and syntax standards.
└── test-generator/
    └── SKILL.md      # Isolation/integration testing and coverage standards.
```

---

## 🔍 2. Detailed Skill Descriptions

### 🛡️ Code Review (`skills/code-review/SKILL.md`)
Enforces automated checks on code changes for correctness, edge-case safety, style consistency, and performance efficiency. Ensures that review feedback is actionable, explaining the "why" behind any requested change.

### 📝 Doc Writer (`skills/doc-writer/SKILL.md`)
Enforces strict synchronization between source code changes and project documentation. Ensures READMEs, code comments, and configuration guides stay up-to-date across all development tasks.

### 🎓 Expert Coach (`skills/expert-coach/SKILL.md`)
Adopts a senior engineering persona to mentor junior developers. Enforces optimal algorithm selection, deep inline comments, test coverage, modular code structures (micro-files over monoliths), and the mandatory project-wide identity tags.

### 🌿 Git Commit (`skills/git-commit/SKILL.md`)
Enforces strict Git governance, ensuring:
- Commit messages start with a valid Taiga task/story reference (e.g. `TG-105: ...`).
- Branch pipeline flow checks (`development` -> `test/integration` -> `production`).
- Segregation of duties warning if the same user authors and reviews/promotes code.
- File-formatting rules including strict LF line ending enforcement (except for `.bat` files using CRLF) and identity headers.

### ⚙️ Refactor Coach (`skills/refactor-coach/SKILL.md`)
Enforces software refactoring best practices, prioritizing the DRY (Don't Repeat Yourself) principle, function complexity reduction, performance optimizations, and ensuring absolute preservation of existing APIs/behavior.

### 🗄️ SQL Optimizer (`skills/sql-optimizer/SKILL.md`)
Enforces DBA-level standards for SQL databases (MySQL, PostgreSQL, Oracle), including:
- Query optimization, locking checks, and composite/B-Tree indexing.
- Dynamic bind variables to prevent SQL injection.
- Security protocols (restricted schemas, no hardcoded users, audit recommendations).
- Explicit transaction management (no auto-commit).
- Object quotation and Oracle-reserved word collision checks.

### 🧪 Test Generator (`skills/test-generator/SKILL.md`)
Enforces standard unit and integration test generation. Directs the agent to cover boundary conditions, handle unexpected nulls/inputs, use mocking frameworks to isolate third-party APIs/databases, and maximize test coverage.

---

## ⚙️ 3. Setup Instructions

To correctly drive the Gemini agent working on this codebase, these files must be located in the agent's active configuration directory on the developer's workstation:

* **On Windows Workstations:**
  Copy the `skills/` folder structure to:
  `%USERPROFILE%\.gemini\config\skills\`
  *(e.g., `C:\Users\<username>\.gemini\config\skills\`)*

* **On Linux / macOS / WSL Environments:**
  Copy the `skills/` folder structure to:
  `~/.gemini/config/skills/`
  *(e.g., `/home/<username>/.gemini/config/skills/`)*

Once in place, the IDE agent dynamically reads these markdown files to enforce database optimization, code cleanliness, test generation, and commit checks throughout the coding process.