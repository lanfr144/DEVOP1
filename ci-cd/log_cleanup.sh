#!/bin/bash
# Antigravity log cleanup script
# Deletes old log files to prevent disk space exhaustion

# Clean application logs older than 7 days
if [ -d "/app/logs" ]; then
    find /app/logs -type f -name "*.log" -mtime +7 -exec rm -f {} \;
fi

# Clean system logs older than 30 days
find /var/log -type f -name "*.log" -mtime +30 -exec rm -f {} \;
find /var/log -type f -name "*.gz" -mtime +30 -exec rm -f {} \;

echo "Log cleanup executed at $(date)"
