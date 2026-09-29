# Configuration model

Each example owns its checked-in configuration templates under its own `config/` directory. For example:

```text
examples/01-a2a-hello/
├── config/
│   ├── secureagent.conf
│   ├── a2aserver.conf
│   └── a2aclient.conf
├── main.py
├── client.py
└── README.md
```

Checked-in templates are immutable inputs. `make init example-01` creates resolved runtime copies under `$AGENT_NEBULA_EXAMPLES_ROOT/runtime/example-01/config/`. Application code uses those generated files through `AGENT_NEBULA_EXAMPLE_CONFIG_DIR`.

The examples preserve the SecureAgent/Platform configuration boundary. `secureagent.conf` is generic. Protocol configuration belongs to the protocol. `nebula.conf` is optional and independent. A2A Agent Card data remains part of `a2aserver.conf`; no duplicate `agent-card.json` is introduced.

Secrets never belong in checked-in configuration. Shared non-PKI credentials are stored under `$AGENT_NEBULA_EXAMPLES_ROOT/secrets/`. Local development certificates/keys are stored under `certs/`. Agent Nebula enrollment keys/CSRs and approved certificates/trust are stored separately under `nebula-certs/`.

## Runtime certificate and secret paths

Checked-in templates use logical `certs/...` and `secrets/...` paths. During `make init example-NN`, lifecycle initialization rewrites them to absolute paths inside that example's runtime snapshot. A2A TLS uses `runtime/example-NN/certs/trust-bundle.pem`; Agent Nebula connected examples use the approved `runtime/example-NN/certs/trust-bundle.pem` copied from `nebula-certs/`.

A2A server Agent Cards must define a non-empty absolute `agent_card.url` pointing to the well-known Agent Card location. Supported interfaces remain separate transport endpoints. The existing examples are normalized to this contract.

## Certificate profiles

`examples.json` declares `certificate_profile` for each example. `local` copies the shared development `certs/` directory; `nebula` copies `nebula-certs/`. This keeps Agent Nebula-issued identities separate from the self-managed development CA while preserving one runtime contract: applications always read certificates from `runtime/example-NN/certs/`.
