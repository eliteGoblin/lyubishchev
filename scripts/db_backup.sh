#!/usr/bin/env bash
# Dump the lyubishchev Neon Postgres DB, gzip it, and encrypt it (GPG symmetric, AES256).
#
# Required environment variables:
#   LYUBISHCHEV_DATABASE_URL  Postgres connection string (never printed).
#   BACKUP_PASSPHRASE         Symmetric encryption passphrase (never printed;
#                             passed to gpg via fd 3, not argv).
#
# Usage:
#   scripts/db_backup.sh [output-file]
#
# Default output file: lyubishchev-YYYYMMDD.sql.gz.gpg (UTC date, current directory).
# Decrypt/restore with scripts/db_restore.sh.
set -euo pipefail

: "${LYUBISHCHEV_DATABASE_URL:?LYUBISHCHEV_DATABASE_URL is not set}"
: "${BACKUP_PASSPHRASE:?BACKUP_PASSPHRASE is not set}"

out="${1:-lyubishchev-$(date -u +%Y%m%d).sql.gz.gpg}"

# A valid dump of this schema is always larger than this; anything smaller
# means pg_dump produced no real output and the backup must not count.
MIN_BACKUP_BYTES=1000

# --no-owner --no-privileges: skip Neon-specific roles/grants so the dump
# restores cleanly into any Postgres instance.
pg_dump --no-owner --no-privileges "$LYUBISHCHEV_DATABASE_URL" \
    | gzip \
    | gpg --batch --yes --symmetric --cipher-algo AES256 \
        --pinentry-mode loopback \
        --passphrase-fd 3 \
        -o "$out" \
        3<<<"$BACKUP_PASSPHRASE"

size=$(stat -c%s "$out")
if [ "$size" -le "$MIN_BACKUP_BYTES" ]; then
    echo "ERROR: backup $out is only $size bytes (<= $MIN_BACKUP_BYTES); dump looks empty or truncated" >&2
    exit 1
fi

echo "Backup written: $out ($size bytes)"
