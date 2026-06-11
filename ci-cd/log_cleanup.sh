#!/bin/bash
#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
set -euo pipefail

# ==============================================================================
# Enterprise Log Rotation & Cleanup Utility
# ==============================================================================
# This script implements a "copytruncate" log rotation strategy.
# It safely archives and compresses log files without breaking active file 
# descriptors held by running processes, ensuring space is actually freed
# and new logs continue to be written correctly.
# ==============================================================================

LOG_DIRS=("/app/logs" "/var/log")
MAX_SIZE="50M"
RETENTION_DAYS=7
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

log_message() {
    echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] $1"
}

log_message "Starting enterprise log maintenance..."

for DIR in "${LOG_DIRS[@]}"; do
    if [ -d "$DIR" ]; then
        log_message "Scanning directory: $DIR"
        
        # 1. Rotate active logs that exceed MAX_SIZE using copytruncate
        find "$DIR" -type f -name "*.log" -size +"$MAX_SIZE" | while read -r logfile; do
            archive_name="${logfile}.${TIMESTAMP}"
            
            # Copy the current content to an archive file
            cp "$logfile" "$archive_name"
            
            # Truncate the original file to 0 bytes safely. 
            # This frees disk space while keeping the inode intact for the running process.
            truncate -s 0 "$logfile"
            
            # Compress the archived log in the background
            gzip "$archive_name" &
            
            log_message "Rotated and truncated: $logfile -> ${archive_name}.gz"
        done
        
        # 2. Cleanup old rotated logs to free up space
        # Remove archived .gz or .log files older than the retention policy
        find "$DIR" -type f -name "*.log.*" -mtime +$RETENTION_DAYS -exec rm -f {} \; -print | while read -r deleted; do
            log_message "Deleted old archive: $deleted"
        done
        
        find "$DIR" -type f -name "*.gz" -mtime +$RETENTION_DAYS -exec rm -f {} \; -print | while read -r deleted; do
            log_message "Deleted old compressed archive: $deleted"
        done
    else
        log_message "Warning: Directory $DIR does not exist, skipping."
    fi
done

# Wait for any background gzip processes to finish
wait

log_message "Log maintenance completed successfully."