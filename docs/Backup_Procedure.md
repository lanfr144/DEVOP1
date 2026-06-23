#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
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
