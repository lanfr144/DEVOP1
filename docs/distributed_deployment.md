#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🌐 Distributed Deployment Guide

This procedure details the deployment of DEVOP1 onto a fresh virtual/physical computer which has access only to the Git repository.

## Step-by-Step Deployment
1. **Install Prerequisites**: Ensure Git, Docker, and Docker Compose v2 are installed.
2. **Clone the repository**:
   ```bash
   git clone https://github.com/lanfr144/DEVOP1.git
   cd DEVOP1
   ```
3. **Setup environment**:
   ```bash
   cp .env.sample .env
   # Edit the passwords and webhook parameters
   ```
4. **Deploy Containers**:
   ```bash
   docker compose up -d
   ```
