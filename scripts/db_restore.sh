#!/usr/bin/env bash
# Restore an encrypted lyubishchev backup (produced by scripts/db_backup.sh)
# into a Postgres database.
#
# Required environment variable:
#   BACKUP_PASSPHRASE  Passphrase the backup was encrypted with (never printed).
#
# Usage:
#   scripts/db_restore.sh <backup-file.sql.gz.gpg> <target-database-url>
#
# WARNING: this replays the full SQL dump into the target database. Point it
# at an empty database (or one you intend to overwrite), never at a live
# database you want to keep.
set -euo pipefail

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <backup-file.sql.gz.gpg> <target-database-url>" >&2
    exit 1
fi

: "${BACKUP_PASSPHRASE:?BACKUP_PASSPHRASE is not set}"

gpg --batch --quiet --decrypt \
        --pinentry-mode loopback \
        --passphrase "$BACKUP_PASSPHRASE" \
        "$1" \
    | gunzip \
    | psql "$2"
