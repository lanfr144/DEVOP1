#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🧑‍🔧 Operator Installation Guide

Guidelines for production system administrators.

- **Port Verification**: Ensure host ports `6000`, `4306`, `9080`, `9081`, and `9088` are not already in use.
- **Cluster Deployment**: Deploys the service definitions via K3s manifests:
  ```bash
  kubectl apply -f kubernetes/manifests/
  ```
