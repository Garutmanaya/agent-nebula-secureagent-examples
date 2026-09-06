# Initialization contract

All example initialization is delegated to `scripts/init-example.sh` and `scripts/common.sh`.

## Generated directories

- `.runtime/`: temporary CSRs and local runtime files.
- `certs/`: generated public certificates.
- `secrets/`: private keys and externally provisioned secrets; mode 0700 directory, 0600 generated keys.
- `trust/`: local development CA/trust bundles.

## Modes

- `basic`: paths only.
- `tls`: paths + local CA + server certificate.
- `oauth`: TLS material + local OAuth client signing key.
- `nebula`: TLS material + optional onboarding API-key provisioning from the environment.
- `oauth-nebula`: combines OAuth and Nebula requirements.
- `planned`: paths only; no fake credentials or protocol material.

The scripts are deliberately development-only. Production deployments should use the Agent Nebula deployment/PKI process and external secret stores.
