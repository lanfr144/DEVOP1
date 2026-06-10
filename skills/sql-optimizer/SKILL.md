---
name: sql-optimizer
description: Optimizes and secures SQL for MySQL, Oracle, and PostgreSQL, enforcing strict DBA standards.
---

# SQL Optimizer & DBA Skill

When reviewing, optimizing, or generating SQL code (MySQL, Oracle, PostgreSQL), enforce these strict database guidelines:

## 1. Performance & Concurrency
- **Locking:** Avoid row locking issues and design queries to prevent deadlocks.
- **Indexing:** Suggest optimal indexes, including B-Tree, full-text, spatial, or composite indexes where appropriate.
- **Testing:** When testing SQL in non-production environments, utilize all available database optimizer tools (e.g., `EXPLAIN PLAN`, `tkprof`).

## 2. Security & Access Control
- **No Hardcoded Users:** NEVER hardcode usernames in scripts.
- **Proxy/Restricted Access:** Ensure the program accesses objects through proxy users or restricted views (objects must be owned by one or more dedicated owner schemas, not the application user).
- **Audit Policies:** Recommend the setup of appropriate audit policies for sensitive tables/actions (Do not write the scripts to set them up, only advise).
- **Bind Variables:** SQL statements MUST use bind variables to pass and receive values. No dynamic concatenation of user inputs.
- **Grants & Synonyms:** Whenever new objects are created or accessed, you MUST provide all the necessary `GRANT` statements and `SYNONYM` creations required for the application to function securely.
## 3. Transaction Management
- **No Auto-Commit:** Disable auto-commit. Explicitly manage transactions with `COMMIT` and `ROLLBACK` blocks.

## 4. Syntax & DDL Standards
- **Quoted Identifiers:** All object and column names must be double-quoted (`"`) or back-quoted (`` ` ``) to avoid collisions with reserved words. Warn if a name matches a `V$RESERVED_WORDS` in Oracle.
- **Reserved Words Warning:** Issue a warning if an object or column name matches an Oracle reserved word (from `V$RESERVED_WORDS`).
- **DDL Changes:** All Data Definition Language (DDL) changes must be generated using `DBMS_METADATA` and `DBMS_METADATA_DIFF` to calculate and apply exact differences.
- **Exception Management:** Always implement robust exception handling (e.g., `EXCEPTION` blocks in PL/SQL) to capture, manage, and log database errors gracefully. Do not allow silent failures.

## 5. Mandatory File Header
- **Identity Tag:** The first line of ANY provided source code or text file MUST be a comment containing exactly this string: `#ident @(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$`. Adapt the comment syntax (e.g., "//", "#", "--", "`", "!", "REM", "/*  */") to the specific language. Exception: For executable scripts requiring a shebang (e.g., #!/bin/bashor#!/usr/bin/env python), the shebang must remain on the first line, and the Identity Tag MUST be placed on the second line.
