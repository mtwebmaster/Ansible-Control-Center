# Backup Architecture and Recovery Readiness

> **Important:** A verified archive checksum does not demonstrate recoverability. Restore testing is outstanding for this source release.

## Intended workflow

1. Resolve a configured control-plane backup source from the validated inventory.
2. Confirm an explicitly configured backup mount is mounted.
3. Authenticate with a dedicated SSH key and a restricted remote account.
4. Run the remote backup gate/export command.
5. Store an archive under the configured destination, using file locking.
6. Compare local and remote checksums and write a machine-readable status record.
7. Retain archives under the policy implemented by the backup script.

The source includes `backup/backup-daily.sh`, `backup/microk8s-backup-gate`, `backup/microk8s-export-backup`, `backup/setup-remote.yml`, and `config/templates/microk8s-backup.service.in`.

## Service status

`microk8s-backup.service.in` is a **template**, not a ready-to-enable unit. A future installer must resolve placeholders, validate the configured user and paths, and ensure a mounted backup filesystem is available.

## Recovery validation checklist

- [ ] Verify archive accessibility and integrity on an isolated controller
- [ ] Document MicroK8s and dqlite version compatibility
- [ ] Validate the restore procedure away from production
- [ ] Confirm cluster membership and API availability after recovery
- [ ] Verify workloads and persisted application data separately
- [ ] Document recovery time and recovery point objectives
- [ ] Test missing mount, failed SSH, corrupted archive and interrupted transfer cases

Never experiment with datastore restoration on your live HA masters to prove that a backup works.
