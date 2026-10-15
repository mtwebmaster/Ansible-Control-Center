#!/usr/bin/env bash
set -euo pipefail
umask 077
ACC_BACKUP_CONFIG="${ACC_BACKUP_CONFIG:-}"

if [[ -z "$ACC_BACKUP_CONFIG" ]]; then
    SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
    ACC_BACKUP_CONFIG="$SCRIPT_DIR/../src/acc_backup_config.py"
fi

[[ -f "$ACC_BACKUP_CONFIG" ]] || {
    echo "ACC backup configuration reader not found" >&2
    exit 1
}

backup_setting() {
    python3 "$ACC_BACKUP_CONFIG" "$1"
}

ROOT="$(backup_setting directory)"
KEY="$(backup_setting ssh_key)"
HOST="$(backup_setting host)"
MOUNT_POINT="$(backup_setting mount_point)"
REMOTE_USER="$(backup_setting ssh_user)"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
DEST="$ROOT/dqlite/microk8s-$STAMP.tar.gz"
LOG="$ROOT/logs/backup-$STAMP.log"
STATUS="$ROOT/backup-status.json"
mkdir -p "$ROOT/dqlite" "$ROOT/logs" "$ROOT/weekly" "$ROOT/monthly"
exec 9>"$ROOT/.backup.lock"
flock -n 9 || { echo 'Backup already running'; exit 1; }
MOUNT=$(findmnt -n -M "$MOUNT_POINT" -o SOURCE || true)
[[ -n "$MOUNT" ]] || {
    echo "Required backup filesystem is not mounted: $MOUNT_POINT" >&2
    exit 1
}
ssh_opts=(-i "$KEY" -o BatchMode=yes -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=15)
remote() { ssh "${ssh_opts[@]}" "$REMOTE_USER@$HOST" "$1"; }
write_status() {
  python3 - "$STATUS" "$1" "$2" "$3" <<'PY'
import json,os,sys,tempfile,datetime
path,state,archive,message=sys.argv[1:]
obj={'status':state,'archive':archive,'message':message,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
fd,tmp=tempfile.mkstemp(dir=os.path.dirname(path),prefix='.status-',text=True)
try:
    with os.fdopen(fd,'w') as f: json.dump(obj,f,indent=2);f.write('\n')
    os.chmod(tmp,0o600);os.replace(tmp,path)
finally:
    if os.path.exists(tmp):os.unlink(tmp)
PY
}
fail() { write_status failed '' "See $LOG"; echo "Backup failed: $LOG" >&2; }
trap fail ERR
exec > >(tee -a "$LOG") 2>&1
printf 'Beginning MicroK8s backup %s\n' "$STAMP"
remote backup
TMP="$DEST.partial"
trap 'rm -f -- "${TMP:-}"' EXIT
remote fetch > "$TMP"
[[ -s "$TMP" ]]
gzip -t "$TMP"
tar -tzf "$TMP" >/dev/null
REMOTE_SHA=$(remote sha256 | awk '{print $1}')
LOCAL_SHA=$(sha256sum "$TMP" | awk '{print $1}')
[[ "$REMOTE_SHA" =~ ^[0-9a-f]{64}$ && "$REMOTE_SHA" == "$LOCAL_SHA" ]] || { echo 'SHA256 mismatch' >&2; exit 1; }
chmod 600 "$TMP"
mv -f "$TMP" "$DEST"
printf '%s  %s\n' "$LOCAL_SHA" "$(basename "$DEST")" > "$DEST.sha256"
chmod 600 "$DEST.sha256"
# Hardlink copies on the same drive; keep matching checksums alongside each.
DOW=$(date +%u); DAY=$(date +%d)
if [[ "$DOW" == 7 ]]; then ln "$DEST" "$ROOT/weekly/$(basename "$DEST")"; cp "$DEST.sha256" "$ROOT/weekly/"; fi
if [[ "$DAY" == 01 ]]; then ln "$DEST" "$ROOT/monthly/$(basename "$DEST")"; cp "$DEST.sha256" "$ROOT/monthly/"; fi
# Keep seven newest daily files, four weekly and three monthly.
for rule in 'dqlite 7' 'weekly 4' 'monthly 3'; do
  read -r SUB KEEP <<< "$rule"
  mapfile -t NAMES < <(find "$ROOT/$SUB" -maxdepth 1 -type f -name 'microk8s-*.tar.gz' -printf '%f\n' | sort -r)
  if (( ${#NAMES[@]} > KEEP )); then
    for f in "${NAMES[@]:KEEP}"; do rm -f -- "$ROOT/$SUB/$f" "$ROOT/$SUB/$f.sha256"; done
  fi
done
find "$ROOT/logs" -maxdepth 1 -type f -name 'backup-*.log' -mtime +30 -delete
write_status ok "$DEST" 'SHA256 verified, gzip verified'
trap - ERR
printf 'SUCCESS: %s (%s bytes)\n' "$DEST" "$(stat -c %s "$DEST")"
