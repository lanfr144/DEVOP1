#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🔔 Changing Webhooks, Emails, and Toggles

Instructions to edit destinations and enable/disable alert routing.

## 1. Modifying Webhooks & Email Destinations
Open the `.env` file in your workspace root:
- Change Discord destination: edit `DISCORD_WEBHOOK_URL`
- Change Teams destination: edit `TEAMS_WEBHOOK_URL`
- Change Email destination: edit `EMAIL_USER`

## 2. Enabling/Disabling Alert Routes
To enable/disable routing, change the toggles in `.env` to `true` or `false`:
- **Mail**: `ENABLE_MAIL=false`
- **Discord**: `ENABLE_DISCORD=false`
- **Teams**: `ENABLE_TEAMS=false`
