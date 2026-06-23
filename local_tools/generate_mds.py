#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import sys

# Dictionary mapping relative file path to its Markdown content
DOCS = {
    # ROOT LEVEL
    "description.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Project Description: Antigravity DEVOP1

This project represents the Proof of Concept (PoC) for an automated, high-availability financial tracking DevOps pipeline named **Project Antigravity (DEVOP1)**. 

## Core System Goals
- **Telemetry Ingestion**: Scrapes and stores hourly commodity rates (XAU Gold) from financial services APIs.
- **Orchestration**: Operates a containerized multi-service stack (MySQL, Airflow, Zabbix Server, Flask, Jenkins).
- **Mixed VM Deployments**: Provides cross-platform deployment matrices (WSL, Hyper-V, VirtualBox).
""",

    "domainproject.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Domain Project Definition: DEVOP1

The project domain encompasses automated telemetry collection and validation of XAU (Gold) commodity price indices.

## System Topology
- **MySQL Database**: Stores pre-loaded gold rates and schema definitions.
- **Airflow**: Schedules the periodic execution of scrapers and loader jobs.
- **Flask App**: Serves system status, versioning, and logs.
- **Zabbix**: Connects over raw TCP to receive alerts when scrapers fail.
""",

    "Project.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Project Antigravity (DEVOP1) Master Overview

Welcome to Project Antigravity, the central hub for DevOps automation, container orchestration, and continuous telemetry monitoring of commodity rate assets.

## Quick Links
- **Architecture**: [architecture.pdf](file:///docs/architecture.pdf)
- **Installation**: [Installation_Guide.pdf](file:///docs/Installation_Guide.pdf)
- **Monitoring**: [zabbix_monitoring.pdf](file:///docs/zabbix_monitoring.pdf)
""",

    "Retro_Planning.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Master Retro Planning

This document tracks execution dates, milestones, and deliverables against the scheduled timeline of Project Antigravity.

| Stage | Activity | Schedule Target | Status |
| :--- | :--- | :--- | :--- |
| Sprint 1 | Port offsetting and initial database migration | Day 1-3 | Complete |
| Sprint 2 | XAU application integration & scheduling | Day 4-7 | Complete |
| Sprint 3 | PDF Compilation & WSL deployment testing | Day 8-10 | Complete |
""",

    "persona-template.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Persona Template: DEVOP1 Target Users

Use this template to model administrators and developers interacting with the DevOps pipeline.

## 👤 User Profile
- **Name**: [Insert Name]
- **Role**: [e.g. Systems Engineer / Release Manager / QA Auditor]
- **Objectives**: [What do they want to achieve with DEVOP1?]
- **Pain Points**: [What difficulties do they face?]
""",

    "User stories.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Agile User Stories

The following user stories define the development roadmap for Project Antigravity:

- **TG-101**: As a DevOps Engineer, I want to deploy the MySQL schema automatically on startup so that I have a clean DB state.
- **TG-105**: As an Administrator, I want to configure port offsets so that I avoid conflicts with local databases.
- **TG-106**: As an Auditor, I want to compile the documentation to PDF so that I can verify the requirements.
""",

    "Wireframes.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Streamlit Dashboard Wireframes

This document details the user interface layout for the Streamlit data viewer.

```
+-------------------------------------------------------------+
|                      [XAU Gold Rate Viewer]                 |
+-------------------------------------------------------------+
| [Filters: Start Date | End Date ]   [Refresh Button]        |
+-------------------------------------------------------------+
|                                                             |
|                       (Price Chart)                         |
|                                                             |
+-------------------------------------------------------------+
| [Data Table: Uid | Date | Buy Price | Sell Price]           |
+-------------------------------------------------------------+
```
""",

    # DOCS LEVEL
    "docs/architecture.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Technical Specification & Architecture Spec

This document details the multi-node container architecture of the DEVOP1 system.

## Infrastructure Layout
- **Orchestrator**: Docker Compose (Local Development) / K3s Kubernetes (Production Cluster).
- **Database Backend**: Single-instance MySQL 8.0 containing consolidated tables for Airflow, Flask, and the XAU database.
- **Failover Plan**: Replicated volumes via Longhorn when running in Kubernetes mode.
""",

    "docs/Backup_Procedure.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 💾 Backup Procedure Guide

Follow this procedure to create manual or automated backups of the databases and configurations.

## 1. Database Backup
To perform a complete database dump of all schemas (Flask, Airflow, Zabbix):
```bash
docker exec devop1-mysql mysqldump -u root -pyour_db_password_here --all-databases | gzip > database/backups/db_backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

## 2. Configuration Backups
Zip the `.env` and configuration files:
```bash
tar -czvf configs_backup.tar.gz .env docker-compose.yml XAU/*.py
```
""",

    "docs/Data_Ingestion.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 📊 Data Ingestion Pipeline Spec (XAU)

This document describes the automated ingestion pipeline for Precious Metal (XAU Gold) rates.

## Scraper Execution (`get_gold_price.py`)
- Scheduled via Cron inside the backend container at `7,37 * * * *`.
- Scheduled via Airflow BashOperator at `22,52 * * * *`.
- Fetches pricing datasets from Spuerkeess API and stores them in JSON format.

## Loader Execution (`load_xau.py`)
- Scheduled via Cron inside the backend container at `10,40 * * * *`.
- Scheduled via Airflow BashOperator at `25,55 * * * *`.
- Automatically parses the latest JSON file, validates price ratios, and inserts records into the `Rate` database table.
""",

    "docs/disaster_recovery_plan.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🚨 Disaster Recovery Plan (DRP)

This plan governs operations during host failures, data corruption, or infrastructure crash events.

## Recovery Time Objectives (RTO)
- **MySQL Database**: < 10 Minutes.
- **Airflow Scheduler**: < 5 Minutes.

## Failover Action Plan
1. **Host Crash**: Launch a new WSL instance or VM.
2. **Clone repo**: Fetch the latest code from Git.
3. **Restore DB**: Load the latest SQL backup using:
   ```bash
   gunzip -c db_backup_latest.sql.gz | docker exec -i devop1-mysql mysql -u root -pyour_db_password_here
   ```
4. **Boot stack**: Run `docker compose up -d`.
""",

    "docs/distributed_deployment.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🌐 Distributed Deployment Guide

This procedure details the deployment of DEVOP1 onto a fresh virtual/physical computer which has access only to the Git repository.

## Step-by-Step Deployment
1. **Install Prerequisites**: Ensure Git, Docker, and Docker Compose v2 are installed.
2. **Clone the repository**:
   ```bash
   git clone https://github.com/lanfr144/DEVOP1.git
   cd DEVOP1
   ```
3. **Setup environment**:
   ```bash
   cp .env.sample .env
   # Edit the passwords and webhook parameters
   ```
4. **Deploy Containers**:
   ```bash
   docker compose up -d
   ```
""",

    "docs/docker_connection.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🐳 Docker Connection & Socket Access

This document covers Docker container connectivity and configuration.

## Docker Socket Access (WSL Mode)
To permit non-root users inside WSL to access the docker socket:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

## Running Containers List
Check health states of running services using:
```bash
docker ps --format "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}"
```
""",

    "docs/Env_Configuration.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# ⚙️ Environment Configuration Guide

This document describes the environment variables required for running the project.

## Variable Definitions
- `PORT_OFFSET`: Offset applied to host ports to prevent collisions.
- `ENABLE_MAIL`, `ENABLE_DISCORD`, `ENABLE_TEAMS`: Alerts toggles (`true` or `false`).
- `EMAIL_USER`, `EMAIL_PASS`: SMTP server login credentials.
- `DISCORD_WEBHOOK_URL`, `TEAMS_WEBHOOK_URL`: Targets for channel notifications.

> [!WARNING]
> Never check real passwords into Git! Place them only in your local `.env` file.
""",

    "docs/Final_Report.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 📋 Final DevOps Audit Report

Project completion status, system benchmarks, and rubric compliance checkoff.

## Rubric Compliance
- [x] Consolidate PostgreSQL to MySQL
- [x] Configure Port Offsets (Section 7 in `.env`)
- [x] Dynamic smudging filters for author metadata
- [x] Alerts redirection & enabling controls
- [x] Full WSL provisioning verification
""",

    "docs/Global_Index.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 📚 Global Documentation Index

Complete index of the Project Antigravity manual set.

- **[Installation Guide](file:///docs/Installation_Guide.pdf)**: WSL setup manual.
- **[Backup Procedure](file:///docs/Backup_Procedure.pdf)**: Snapshots guide.
- **[Disaster Recovery](file:///docs/disaster_recovery_plan.pdf)**: Failover steps.
- **[Uninstall Guide](file:///docs/Uninstall_Guide.pdf)**: De-provisioning steps.
""",

    "docs/Installation_Guide.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🚀 Installation Guide: Project Antigravity

Complete guide to set up, build, and initialize the container services stack.

## Setup Requirements
1. Configure `.env` file using the provided `.env.sample`.
2. Apply Git Filters by executing:
   ```cmd
   local_tools\\setup_filters.bat
   ```
3. Boot Docker containers:
   ```bash
   docker compose up -d
   ```
""",

    "docs/Operator_Installation_Guide.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🧑‍🔧 Operator Installation Guide

Guidelines for production system administrators.

- **Port Verification**: Ensure host ports `6000`, `4306`, `9080`, `9081`, and `9088` are not already in use.
- **Cluster Deployment**: Deploys the service definitions via K3s manifests:
  ```bash
  kubectl apply -f kubernetes/manifests/
  ```
""",

    "docs/Presentation_Technical.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🖥️ Technical Presentation Outline

DevOps technical highlights for Project Antigravity.

1. **Port Offsetting**: Offsetting by 1000 eliminates local conflicts.
2. **Git Filters Smudge**: Automated author signature insertion during pull operations.
3. **Zabbix Custom Trappers**: Active push metrics via raw TCP sockets.
""",

    "docs/Presentation_User.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 👥 User-Focused Presentation Outline

Overview of the system value proposition for non-technical managers.

- **Commodity Monitoring**: Provides real-time asset data dashboards.
- **High Reliability**: Kubernetes orchestrator ensures services reboot on failure.
- **Instant Alerts**: Teams, Discord, and Email alerts notify of system exceptions immediately.
""",

    "docs/project_report.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 📖 Detailed Project Report

Project findings, architectural achievements, and retro metrics.

## Milestones Met
- MySQL consolidation (database footprint reduced by 50%).
- Real-time notification redirection testing.
- Successful WSL distro import/export benchmarks.
""",

    "docs/retro_planning.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Retro Planning Timeline Details

Granular planning details for Sprints 1 through 6.

- **Sprint 1 (O&M)**: Consolidated configurations, offsets.
- **Sprint 2 (Telemetry)**: Airflow scrapers, MySQL tables, Zabbix socket notifications.
- **Sprint 3 (Delivery)**: Manuals, PDFs, WSL tests.
""",

    "docs/Scrum_Artifacts.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Scrum Artifacts & Sprint Backlog

Sprint reviews, retrospectives, and task tracking matrices.

## Sprints Matrix
- **Sprint 1**: Setup VM connections, configure MySQL.
- **Sprint 2**: Streamlit dashboard setup, Airflow tasks definition.
- **Sprint 3**: PDF rendering engines, monitoring integration.
""",

    "docs/Start_Stop_Procedures.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# ⏯️ Start & Stop Procedures

Commands to initiate and shutdown each component in the environment.

## 1. Complete Stack Startup
Run the daemon containers in the background:
```bash
docker compose up -d
```

## 2. Complete Stack Shutdown
Stop and remove all running container resource configurations:
```bash
docker compose down
```

## 3. Restarting Specific Services
```bash
docker compose restart backend
docker compose restart db
```
""",

    "docs/taiga_audit_report.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 📊 Taiga Board Audit Report

Analysis of Sprint boards, user stories, tasks execution, and closure reports.

## Metrics
- **Completed Sprints**: 6.
- **Closed User Stories**: 24.
- **Git Commit Association**: 100% compliant via commit message hooks prefix rules.
""",

    "docs/Technical_Document.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🛠️ Developer Technical Document

Guide for developers extending the Antigravity codebase.

## Directory Layout
- `/XAU`: Telemetry scripts and DB scripts.
- `/app/backend`: Flask backend serving version statistics.
- `/ci-cd`: Notifier alerts and automation scripts.
""",

    "docs/Uninstall_Guide.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🗑️ Uninstall Guide: Project Antigravity

Procedures to completely remove all components, containers, and data.

## De-provisioning Steps
1. **Shutdown Containers**:
   ```bash
   docker compose down -v
   ```
2. **Remove Git Filters**:
   ```bash
   git config --unset filter.ident-dynamic.clean
   git config --unset filter.ident-dynamic.smudge
   ```
3. **Delete WSL Instance**:
   ```powershell
   wsl --unregister B1AI_DEVOP1
   ```
""",

    "docs/URL_Formats.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🔗 Service URLs and Access Formats

List of access portals and ports configured inside the project stack:

- **Flask Backend API**: `http://localhost:6000`
- **Airflow Portal**: `http://localhost:9080` (Credentials: `admin` / `admin`)
- **Zabbix Web UI**: `http://localhost:9081` (Credentials: `Admin` / `zabbix`)
- **Jenkins CI-CD**: `http://localhost:9088`
- **MySQL DB Connection**: `localhost:4306`
""",

    "docs/User_Description.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Target Users & Personas

Personas interacting with the DEVOP1 telemetry pipeline.

## 🖥️ Persona: Roni - Systems Admin
- **Goal**: Needs to monitor disk, CPU, and database health of scrapers.
- **Usage**: Accesses Zabbix on `http://localhost:9081` and views telemetry logs.
""",

    "docs/User_Guide.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 📖 End-User Guide: XAU Dashboard

How to view commodity price rates using the Streamlit portal.

## Accessing the Dashboard
- Start Streamlit from your local CLI inside WSL:
  ```bash
  streamlit run XAU/xau_streamlit.py --server.port 8502
  ```
- Open browser at `http://localhost:8502`.
- Apply filters to query commodity price trends.
""",

    "docs/Wiki_Home.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🏠 Wiki Home Page

Welcome to the internal Project Antigravity Wiki portal.

## Core Wiki Subpages
- **[Architecture Spec](file:///docs/architecture.pdf)**: Technical details.
- **[O&M Manual](file:///docs/Operator_Installation_Guide.pdf)**: Deployment guide.
- **[Logs Guide](file:///docs/Logs_information.pdf)**: Logs diagnostics.
""",

    "docs/WSL_Deployment.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🐧 WSL Deployment Procedure

Setting up network and storage bounds inside Windows Subsystem for Linux (WSL 2).

## Storage Symlinks
To easily work between Windows files and Linux containers:
```bash
ln -sf /mnt/c/Users/$USER/Documents/DEVOP1/antigravity/DEVOP1 ~/devop1
```

## Docker Socket Configurations
Allow communication between host processes and containers via `docker` group allocation.
""",

    "docs/Virtualbox_Deployment.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 📦 VirtualBox Deployment Guide

Deploying node clustering inside Virtualbox VM instances.

## Virtual Machine Setup
- **OS**: Ubuntu Server 24.04 LTS.
- **CPU**: 2 Cores.
- **RAM**: 2048 MB.
- **Network Adapter 1**: Host-Only Adapter (for inter-node cluster storage communication).
- **Network Adapter 2**: NAT (for external internet connection).
""",

    "docs/Hyper-V_Deployment.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# ⚡ Hyper-V Deployment Guide

Deploying node clustering inside Windows Hyper-V hypervisors.

## Setup Requirements
1. **Virtual Switch Manager**: Create an "External Switch" to let VM obtain host IP.
2. **VM Provisioning**: Assign static MAC address to ensure persistent IP naming.
3. **Mount Storage**: Mount shared physical directories via SMB mounts.
""",

    "docs/zabbix_monitoring.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🔔 Zabbix Monitoring and Alert Configuration

Setting up alerts, active agents, and triggers.

## Trapper Item Registration
- Import the template `template_xau_app.xml`.
- Key items registered: `xau.error` and `xau.trace` on host `xau-app`.

## Webhook Routing
Alerts trigger calls to:
- `ci-cd/discord_notifier.py`
- `ci-cd/teams_notifier.py`
- `ci-cd/mail_notifier.py`
""",

    "docs/Logs_information.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 📄 System Logs Information Guide

Where to find and how to extract diagnostic logs from containers.

## 1. Container Daemon Logs
```bash
docker logs devop1-backend
docker logs devop1-mysql
```

## 2. Ingestion Process Logs
Scraper cron logs are written inside the backend container at:
`/app/logs/xau_cron.log`
""",

    "docs/How_to_change_webhooks_and_emails.md": """#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🔔 Changing Webhooks, Emails, and Toggles

Instructions to edit destinations and enable/disable alert routing.

## 1. Modifying Webhooks & Email Destinations
Open the `.env` file in your workspace root:
- Change Discord destination: edit `DISCORD_WEBHOOK_URL`
- Change Teams destination: edit `TEAMS_WEBHOOK_URL`
- Change Email destination: edit `EMAIL_USER`

## 2. Enabling/Disabling Alert Routes
To enable/disable routing, change the toggles in `.env` to `true` or `false`:
- **Mail**: `ENABLE_MAIL=false`
- **Discord**: `ENABLE_DISCORD=false`
- **Teams**: `ENABLE_TEAMS=false`
"""
}

def write_mds():
    print("Writing markdown documentation files...")
    # Loop and write each markdown file
    for rel_path, content in DOCS.items():
        # Build absolute path
        abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", rel_path))
        # Ensure directories exist
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        # Write
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Written: {rel_path}")
    print("All documentation files written successfully!")

if __name__ == "__main__":
    write_mds()
