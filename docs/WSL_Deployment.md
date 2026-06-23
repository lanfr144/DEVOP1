#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🐧 WSL Deployment Procedure

Setting up network and storage bounds inside Windows Subsystem for Linux (WSL 2).

## Storage Symlinks
To easily work between Windows files and Linux containers:
```bash
ln -sf /mnt/c/Users/$USER/Documents/DEVOP1/antigravity/DEVOP1 ~/devop1
```

## Docker Socket Configurations
Allow communication between host processes and containers via `docker` group allocation.
