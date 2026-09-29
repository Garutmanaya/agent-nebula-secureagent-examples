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

Secrets never belong in checked-in configuration. Private keys, API keys, OAuth material, and similar credentials are stored under `$AGENT_NEBULA_EXAMPLES_ROOT/secrets/example-NN/`. Public certificates and trust material are stored under `$AGENT_NEBULA_EXAMPLES_ROOT/certs/example-NN/`.
