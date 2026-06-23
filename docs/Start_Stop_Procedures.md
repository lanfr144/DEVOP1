#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
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
