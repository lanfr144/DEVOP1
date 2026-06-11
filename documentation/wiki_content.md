The current version is #ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Antigravity Architecture & Operations Wiki

## Overview
Antigravity is a containerized stack managed via Docker Compose, designed for scalable and robust development.

## Infrastructure Components
* **Web Backend**: Python-based application serving API traffic.
* **MySQL Database**: Persistent storage for all core backend services.
* **Apache Airflow**: Robust orchestration engine using LocalExecutor for DAGs.
* **Scheduling**: Cron and `at` daemons configured on all nodes for system-level background jobs.
* **CI/CD**: Custom `antigravity_bot.py` syncs YAML sprints into Taiga. Discord/Teams are used for notifications.

## Git & Taiga Integration
All developers **must** include the Taiga task identifier in their Git commits (e.g., `TG-123: Add feature`). 
A Git Webhook has been established via Taiga's GitHub integration so that these commits automatically log activity to the associated User Stories.

## Log Management
Automated log rotation runs via cron `ci-cd/log_cleanup.sh`, pruning old container and system logs to prevent disk exhaustion.