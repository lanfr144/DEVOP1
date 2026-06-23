#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# ⚡ Hyper-V Deployment Guide

Deploying node clustering inside Windows Hyper-V hypervisors.

## Setup Requirements
1. **Virtual Switch Manager**: Create an "External Switch" to let VM obtain host IP.
2. **VM Provisioning**: Assign static MAC address to ensure persistent IP naming.
3. **Mount Storage**: Mount shared physical directories via SMB mounts.
