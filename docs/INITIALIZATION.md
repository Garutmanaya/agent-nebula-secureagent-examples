# External environment and lifecycle

Example lifecycle is controlled from the repository root. Individual example directories do not contain Makefiles or generated runtime material.

## Environment root

`AGENT_NEBULA_EXAMPLES_ROOT` selects the external root and defaults to `/opt/agent-nebula/examples`.

```bash
export AGENT_NEBULA_EXAMPLES_ROOT=/opt/nebula/examples
make env-init
```

`env-init` is idempotent and creates `certs/`, `nebula-certs/`, `config/`, `data/`, `logs/`, `secrets/`, `tmp/`, and `runtime/`. Existing secrets and certificates are never overwritten merely by environment initialization.

## Example initialization

```bash
make init example-01
```

Initialization reads metadata from `examples.json`, displays the example name/description, creates `runtime/example-01`, and renders the checked-in `examples/01-a2a-hello/config/*.conf` templates into `runtime/example-01/config/`. Generated configuration contains absolute external paths.

Local development PKI lives under top-level `certs/`. Agent Nebula enrollment and approved PKI lives under top-level `nebula-certs/`. Non-PKI credentials live under top-level `secrets/`. `make init` copies the profile selected by `examples.json` into the disposable runtime snapshot.

## Running

```bash
make run example-01 server
make run example-01 client
```

The selected process is validated against `examples.json`. The runner sets `AGENT_NEBULA_EXAMPLE_CONFIG_DIR` to the initialized external configuration directory before executing the Python application.

## Cleaning

```bash
make clean example-01
make clean all
```

Clean removes only `$AGENT_NEBULA_EXAMPLES_ROOT/runtime/example-NN`. It deliberately preserves external certificates and secrets.

## Bulk initialization

```bash
make init all
```

This initializes every catalog entry. Reserved/planned examples create their external runtime boundary but do not fabricate unsupported protocol/security material.

## Shared PKI and secrets

The external environment uses one shared PKI and one shared secrets directory for all examples. Do not create per-example directories under top-level `certs/` or `secrets/`.

```bash
export AGENT_NEBULA_EXAMPLES_ROOT=/opt/agent-nebula/examples
make env-init
make pki-init
make secrets-init
make init example-01
```

`pki-init` creates `ca.crt`, `ca.key`, `server.crt`, `server.key`, `client.crt`, `client.key`, and `trust-bundle.pem` under the shared `certs/` directory. `init` copies shared certificate and secret material into `runtime/example-NN/certs/` and `runtime/example-NN/secrets/`. Runtime cleanup does not modify the shared material.

For Agent Nebula connected examples, place the Agent Nebula trust certificate at `certs/agent-nebula-ca.crt`. `secrets-init` can provision `onboarding-api-key` from `NEBULA_ONBOARDING_API_KEY` and `oauth-client-id` from `NEBULA_OAUTH_CLIENT_ID`; it also creates the shared OAuth authentication and DPoP development keys when absent.

## Agent Nebula PKI enrollment

```bash
make env-init
make nebula-pki-init
```

`nebula-pki-init` creates `nebula-certs/server.key`, `server.csr`, `client.key`, and `client.csr`. It does not self-sign or fabricate Agent Nebula certificates. Submit the CSRs manually through Agent Nebula and place the approved `server.crt`, `client.crt`, and `trust-bundle.pem` back under `nebula-certs/`.

Examples with `certificate_profile: "nebula"` fail initialization until the approved material is present. Initialization copies `nebula-certs/` to `runtime/example-NN/certs/`. Other examples copy the local `certs/` profile.
