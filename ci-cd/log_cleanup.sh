#!/bin/bash
#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# -----------------------------------------------------------------------------
# Enterprise Log Rotation & Cleanup Utility (Bash Script)
# -----------------------------------------------------------------------------
# This script rotates and cleans log files to prevent storage exhaustion.
# It employs the safe 'copytruncate' strategy to avoid disrupting active write
# descriptors of running services.
# -----------------------------------------------------------------------------

# set -e: exits script immediately if any command exits with a non-zero code.
# set -u: exits if any uninitialized variable is referenced.
# set -o pipefail: pipeline commands return status of last command that failed.
set -euo pipefail

# Directories containing system logs to be scanned
LOG_DIRS=("/app/logs" "/var/log")
# Maximum size file threshold before rotation gets triggered (50 MB)
MAX_SIZE="50M"
# Keep files for at most 7 days
RETENTION_DAYS=7
# Rotation suffix generator: YYYYMMDD_HHMMSS
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

log_message() {
    """Helper function to print standardized timestamped logs to stdout."""
    echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] $1"
}

log_message "Starting enterprise log maintenance..."

for DIR in "${LOG_DIRS[@]}"; do
    if [ -d "$DIR" ]; then
        log_message "Scanning directory: $DIR"
        
        # 1. Rotate active logs that exceed MAX_SIZE using copytruncate.
        # find searches for files ending in '.log' whose size is greater than MAX_SIZE.
        find "$DIR" -type f -name "*.log" -size +"$MAX_SIZE" | while read -r logfile; do
            archive_name="${logfile}.${TIMESTAMP}"
            
            # A. Copy current contents of log to a temporary backup file.
            cp "$logfile" "$archive_name"
            
            # B. Truncate the active log to 0 bytes safely.
            # Running processes keep writing to the same file descriptor uninterrupted.
            truncate -s 0 "$logfile"
            
            # C. Compress the rotated backup in the background using gzip.
            # The ampersand '&' runs the compression asynchronously.
            gzip "$archive_name" &
            
            log_message "Rotated and truncated: $logfile -> ${archive_name}.gz"
        done
        
        # 2. Cleanup old rotated logs to free up space.
        # Find and remove rotated log archives (.log.TIMESTAMP) older than RETENTION_DAYS.
        find "$DIR" -type f -name "*.log.*" -mtime +$RETENTION_DAYS -exec rm -f {} \; -print | while read -r deleted; do
            log_message "Deleted old archive: $deleted"
        done
        
        # Find and remove compressed log archives (.gz) older than RETENTION_DAYS.
        find "$DIR" -type f -name "*.gz" -mtime +$RETENTION_DAYS -exec rm -f {} \; -print | while read -r deleted; do
            log_message "Deleted old compressed archive: $deleted"
        done
    else
        log_message "Warning: Directory $DIR does not exist, skipping."
    fi
done

# 'wait' suspends shell execution until all background gzip processes complete.
wait

log_message "Log maintenance completed successfully."