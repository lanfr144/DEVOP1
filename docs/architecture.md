#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Technical Specification & Architecture Spec

This document details the multi-node container architecture of the DEVOP1 system.

## Infrastructure Layout
- **Orchestrator**: Docker Compose (Local Development) / K3s Kubernetes (Production Cluster).
- **Database Backend**: Single-instance MySQL 8.0 containing consolidated tables for Airflow, Flask, and the XAU database.
- **Failover Plan**: Replicated volumes via Longhorn when running in Kubernetes mode.
