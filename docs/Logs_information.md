#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
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
