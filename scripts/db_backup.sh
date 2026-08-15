#!/usr/bin/env bash
# Dump the lyubishchev Neon Postgres DB, gzip it, and encrypt it (GPG symmetric, AES256).
#
# Required environment variables:
#   LYUBISHCHEV_DATABASE_URL  Postgres connection string (never printed).
#   BACKUP_PASSPHRASE         Symmetric encryption passphrase (never printed).
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

# --no-owner --no-privileges: skip Neon-specific roles/grants so the dump
# restores cleanly into any Postgres instance.
pg_dump --no-owner --no-privileges "$LYUBISHCHEV_DATABASE_URL" \
    | gzip \
    | gpg --batch --yes --symmetric --cipher-algo AES256 \
        --pinentry-mode loopback \
        --passphrase "$BACKUP_PASSPHRASE" \
        -o "$out"

echo "Backup written: $out ($(stat -c%s "$out") bytes)"
