# ACC Architecture

ACC is a controller-side collection of Python and shell utilities with Ansible as the remote execution layer. The terminal interfaces call command and status helpers; configuration defines trusted node identities; exporters and the local SQLite collector support telemetry.

## Main components

| Layer | Files | Responsibility |
|---|---|---|
| User interface | `src/acc-tui`, `src/ansible-menu`, `src/ansible-menu-classic` | Terminal interaction and administrative workflows |
| Configuration | `src/acc_config.py` | Parse and validate ACC settings |
| Authorization | `src/acc_node_policy.py`, `src/acc_cluster_policy.py` | Enforce declared master and worker roles |
| Inventory and HA | `src/acc_ha_inventory.py`, `src/ha-membership-check.py` | Derive HA member addresses and report observed status |
| Monitoring | `monitoring/acc-monitor`, `monitoring/acc-monitor-export` | Restricted telemetry and SQLite incident records |
| Backup | `backup/`, `src/acc_backup_config.py` | Remote restricted backup workflow and mount-aware configuration |
| Security utilities | `src/acc-cert-*`, `src/acc-k8s-health`, `kubernetes/security/` | API and credential-oriented diagnostics |

## Design assumptions

- The controller has its own credentials and Ansible inventory.
- HA operations currently assume three distinct control-plane masters.
- Routine worker maintenance is kept distinct from quorum-aware master maintenance.
- A reported dqlite voter set is not an independently confirmed failover result.
- Workload data and cluster identity may require recovery steps outside the included datastore archive.

## Boundaries

The repository contains an exported application, not a reproducible complete cluster build. Deployment-specific systemd substitutions and external keys/certificates must be provisioned separately. Do not apply the playbooks to live infrastructure before validating their task effects.
