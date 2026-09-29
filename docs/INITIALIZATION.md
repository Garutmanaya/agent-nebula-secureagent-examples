# External environment and lifecycle

Example lifecycle is controlled from the repository root. Individual example directories do not contain Makefiles or generated runtime material.

## Environment root

`AGENT_NEBULA_EXAMPLES_ROOT` selects the external root and defaults to `/opt/nebula/examples`.

```bash
export AGENT_NEBULA_EXAMPLES_ROOT=/opt/nebula/examples
make env-init
```

`env-init` is idempotent and creates `certs/`, `config/`, `data/`, `logs/`, `secrets/`, `tmp/`, and `runtime/`. Existing secrets and certificates are never overwritten merely by environment initialization.

## Example initialization

```bash
make init example-01
```

Initialization reads metadata from `examples.json`, displays the example name/description, creates `runtime/example-01`, and renders the checked-in `examples/01-a2a-hello/config/*.conf` templates into `runtime/example-01/config/`. Generated configuration contains absolute external paths.

Security examples place public certificates/trust material under `certs/example-NN/` and private keys/credentials under `secrets/example-NN/`. Temporary CSRs and other disposable files belong under the example runtime `tmp/` directory.

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
