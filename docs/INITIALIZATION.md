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

## External example runtime root

Set `AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME` to keep generated example data,
runtime material, secrets, certificates, trust material, and generated configuration
outside the source checkout:

```bash
export AGENT_NEBULA_SECUREAGENTS_EXAMPLES_RUNTIME=/opt/agent-nebula/secureagent-examples
make -C examples/06-nebula-registration-discovery init
```

The example is initialized under:

```text
/opt/agent-nebula/secureagent-examples/06-nebula-registration-discovery/
├── .data/
├── .runtime/
└── config/
```

Generated configuration contains the resolved external `.data` and `.runtime`
paths. Checked-in configuration files are not modified. `make run ...` selects the
generated configuration automatically while the environment variable is set.
Without the variable, initialization and execution retain the local example-directory
layout.
