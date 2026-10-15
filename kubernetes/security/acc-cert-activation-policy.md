# ACC v6.0.1 — Certificate Activation and Rollback Policy

Authors: Jeff Swenson | ChatGPT Pro / OpenAI GPT-6

## Production Credential Management

Active selector:
~/.config/ansible-control-center/token-issuer/current

Version storage:
~/.config/ansible-control-center/token-issuer/versions/

Renewal staging:
~/.config/ansible-control-center/token-issuer/renewal/

## Pre-Activation Requirements

1. Validate active production authentication.
2. Verify staged certificate identity: CN=acc-token-issuer.
3. Verify certificate chain against the Kubernetes CA.
4. Verify TLS client authentication usage.
5. Confirm at least 30 days of certificate validity.
6. Verify staged private key matches certificate.
7. Verify staged certificate can request an acc-k8s-monitor token.
8. Verify staged identity cannot list Kubernetes nodes directly.
9. Verify staged identity cannot issue unrelated service-account tokens.
10. Preserve the previous credential version for rollback.

## Activation Requirements

1. Use a single atomic replacement of the current selector.
2. Resolve both certificate and private key from the same version.
3. Never overwrite or delete an existing version.
4. Serialize activation operations with an exclusive lock.
5. Run an authenticated Kubernetes health test after activation.
6. Verify the certificate expiration checker.
7. Roll back the selector if post-activation validation fails.
8. Preserve the failed candidate for investigation.
9. Record deployment outcome without exposing secrets.

## Rollback Requirements

1. Restore the previously validated credential selector atomically.
2. Verify Kubernetes authentication after restoration.
3. Verify ACC health and monitoring service.
4. Retain old credentials until rollback is no longer required.

## Security

Credential directories: 700
Credential files: 600

Never print, email, log, or distribute private keys or tokens.

## Current Production Certificate

Active version: v1-20261012
Expiration: 2027-01-10 21:54:05 UTC
Scheduled renewal target: 2026-12-01
