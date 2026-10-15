# Development Setup and Installation Status

> **No production-ready installer is included.** This page explains safe source evaluation and the remaining installation work; it is not a deployment runbook.

## Prerequisites

Use a Linux development workstation with Python 3, Bash and Git. Ansible and OpenSSH are required for inventory resolution and remote operations. MicroK8s operations additionally require access to a suitably configured MicroK8s environment.

## Clone and configure

```bash
git clone https://github.com/mtwebmaster/Ansible-Control-Center.git
cd Ansible-Control-Center
mkdir -p "$HOME/.config/ansible-control-center"
cp config/examples/config.json.example "$HOME/.config/ansible-control-center/config.json"
chmod 600 "$HOME/.config/ansible-control-center/config.json"
```

Edit the configuration and supply a private Ansible inventory. Do not use the fictional example hosts as if they were real targets.

## Safe static checks

```bash
python3 -m compileall -q src monitoring kubernetes/security
bash -n backup/backup-daily.sh
ansible-playbook --syntax-check -i 'localhost,' backup/setup-remote.yml
```

The syntax-only Ansible check can warn that the example's remote host is not in the localhost inventory. These checks do not start services, run playbooks, or validate all behavior.

## What is not automated yet

- Installation of the Python helper modules where the launcher and monitoring service can import them
- Substitution of `@...@` placeholders in the backup systemd template
- Correct identity, key, account and mount provisioning for backup operations
- Controller-side service/user setup and clean uninstall
- End-to-end validation of CLI/TUI entrypoints and all privileged workflows

**Do not enable the supplied backup timer or execute remote provisioning scripts from a fresh clone without reviewing and testing them first.**
