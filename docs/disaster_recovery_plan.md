#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
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
