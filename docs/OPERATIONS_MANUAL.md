The current version is #ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 📖 Operations & Maintenance Manual: Project Antigravity (DEVOP1)

This operations manual provides a unified guide for setup, port offsetting, testing, monitoring, backups, and deployment.

---

## ⚙️ 1. Project Lifecycle & Branch Status

The repository utilizes a cascading branching model:
`development` ➡️ `test` (integration & QA) ➡️ `production` (stable releases)

### Current Status
* **Development Phase:** **Closed & Verified.** All core features, Zabbix telemetry templates, K8s manifests, and Git hooks are complete.
* **Working Branch:** Currently committed and pushed on the `development` branch.
* **Next Steps:** Merge the `development` branch into `test` to perform cluster integration testing, followed by promotion to the `production` branch.

---

## 🚀 2. Local Installation & Workspace Setup

### Step 2.1: Clone and Check Out
```bash
# Clone the repository
git clone https://github.com/your_windows_user_here/DEVOP1.git
cd DEVOP1

# Ensure you are on the active development branch
git checkout development
```

### Step 2.2: Configure the Environment
Create a `.env` file in the root directory and configure the environment variables:
```ini
# Network Mode ('local' or 'server')
NETWORK_MODE=local

# MySQL Database Credentials
DB_ROOT_PASSWORD=your_db_password_here
DB_NAME=devop1_db
DB_USER=dev_user
DB_PASSWORD=your_db_password_here

# Taiga Project Credentials
TAIGA_API_URL=https://api.taiga.io/api/v1
TAIGA_USERNAME=your_windows_user_here
TAIGA_PASSWORD=YOUR_PASSWORD
TAIGA_PROJECT_ID=1785465

# Dynamic Port Offset
PORT_OFFSET=1000
```

### Step 2.3: Register Dynamic Git Filters & Hook
Register the dynamically smudged filters to expand dynamic placeholders and copy the validation hook:
* **Windows CMD / PowerShell:**
  ```cmd
  local_tools\setup_filters.bat
  ```
* **Linux / WSL Terminal:**
  ```bash
  chmod +x local_tools/setup_filters.sh
  ./local_tools/setup_filters.sh
  ```

---

## 🔌 3. Port Offset & Availability Verification

To avoid collisions with other software or WSL distributions on your PC, all default ports are mapped with a `PORT_OFFSET` configuration.

### Port verification script
Run the verification script to calculate target ports, check socket availability on the host loopback (`127.0.0.1`), and write variables to `.env`:
```bash
python local_tools/apply_port_offset.py
```
* **Calculated Ports (Example with `PORT_OFFSET=1000`):**
  - Flask Web API: `6000`
  - MySQL Relational Engine: `4306`
  - Airflow Web Server: `9080`
  - Zabbix Web UI: `9081`
  - Jenkins Master: `9088`

If any target port is currently in use, the script will abort with an error, protecting the host system from configuration conflicts.

---

## 🐳 4. Local Deployment (Docker Compose)

Launch the stack using Docker Compose:
```bash
# Verify ports and update env
python local_tools/apply_port_offset.py

# Launch containers in background
docker compose up -d

# Verify container statuses
docker compose ps
```
### Consolidated Database & Airflow
The local environment is optimized to run entirely on **MySQL 8.0**, removing PostgreSQL. Airflow and Flask connect to the unified engine.

---

## 🔄 5. Taiga & Agile Board Synchronization

### 5.1 Sprint & Task Populator
To sync local sprint tasks defined in `taiga-sprints.yml` to the Taiga board:
```bash
python ci-cd/antigravity_bot.py --populate taiga-sprints.yml
```

### 5.2 Wiki Log cadences
Publish logs from `documentation/` and `docs/` to the Taiga Wiki board:
```bash
python ci-cd/antigravity_bot.py --wiki documentation/
python ci-cd/antigravity_bot.py --wiki docs/
```
* **Wiki Scheduling Policy:**
  - Daily logs (`yyyymmdd_daily.md`) must be compiled and synced daily.
  - Plan logs (`yyyymmdd_plan.md`) must be compiled once every 2 days (excluding Sundays).
  - Review logs (`yyyymmdd_revue.md`) must be compiled once every 2 days (excluding Sundays).

### 5.3 Git Commit hook
All commits must start with the Taiga task ID (e.g. `TG-105: ...`). The commit hook `local_tools/commit-msg` automatically rejects non-compliant messages.

---

## 💾 6. Database Backup & Restore Procedures

### 6.1 Database Backup
```bash
# Dump all consolidated databases (devop1_db, airflow_db, zabbix)
docker exec devop1-mysql mysqldump -u root -pyour_db_password_here --all-databases | gzip > database/backups/db_backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

### 6.2 Database Restore
```bash
# Decompress and restore the snapshot back into the container daemon
gunzip -c database/backups/db_backup_XXXXXXXX_XXXXXX.sql.gz | docker exec -i devop1-mysql mysql -u root -pyour_db_password_here
```

### 6.3 Log Cleanup & Scratch Archiving
* **Log Rotation:** Rotating and compressing system logs older than 7 days runs via `ci-cd/log_cleanup.sh`.
* **Scratch Archiving:** Temporary scratch files are never deleted. Run `python local_tools/archive_scratch.py` to archive files from `./scratch` to `%USERPROFILE%\keep`, generating 3-digit semicolon version suffixes if duplicate filenames exist.

---

## 🧪 7. Testing & Verification Procedures

### 7.1 Port Listener Check
Test that host ports are actively listening after spinning up services:
```bash
# Windows PowerShell
Test-NetConnection -ComputerName 127.0.0.1 -Port 6000
Test-NetConnection -ComputerName 127.0.0.1 -Port 4306
```

### 7.2 Docker Compose Syntax Check
```bash
docker compose config
```

### 7.3 Kubernetes Manifest Validation
Validate manifest declarations before applying them to a live cluster:
```bash
kubectl apply --dry-run=client -f kubernetes/manifests/
```

---

## ☸️ 8. Kubernetes Production Deployment & CI/CD

### 8.1 Manual Deployment
Deploy resources to the Kubernetes namespace:
```bash
kubectl apply -f kubernetes/manifests/
```
This provisions:
- MySQL instance with a 5Gi persistent volume claim (`mysql.yaml`).
- Flask backend API (`backend.yaml`).
- Airflow scheduler and webserver (`airflow.yaml`).
- Zabbix monitoring server and web portal (`zabbix.yaml`). <!-- NGINX is built into the zabbix-web image -->
- Jenkins Master workspace with persistent volume storage (`jenkins.yaml`).

### 8.2 Declarative CI/CD Pipelines
The [Jenkinsfile](file:///c:/Users/your_windows_user_here/Documents/DEVOP1/antigravity/DEVOP1/Jenkinsfile) in the root of the repository automates the pipeline steps:
1. **Pull Code:** Checks out the latest codebase from GitHub.
2. **Build Docker Images:** Builds optimized Docker images for components.
3. **Run Tests:** Runs unit and integration test scripts.
4. **Deploy:** Deploys manifests to the production Kubernetes environment.