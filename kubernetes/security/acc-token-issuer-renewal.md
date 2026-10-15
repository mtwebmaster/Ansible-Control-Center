# ACC v6.0.1 — Kubernetes Token Issuer Renewal

Certificate identity: CN=acc-token-issuer
Kubernetes CSR: acc-token-issuer-v1

Certificate host: fedora-server1
Certificate directory:
~/.config/ansible-control-center/token-issuer/

## Certificate Schedule

Expiration: 2027-01-10 21:54:05 UTC
Expiration (Montana): 2027-01-10 14:54:05 MST

Renewal target: 2026-12-01
Warning threshold: 2026-12-11
Critical threshold: 2027-01-03

## Renewal Procedure

1. Generate a new private key and CSR with CN=acc-token-issuer.
2. Submit the new CSR to Kubernetes.
3. Verify the requested certificate identity and permissions.
4. Approve the CSR using Kubernetes administrative credentials.
5. Retrieve the signed client certificate.
6. Verify certificate identity and public/private key matching.
7. Test restricted Kubernetes token issuance.
8. Replace the active certificate and key using a validated rollback procedure.
9. Run acc-k8s-health and acc-monitor --once.
10. Verify Kubernetes API monitoring and incident resolution.

## Security

Never expose or distribute private keys.

The issuer may create short-lived tokens only for:
acc-monitoring/acc-k8s-monitor

## ACC Monitoring

Incident ID: security:issuer-certificate
Monitoring service: acc-monitor.service
Monitoring timer: acc-monitor.timer
Certificate checker: ~/.local/bin/acc-cert-health
