The current version is #ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

# Technical Specification & Architecture: DEVOP1 Enterprise PoC

This document serves as the comprehensive blueprint for the DEVOP1 system, designed to fulfill the academic requirements while demonstrating advanced Enterprise DevOps capabilities (High Availability, Disaster Recovery, and Heterogeneous Clustering).

## 1. System Vision & Paradigm
The system is a containerized, cloud-native web application deployed across a highly available Kubernetes cluster. The infrastructure acts as a Proof of Concept (PoC) demonstrating that the DevOps team can orchestrate self-healing pipelines, load balancing, and dynamic failover across a mixed local environment (WSL, Hyper-V, VirtualBox, and native Linux).

## 2. Technology Stack & Infrastructure
| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **User Interface** | React/HTML/CSS | Frontend of the web application. |
| **Backend API** | Flask / Node.js | Backend logic connecting UI to the database. |
| **Database** | MySQL 8.0 | Relational engine. Populated via Python SQLAlchemy as per DEVOP1 Part 4. |
| **Orchestration** | K3s (Kubernetes) | Lightweight K8s distribution optimized for mixed local VM/bare-metal environments. |
| **Load Balancing** | Kubernetes Service | Bare-metal load balancer allowing external access and routing traffic to healthy nodes. <!-- Removed MetalLB & NGINX as they are not used --> |
| **Distributed Storage** | Longhorn | Creates a highly available virtual SAN using local node disks to ensure persistent data replication for MySQL and Zabbix if a node fails. |
| **CI/CD Automation** | Jenkins | Runs as a K8s pod, dynamically provisioning agents to build/push Docker images and deploy. <!-- Removed Helm reference as it is not used --> |
| **Monitoring** | Zabbix | Real-time system health monitoring. Alerts are routed to Email, Discord, and Teams. |
| **Agile Tracking** | Taiga | Integrated with Git webhooks for sprint tracking. |

## 3. High Availability (HA) & Disaster Recovery (DR)
Because this cluster operates across diverse local hardware without a dedicated NAS, the architecture employs the following resilience strategies:
* **Node Redundancy:** Multiple worker nodes are provisioned. If resources max out, new Docker/K3s nodes can be dynamically joined to the cluster.
* **Storage Replication (Longhorn):** Database volumes (MySQL, Zabbix DB) are replicated across at least 3 distinct physical/virtual nodes.
* **Automated Failover:** If a node reboots or crashes, Kubernetes will automatically reschedule the Pods to healthy nodes. Longhorn ensures the new node has immediate access to the replicated persistent data.
* **Disaster Recovery:** CronJobs are configured to take automated snapshots of the Longhorn volumes and dump SQL backups locally.

## 4. Deployment Topology
1. **Initial Development:** Developers use `docker-compose.yml` to spin up isolated local environments for testing.
2. **Production Cluster:** * Jenkins pulls code from the Git repository.
   * Jenkins dynamically provisions a K8s agent pod.
   * Agent builds the Docker image and pushes it to a private registry.
   * Agent deploys updated manifests to the K3s cluster.
3. **Telemetry:** Zabbix agents (SNMP/Active checks) monitor cluster health, node CPU/RAM, and application metrics.