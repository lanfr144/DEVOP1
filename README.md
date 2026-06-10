# ident @(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$

# 🌌 Project Antigravity (DEVOP1)

[![Docker Compose](https://img.shields.io/badge/Orchestration-Docker_Compose-blue?logo=docker&logoColor=white)](https://docs.docker.com/)
[![MySQL 8.0](https://img.shields.io/badge/Database-MySQL_8.0-orange?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Apache Airflow](https://img.shields.io/badge/Orchestrator-Apache_Airflow_2.9.1-red?logo=apacheairflow&logoColor=white)](https://airflow.apache.org/)
[![K3s Kubernetes](https://img.shields.io/badge/Clustering-K3s_Kubernetes-green?logo=kubernetes&logoColor=white)](https://k3s.io/)

Welcome to **Project Antigravity (DEVOP1)**, an enterprise-grade Proof of Concept (PoC) demonstrating self-healing containerization, workflow automation, and unified database architectures across heterogeneous environments.

---

## 📐 System Architecture

The following diagram illustrates the containerized development topology and data flows:

```mermaid
graph TD
    %% Define styles
    classDef client fill:#f9f,stroke:#333,stroke-width:2px;
    classDef gateway fill:#bbf,stroke:#333,stroke-width:2px;
    classDef app fill:#ddf,stroke:#333,stroke-width:2px;
    classDef storage fill:#ffb,stroke:#333,stroke-width:2px;
    classDef monitor fill:#ffd,stroke:#333,stroke-width:2px;
    
    %% Elements
    User((Developer / Client)):::client
    HostPort[Host Port: 3317]:::gateway
    
    subgraph DockerCompose [Docker Compose Environment]
        WebBackend[web-backend <br> Python Flask API <br> Port 5000]:::app
        
        subgraph MySQL_Stack [MySQL Consolidated Engine]
            MySQL_DB[(MySQL 8.0 Daemon <br> Port 3306)]:::storage
            InitScript[init.sql <br> auto-provisioning]:::gateway
        end
        
        subgraph Airflow_Stack [Apache Airflow Engine]
            AirflowWeb[Airflow Webserver <br> Port 8080]:::app
            AirflowSch[Airflow Scheduler]:::app
        end
    end
    
    %% Flows
    User -->|API Requests| WebBackend
    User -->|External Access <br> Host:Port 3317| HostPort
    HostPort -->|Map| MySQL_DB
    
    InitScript -.->|First Run <br> Provision| MySQL_DB
    WebBackend -->|Connects to <br> devop1_db| MySQL_DB
    
    AirflowWeb -->|Metadata Store <br> airflow_db| MySQL_DB
    AirflowSch -->|Metadata Store <br> airflow_db| MySQL_DB
    
    class MySQL_DB,InitScript storage;
```

---

## 🛠️ Technology Stack & Matrix

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **User Interface** | React / Vanilla HTML & CSS | Frontend for end-user interaction. |
| **Backend API** | Flask (Python 3.11) | Serves endpoints, executes `cron` / `at` system jobs. |
| **Consolidated Database** | MySQL 8.0 | Single engine hosting multiple logical databases (`devop1_db`, `airflow_db`). |
| **Workflow Automation** | Apache Airflow 2.9.1 | Manages execution of DAGs via `LocalExecutor`. |
| **CI/CD Automation** | Jenkins / `antigravity_bot.py` | Idempotent sync of sprints to Taiga boards and build orchestration. |

---

## 💾 Unified Database Architecture (MySQL Consolidation)

To enforce security, optimize resources, and prevent database collisions, this project **consolidates all storage services into a single MySQL 8.0 database engine**, entirely removing PostgreSQL. 

### Logical Databases Hosted:
1. **`devop1_db`**: Stores Flask backend application schemas and transactional data.
2. **`airflow_db`**: Serves as the Apache Airflow workflow engine's metadata repository.

### Host Port Mapping:
* **Host Port:** `3317` (Exposed to avoid conflict with default local MySQL instances).
* **Container Port:** `3306` (Internal container communication is isolated).

### Automated Provisioning (`database/scripts/init.sql`)
When the MySQL stack spins up for the first time, it automatically executes the initialization script:
```sql
CREATE DATABASE IF NOT EXISTS devop1_db;
CREATE DATABASE IF NOT EXISTS airflow_db;

CREATE USER IF NOT EXISTS 'dev_user'@'%' IDENTIFIED BY 'your_db_password_here';
GRANT ALL PRIVILEGES ON devop1_db.* TO 'dev_user'@'%';

CREATE USER IF NOT EXISTS 'airflow'@'%' IDENTIFIED BY 'airflow';
GRANT ALL PRIVILEGES ON airflow_db.* TO 'airflow'@'%';
```

---

## 🔀 Git Workflow Standards & Cheat Sheet

We enforce strict Agile tracking and repository standards. **No changes to project files can be made without creating a task in Taiga first.** Commit messages must reference the Taiga ID (e.g., `TG-101`) to maintain clear audit logs.

### 📚 Commit Format Specification
```text
TG-<TaskID>: <Brief description in active voice>

- Detailed bullet point explaining why and what was changed
- Includes any testing verification executed
```
*Example:* `TG-105: Consolidate PostgreSQL to MySQL for Airflow metadata`

For all the commit a task in taiga must be associated. If the task does not exists created and add the task to a user story and a sprints.

### ⚡ Git Cheat Sheet

* **Create & Switch to a Feature Branch:**
  ```bash
  git checkout -b feature/TG-<TaskID>-description
  ```
* **Verify Current Workspace Status:**
  ```bash
  git status
  ```
* **Stage Modified & Untracked Files:**
  ```bash
  git add <filename>
  ```
* **Commit with Dynamic Formatting Rules:**
  ```bash
  git commit -m "TG-123: Implement database consolidation"
  ```
* **Push Branch to Origin:**
  ```bash
  git push -u origin feature/TG-<TaskID>-description
  ```

---

## ⚙️ Dynamic Git Filters ($Format$)

This repository utilizes advanced smudge/clean Git filters to dynamically inject repository metadata (author name, email, dates, commit hashes) into source code headers during checkouts, while storing them in a pristine "clean" state in Git to prevent merge conflicts.

### 🚀 Filter Setup Instructions

Run the setup script corresponding to your developer environment to register the filters in `.git/config`:

* **Windows Native (PowerShell/CMD):**
  ```cmd
  local_tools\setup_filters.bat
  ```
* **Unix / WSL / macOS:**
  ```bash
  chmod +x local_tools/setup_filters.sh
  ./local_tools/setup_filters.sh
  ```

These scripts register a **fully portable relative filter driver** that executes regardless of where your project repository is cloned:
```bash
git config filter.ident-dynamic.clean "python local_tools/git-ident-filter.py clean"
git config filter.ident-dynamic.smudge "python local_tools/git-ident-filter.py smudge %f"
```

---

## 🐳 Quickstart: Docker Compose Local Environment

1. **Verify or Configure the Local Environment (`.env`):**
   Ensure `.env` contains the required credentials and ports.
2. **Launch the Container Stack:**
   ```bash
   docker compose up -d
   ```
3. **Verify Service Health:**
   ```bash
   docker compose ps
   ```
4. **Access Applications:**
   * **Web Backend API:** `http://localhost:5000`
   * **Apache Airflow Dashboard:** `http://localhost:8080` (Credentials: `admin`/`admin`)
   * **MySQL Server:** Host `127.0.0.1`, Port `3317`, User `dev_user` / Pass `your_db_password_here`

---

## 🧪 Development Guidelines & Testing Policy

1. **Prerequisite Validation:** Every shell script and service config must programmatically verify that required environment variables exist and are not empty before proceeding with execution.
2. **Post-Task Verification:** A task cannot be resolved without a corresponding test validating its success. After executing database updates, connectivity checks must be run.
3. **WSL Integration:** WSL distributions (such as `B1AI_DEVOP1_LanFr144`) are linked directly to the project via `/mnt/c/...` or the home symlink (`~/devop1`), allowing easy CLI administration and verification under a Unix runtime.



## 🌟 Standard Repository & Skill Guidelines

This project strictly adheres to the developer standards defined across our organization's workspace. Every contribution must respect the following practices:

### 1. Git Commit & Pipeline Governance
* **Taiga Hook Validation:** Every commit message must start with a valid Taiga task/story ID tag (e.g., `TG-123`, `US#123`, or `[#123]`). A local git hook (`local_tools/commit-msg`) is configured to enforce this format.
* **Pipeline Progression:** Code must progress strictly through the branches: `development` -> `test` -> `production`.
* **Segregation of Duties:** Authors promoting/merging code must not be the sole author without secondary gate review (warnings will be generated if promoting directly without review gates).
* **Header Tag Requirement:** Every source code or text file must include the exact identity format on its first line (or second line if a shebang is required):
  `@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$`
  The comment syntax must match the file's language (e.g., `#` for Python/Shell, `//` or `/* */` for JS/TS, `--` for SQL, `::`/`REM` for Batch).
* **Line Endings:** All files must use **LF** (Line Feed) line endings. The only exception is Windows batch scripts (`*.bat`), which must use **CRLF**.
* **Wiki Documentation Cadence:** Progress files under `documentation/` must be generated and synced to the Taiga Wiki board (`python ci-cd/antigravity_bot.py --wiki documentation/`) according to the schedule:
  * Daily logs (`yyyymmdd_daily.md`) must be compiled and synced daily.
  * Plan logs (`yyyymmdd_plan.md`) must be compiled and synced once every 2 days (excluding Sundays).
  * Review logs (`yyyymmdd_revue.md`) must be compiled and synced once every 2 days (excluding Sundays).
* **Scratch Directory Management:** Files inside `./scratch` are never deleted. Instead, use the archiving utility `python local_tools/archive_scratch.py` to move them to `%USERPROFILE%\keep`. If a file already exists in the destination, a 3-digit version code is appended using a semicolon (e.g., `test_filter.py;001`, `test_filter.py;002`).

### 2. Code Review & Mentorship Policy
* **Mentorship Perspective:** Senior engineers and peer reviewers adopt a constructive, instructional persona when providing code feedback.
* **Review Checklist:**
  * **Correctness:** Verify the implementation solves the intended requirements.
  * **Edge cases:** Handle null inputs, boundary conditions, and error states defensively.
  * **Style:** Adhere strictly to project conventions.
  * **Performance:** Resolve nested loops, inefficient data structures, or other potential bottlenecks.
* **Feedback Quality:** Feedback must be specific, explaining the *why* rather than just the *what*, and offering clean alternative implementations where possible.

### 3. Refactoring & Architecture Standards
* **DRY Principle:** Identify duplicated blocks and extract them into reusable utilities, helper functions, or libraries.
* **Complexity Reduction:** Deconstruct long, monolithic functions into small, single-purpose helper functions.
* **Micro-Files Strategy:** Prefer small, single-purpose files over monolithic structures. This ensures cleaner change tracking and simpler unit testing.
* **Behavioral Safety:** Refactored code must maintain identical external APIs and behavior without side-effects.

### 4. Database & SQL Optimization Standards (MySQL)
* **Performance & Locks:** Prevent row locking issues and deadlocks. Always utilize database analysis tools (like `EXPLAIN`) for performance auditing.
* **Security & Access Control:**
  * **No Hardcoded Credentials:** Application scripts must never embed plain usernames or passwords.
  * **Restricted Access:** Access database objects via proxy users or restricted views owned by dedicated schemas.
  * **Bind Variables:** All parameterized inputs must use bind variables. Dynamic query string concatenation is strictly forbidden.
  * **Grants & Synonyms:** DDL/DML scripts must include required `GRANT` statements and `SYNONYM` configurations.
* **Transaction Management:** Auto-commit must be disabled. Explicitly control transaction scope via `COMMIT` and `ROLLBACK` blocks.
* **Syntax Standards:** Object and column names must be double-quoted (`"`) or back-quoted (`` ` ``) to prevent collision with reserved keywords. Avoid using keywords reserved in Oracle or standard SQL.

### 5. Documentation Synchronization
* **Continuous Synchronization:** Documentation, inline comments, and README instructions must be updated concurrently with any code change.
* **Architectural Impacts:** Significant system design updates must be traced and documented across the entire codebase.
* **Onboarding On-demand:** Documentation is authored assuming the reader is a new teammate, requiring maximum clarity and completeness.

### 6. Test-Driven Development (TDD) Policy
* **Isolation vs Integration:** Write unit tests for individual functions and integration tests for complete workflows.
* **Robust Mocks:** Mock external databases, API calls, and environment parameters using robust testing frameworks.
* **Coverage:** Strive for maximum logical coverage, specifically targeting newly modified lines of code.
