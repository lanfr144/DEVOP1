<!-- # ident @(#)$Format:PROJECT_NAME:FILE_NAME:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$ -->
# DEVOP1 Project Rubric & Delivery Checklist
**Deadline:** June 24, 2026

Antigravity must ensure the project repository fulfills these specific grading criteria:

## Part 1: Implementing Agile Methods
- [ ] Taiga boards configured and workloads assigned.
- [ ] Direct link to Git repository for code tracking via webhooks.

## Part 2: Version Control
- [x] At least 3 active feature branches with a clean commit history.
- [x] README.md includes a Git cheat sheet and workflow standards.
- [x] `.gitattributes` and Python script configured to manage `$Format$` expansion tags.
- [x] All file line endings are strictly configured to use `LF` (Line Feed) and not `CRLF`.

## Part 3 & 5: Docker & Web App
- [ ] Web App (Frontend + Backend) containerized with optimized Dockerfiles.
- [ ] `docker-compose.yml` orchestrating App, Database, and Zabbix for local dev.
- [ ] Secure `.env` file management for dynamic configuration.

## Part 4: MySQL Database
- [ ] MySQL containerized utilizing local `hostPath` volumes or local shared disks.
- [ ] SQLAlchemy Python script created to programmatically connect and load transformed data.

## Part 6: Zabbix Monitoring
- [ ] Zabbix Server, Web Interface, and Database containerized.
- [ ] 3 custom dashboards created (System metrics, App metrics, DB metrics) and exported as XML.
- [ ] Alerts configured to send notifications to Email, Discord, and Teams.

## Part 7: Jenkins & Kubernetes
- [ ] Jenkins installed on the Kubernetes cluster.
- [ ] Jenkins master configured to use Kubernetes plugin for dynamic build agents.
- [ ] Declarative `Jenkinsfile` written to build, test, and deploy the application to K8s.
