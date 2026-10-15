# Configuration Reference

Copy `config/examples/config.json.example` to `~/.config/ansible-control-center/config.json` and secure it with `chmod 600`. Some utilities support overriding that location with `ACC_CONFIG`.

| Key | Purpose |
|---|---|
| `inventory` | Ansible inventory file |
| `ssh_key` | Primary Ansible SSH key |
| `management_user` | Remote management identity |
| `microk8s.masters` | Exactly three named control-plane hosts for current HA policy |
| `microk8s.workers` | Named workers allowed in worker-specific workflows |
| `microk8s.dqlite_port` | HA datastore port (example 19001) |
| `microk8s.api_port` | Kubernetes API port (example 16443) |
| `monitoring.ssh_user` | Restricted monitoring account |
| `monitoring.ssh_key` | Key used for monitoring SSH collection |
| `monitoring.collection_interval_seconds` | Collector interval |
| `backups.directory` | Backup destination directory |
| `backups.mount_point` | Mount point required for backup destination |
| `backups.remote_host` | Named master used as backup source |
| `backups.ssh_user` | Restricted remote account; presently expected to be `microbackup` |
| `backups.ssh_key` | Dedicated backup SSH identity |

The backup destination must be beneath the configured mount point. **This condition alone does not establish that the filesystem is mounted:** actual backup execution must verify the mount before writing archives.

The hostnames in the example are placeholders. Real cluster identities, private IP addresses, passwords, SSH material and credential files belong outside the public Git repository.
