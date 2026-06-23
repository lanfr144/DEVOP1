#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 🔔 Zabbix Monitoring and Alert Configuration

Setting up alerts, active agents, and triggers.

## Trapper Item Registration
- Import the template `template_xau_app.xml`.
- Key items registered: `xau.error` and `xau.trace` on host `xau-app`.

## Webhook Routing
Alerts trigger calls to:
- `ci-cd/discord_notifier.py`
- `ci-cd/teams_notifier.py`
- `ci-cd/mail_notifier.py`
