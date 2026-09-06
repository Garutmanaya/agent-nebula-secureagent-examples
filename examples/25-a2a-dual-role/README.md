# 25. A2A server and client

**Category:** A2A  
**Status:** PLANNED

## Purpose

Prepared for composing server and client roles through one SecureAgent facade.

This is an activation-ready example for a public adapter that is not available yet. It is intentionally marked **PLANNED** and must not be treated as currently runnable.

## Public API demonstrated

```python
agent = SecureAgent()
agent.use_protocol("a2a", role="server", config="a2aserver.conf")

@agent.skill("example.invoke")
def handle(payload):
    return {"received": dict(payload)}
```

The application imports only `agent_nebula_secureagent`. Protocol execution, security, listener lifecycle, and Agent Nebula integration are delegated through SecureAgent to Platform.

## Files

- `main.py` — SecureAgent application code.
- `application.conf` — generic application identity and filesystem roots.
- `a2aserver.conf` — A2A server configuration.
- `Makefile` — standard init/run/clean commands.

## Prerequisites

Python 3.12+, uv, and the sibling `agent-nebula-secureagent` repository.

## Initialize

```bash
make init
```

Initialization creates only local runtime material needed by this example. Generated private keys and secrets are stored below `secrets/` with restrictive permissions and are ignored by Git. Registry API keys are never invented: set `NEBULA_ONBOARDING_API_KEY` or provision `secrets/onboarding-api-key` yourself.

## Run

```bash
make run
```

For PLANNED examples, `make run` is expected to fail explicitly until the corresponding Platform/SecureAgent adapter exists.

## Configuration

`application.conf` contains only generic application settings. Protocol-specific settings remain in `a2aserver.conf`. No Agent Nebula Registry configuration is required.

## Security

This example does not add listener TLS. Use the TLS/security examples before deploying outside a controlled local environment.

## Cleanup

```bash
make clean
```

## Related examples

Return to the [example index](../../README.md) to select the next capability.
