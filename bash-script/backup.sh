#!/bin/bash

read -p "Enter the directory you want to back up: " SOURCE_DIR

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Directory '$SOURCE_DIR' does not exist"
    exit 1
fi

read -p "Enter the directory where you want to save the backup: " BACKUP_DIR

if [ -z "$BACKUP_DIR" ]; then
    echo "No destination directory provided"
    exit 1
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)

ARCHIVE_NAME="backup_${TIMESTAMP}.tar.gz"

mkdir -p "${BACKUP_DIR}"

echo "Starting backup of ${SOURCE_DIR} to ${BACKUP_DIR}/${ARCHIVE_NAME}..."
tar -czf "${BACKUP_DIR}/${ARCHIVE_NAME}" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")"

if [ $? -eq 0 ]; then
    echo "Backup completed successfully"
else
    echo "Backup failed"
fi

find "${BACKUP_DIR}" -type f -name "backup_*.tar.gz" -mtime +7 -delete
echo "Old backups removed"