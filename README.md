# Ansible Control Center (ACC)

Ansible Control Center is a self-hosted management platform for Linux servers and MicroK8s clusters.

Developed by Jeff Swenson with assistance from OpenAI GPT-6.

## Features

- Terminal-based server management dashboard
- Ansible inventory and node administration
- Restricted worker maintenance workflows
- MicroK8s HA monitoring and health checks
- SQLite-based monitoring and alert collection
- MicroK8s backup and integrity verification utilities
- Kubernetes API certificate and authentication checks
- Configuration-driven cluster role authorization

## Release status

**Experimental source release — not production-ready.**

This repository contains working components exported from an existing deployment, but the portable installation process and complete disaster-recovery workflow have not been independently validated.

Do not replace an existing production ACC installation with this version.

## Requirements

- Linux management workstation
- Python 3
- Ansible and OpenSSH
- SSH access to managed Linux hosts
- MicroK8s for Kubernetes-specific functionality
- Three HA control-plane nodes for the current HA policy
- A separate mounted backup filesystem for backup operations

## Configuration

Start with:

`config/examples/config.json.example`

Copy and adapt it to:

`~/.config/ansible-control-center/config.json`

Alternatively, select a configuration file using the `ACC_CONFIG` environment variable.

Set your own inventory path, SSH keys, management username, master and worker names, monitoring options, and backup destination.

Never commit private inventory files, credentials, certificates, SSH keys, or operational backups.

## Source layout

| Directory | Purpose |
|---|---|
| `src/` | Management interface, configuration, HA and security utilities |
| `ansible/` | Playbooks and monitoring deployment files |
| `monitoring/` | Telemetry collector and restricted exporter |
| `backup/` | Backup scripts, remote backup gate and service files |
| `kubernetes/` | Kubernetes security and authentication utilities |
| `systemd/` | Monitoring service definitions |
| `config/` | Example configuration and installation templates |

## Security

ACC uses explicit node-role authorization to protect HA control-plane nodes from ordinary worker maintenance operations.

The exported source includes safeguards for unknown inventory hosts, duplicate addresses, invalid master configuration, and restricted backup access.

These safeguards have passed focused offline tests, but a complete security review has not been performed.

## Backup safety

Backups require a configured destination beneath an explicitly mounted backup filesystem.

The backup script includes file locking, SSH host-key verification, and archive integrity checks.

A successful backup is not proof of recoverability. Perform a tested restore before relying on ACC backups for disaster recovery.

## Installation

A production-ready portable installer is not yet available.

For source review and development, use the example configuration and inspect the individual scripts before running them.

Do not directly install the legacy systemd service or enable the backup timer without completing the configuration and mount-safety validation.

## License

Released under the MIT License. See [LICENSE](LICENSE).

## Disclaimer

Use at your own risk. Administrative functions may alter remote systems and Kubernetes workloads.
