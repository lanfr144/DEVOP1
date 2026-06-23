#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# ⚙️ Environment Configuration Guide

This document describes the environment variables required for running the project.

## Variable Definitions
- `PORT_OFFSET`: Offset applied to host ports to prevent collisions.
- `ENABLE_MAIL`, `ENABLE_DISCORD`, `ENABLE_TEAMS`: Alerts toggles (`true` or `false`).
- `EMAIL_USER`, `EMAIL_PASS`: SMTP server login credentials.
- `DISCORD_WEBHOOK_URL`, `TEAMS_WEBHOOK_URL`: Targets for channel notifications.

> [!WARNING]
> Never check real passwords into Git! Place them only in your local `.env` file.
