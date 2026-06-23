#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🗑️ Uninstall Guide: Project Antigravity

Procedures to completely remove all components, containers, and data.

## De-provisioning Steps
1. **Shutdown Containers**:
   ```bash
   docker compose down -v
   ```
2. **Remove Git Filters**:
   ```bash
   git config --unset filter.ident-dynamic.clean
   git config --unset filter.ident-dynamic.smudge
   ```
3. **Delete WSL Instance**:
   ```powershell
   wsl --unregister B1AI_DEVOP1
   ```
