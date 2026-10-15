# Security Model and Review Checklist

ACC includes privileged operations. A syntax check or passing unit test is not a certification that all operations are safe.

## Designed protections

- Inventory and configuration define master and worker identity.
- Workers are explicitly authorized for worker-specific maintenance; unknown targets are denied.
- Master configuration must be complete and non-overlapping.
- Disruptive actions use explicit confirmation prompts in relevant menus.
- Backup access uses SSH host-key checking, a dedicated restricted account and a forced-command remote gate.

## Before public deployment

1. Audit every menu route to privileged subprocess, `run`, `adhoc`, and Kubernetes API actions.
2. Review all Ansible YAML for `become`, sudoers rules, file permissions and targeted hosts.
3. Replace deployment-specific scripts and service assumptions with tested installer logic.
4. Test accidental and intentional authorization failures in isolation.
5. Confirm inventory and monitoring inputs cannot change role decisions unexpectedly.
6. Add automated scans for credentials, keys, certificates, runtime state and embedded network metadata.
7. Confirm secret-bearing subprocess output never reaches public logs.
8. Verify backup mount and SSH restrictions on an isolated test host.

Do not publish private keys, credentials, private token issuers, production backup files, sensitive logs or infrastructure maps in issues and pull requests. Restrict repository access if a full public-source review has not been completed.
