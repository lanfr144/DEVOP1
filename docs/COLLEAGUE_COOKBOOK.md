The current version is #ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

# 📖 Colleague Onboarding & Setup Cookbook: DEVOP1

Welcome to **Project Antigravity (DEVOP1)**! This cookbook provides a step-by-step walkthrough to set up your local development environment on your Windows PC using Docker, WSL 2, and Git.

---

## 📋 Prerequisites
Ensure your local machine has the following tools installed and active:
* **WSL 2** (Windows Subsystem for Linux) with a modern distribution (e.g. Ubuntu).
* **Docker Desktop** (with "Use the WSL 2 based engine" enabled in settings).
* **Git** (Windows native client and/or inside WSL).
* **Python 3.10+** (installed on both Windows and WSL).

### 🔌 Recommended VS Code Extensions
When you open this project in VS Code, you will see a prompt recommending the workspace extensions configured in `.vscode/extensions.json`. Installing these will significantly streamline your work:
* **WSL Extension** (`ms-vscode-remote.remote-wsl`): Connects VS Code directly inside your WSL `B1AI_DEVOP1` environment.
* **Docker Extension** (`ms-azuretools.vscode-containers`): Manages containers, logs, and compose services directly from the VS Code UI.
* **YAML Extension** (`redhat.vscode-yaml`): Auto-validates and formats your `docker-compose.yml` and `taiga-sprints.yml`.
* **SQLTools + MySQL Driver** (`mtxr.sqltools` & `mtxr.sqltools-driver-mysql`): Connects to and executes queries against the unified MySQL database on port `3317` directly within the editor.
* **Python & Pylance** (`ms-python.python`): Native Python validation and syntax diagnostics for `git-ident-filter.py` and `antigravity_bot.py`.

---


## 🚀 Step-by-Step Environment Setup

### Step 1: Clone the Repository
Clone the repository and switch to the active development branch:
```bash
# Clone the repository
git clone https://github.com/lanfr144/DEVOP1.git
cd DEVOP1

# Check out the active development branch
git checkout development
```

### Step 2: Configure Environment Variables (`.env`)
Create a `.env` file in the root directory by copying the configuration below. Replace credentials and webhook endpoints with your own tokens:
```ini
# .env
DB_ROOT_PASSWORD=your_db_password_here
DB_NAME=devop1_db
DB_USER=dev_user
DB_PASSWORD=your_db_password_here

# Taiga Integration Configuration
TAIGA_API_URL=https://api.taiga.io/api/v1
TAIGA_USERNAME=YOUR_TAIGA_USERNAME
TAIGA_PASSWORD=YOUR_TAIGA_PASSWORD
TAIGA_PROJECT_ID=1785465

# Webhook Alert Channels
TEAMS_WEBHOOK_URL=YOUR_TEAMS_WEBHOOK_ENDPOINT
DISCORD_WEBHOOK_URL=YOUR_DISCORD_WEBHOOK_ENDPOINT
```
> [!WARNING]
> Keep `.env` strictly out of version control! It is already configured in `.gitignore` to prevent leaks.

### Step 3: Register the Portable Git Filters
This repository uses dynamic clean/smudge filters to manage dynamic `$Format$` headers across code files.
Run the setup script corresponding to your command line environment to register the relative filters:

* **Windows Command Prompt / CMD:**
  ```cmd
  local_tools\setup_filters.bat
  ```
* **Linux / WSL Terminal:**
  ```bash
  chmod +x local_tools/setup_filters.sh
  ./local_tools/setup_filters.sh
  ```

* **Force Checkout to Apply Smudge Tags:**
  To populate the `$Format$` tags inside your working files with your personal metadata, run:
  ```bash
  git add --renormalize .
  git checkout -f -- .
  ```

---

## 🐧 Step 4: Register & Link Your WSL Distribution

To keep WSL distribution names generic and easy to manage, execute the following commands in PowerShell on your Windows PC:

1. **Clean WSL Naming:**
   Import your preferred WSL instance under the project generic name `B1AI_DEVOP1`.
2. **Default Password Configuration:**
   Standardize your user password inside WSL to `"your_db_password_here"`. In your WSL bash shell, run:
   ```bash
   sudo passwd $USER
   # Set the password to: your_db_password_here
   ```
3. **Link Your Codebase to WSL:**
   Inside your WSL home directory, create a symbolic link directly to the Windows repository folder to work seamlessly between Windows and Linux:
   ```bash
   ln -sf /mnt/c/Users/YOUR_WINDOWS_USER/PATH_TO_REPO/DEVOP1 ~/devop1
   ```
   You can now access your repository in WSL via `cd ~/devop1`.

4. **WSL Docker Permission Fix (Non-Root execution):**
   If you receive a `permission denied` error when executing `docker` commands (such as `docker ps`) under your local WSL user, you must join the `docker` group inside WSL.
   In Windows PowerShell, run the following to add your WSL user to the `docker` group and restart the instance:
   ```powershell
   # Add your WSL user to the docker group
   wsl -d B1AI_DEVOP1 -u root bash -c "groupadd -f docker; usermod -aG docker YOUR_WSL_USER"
   
   # Restart the WSL distribution to apply group changes
   wsl -t B1AI_DEVOP1
   ```
   *Note: On your next login via `wsl -d B1AI_DEVOP1`, you can run `docker ps` immediately under your own user context without root or `sudo`!*


---

## 🐳 Step 5: Start the Container Infrastructure

Spin up the local container stack via Docker Compose.
```bash
docker compose up -d
```

### Consolidated Database & Safe Ports Matrix:
* **Single Engine:** PostgreSQL is removed; all applications (including Airflow) run on **MySQL 8.0**.
* **Database Port:** Exposes container port `3306` externally as **host port `3317`** (e.g. `127.0.0.1:3317`) to prevent conflicts with other local databases on your machine.
* **Auto-Provisioning:** The SQL initialization script `database/scripts/init.sql` runs on container boot, setting up:
  * `devop1_db` (Flask Web Backend)
  * `airflow_db` (Apache Airflow Metadata Engine)

### Exposing Dashboards:
* **Web Backend API:** `http://localhost:5000`
* **Apache Airflow Dashboard:** `http://localhost:8080` (Credentials: `admin` / `admin`)

---

## 🔄 Step 6: Sync with Taiga & Agile Guidelines

To ensure the Agile board stays in sync with your local commits:

1. **Populate Local Sprints & Tasks:**
   Run the sync bot to pull/push tasks dynamically:
   ```bash
   python ci-cd/antigravity_bot.py --populate taiga-sprints.yml
   ```
2. **Strict Agile Branching & Commits Rule:**
   * **Rule 1:** Never modify any files without first making sure a corresponding task is created in the Taiga project board.
   * **Rule 2:** Always prefix your commit messages with the Taiga task ID (e.g., `TG-105`) so that commits link to the correct cards on the sprint dashboard:
     ```bash
     git commit -m "TG-105: Consolidate metadata database to MySQL"
     ```
3. **Cascading Branches Progression:**
   * Run active feature branches and developments on the **`development`** branch.
   * Merge up to **`testing`** for integration testing and QA.
   * Merge up to **`production`** for stable release-ready tags.