#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
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
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```
