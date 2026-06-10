#ident @(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$
# 📋 Project Deployment & Maintenance Procedures

This guide provides step-by-step instructions on configuring ports, deploying the containerized stack, creating database backups, and restoring system state.

---

## 🔌 1. Dynamic Port Offsetting & Remapping

To prevent host port collisions across multiple development and WSL instances, all service ports are mapped using a `PORT_OFFSET` configuration defined in `.env`.

### Calculated Host Ports
The system adds the `PORT_OFFSET` to each service's standard default port:
* **Flask Web API:** `5000` + `PORT_OFFSET`
* **MySQL Database:** `3306` + `PORT_OFFSET`
* **Airflow Webserver:** `8080` + `PORT_OFFSET`
* **Zabbix Web UI:** `8081` + `PORT_OFFSET`
* **Jenkins Master:** `8088` + `PORT_OFFSET`

### Port Verification Script
Before launching services, you **must** execute the port calculator and verification script:
```bash
python local_tools/apply_port_offset.py
```
This utility will:
1. Load `PORT_OFFSET` from `.env`.
2. Compute the target host ports.
3. Establish socket connections to verify the ports are currently free.
4. Write the mapped port variables (e.g. `BACKEND_PORT`, `MYSQL_PORT`) to `.env` if all check out. If a port is in use, the script aborts.

---

## 🐳 2. Local Deployment: Docker Compose

Once ports are verified and written to `.env`, launch the local container stack:
```bash
# Verify port allocations
python local_tools/apply_port_offset.py

# Spin up services in detached mode
docker compose up -d

# Verify service health
docker compose ps
```

---

## ☸️ 3. Production Deployment: Kubernetes manifests

To deploy the stack to the local or remote Kubernetes cluster (K3s / Minikube):
```bash
# Apply deployments, services, and PVCs
kubectl apply -f kubernetes/manifests/
```
Verify the status of pods and services:
```bash
kubectl get pods -w
kubectl get svc
```

---

## 💾 4. Database Backup & Restore Procedures

All database services (Flask app, Airflow, and Zabbix) are consolidated inside the single MySQL container.

### 4.1 Creating a Database Backup
To take a logical snapshot of all schemas:
```bash
# Execute mysqldump inside the container and compress it
docker exec devop1-mysql mysqldump -u root -pyour_db_password_here --all-databases | gzip > database/backups/db_backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

### 4.2 Restoring from a Backup
To restore database states from a compressed SQL dump:
```bash
# Uncompress and pipe back into the MySQL daemon
gunzip -c database/backups/db_backup_XXXXXXXX_XXXXXX.sql.gz | docker exec -i devop1-mysql mysql -u root -pyour_db_password_here
```

---

## 🧹 5. Scratch Directory Maintenance
Temporary scratch files should never be deleted. To archive them cleanly:
```bash
python local_tools/archive_scratch.py
```
This moves files from `scratch/` into `%USERPROFILE%\keep`, appending a `;<version>` suffix (e.g. `test_filter.py;001`, `test_filter.py;002`) if duplicate filenames exist in the destination.
