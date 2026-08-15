#!/usr/bin/env bash
# Restore an encrypted lyubishchev backup (produced by scripts/db_backup.sh)
# into a Postgres database.
#
# Required environment variables:
#   TARGET_DATABASE_URL  Postgres connection string of the RESTORE TARGET
#                        (env var, not an argument, to keep it out of argv
#                        and shell history; never printed).
#   BACKUP_PASSPHRASE    Passphrase the backup was encrypted with (never
#                        printed; passed to gpg via fd 3, not argv).
#
# Usage:
#   scripts/db_restore.sh <backup-file.sql.gz.gpg>
#
# WARNING: this replays the full SQL dump into the target database. Point it
# at an empty database (or one you intend to overwrite), never at a live
# database you want to keep. Stops at the first SQL error (ON_ERROR_STOP).
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <backup-file.sql.gz.gpg>  (target DB comes from TARGET_DATABASE_URL)" >&2
    exit 1
fi

: "${TARGET_DATABASE_URL:?TARGET_DATABASE_URL is not set}"
: "${BACKUP_PASSPHRASE:?BACKUP_PASSPHRASE is not set}"

echo "WARNING: replaying full dump '$1' into TARGET_DATABASE_URL; this writes to that database." >&2

gpg --batch --quiet --decrypt \
        --pinentry-mode loopback \
        --passphrase-fd 3 \
        "$1" \
        3<<<"$BACKUP_PASSPHRASE" \
    | gunzip \
    | psql --set ON_ERROR_STOP=1 "$TARGET_DATABASE_URL"
