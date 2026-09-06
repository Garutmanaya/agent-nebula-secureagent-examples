# 15. OAuth plus TLS

**Category:** Security  
**Status:** CURRENT

## Purpose

Combine listener TLS with OAuth-protected A2A requests.

This example is runnable with the current SecureAgent A2A server adapter.

## Public API demonstrated

```python
agent = SecureAgent(config=HERE / "secureagent.conf")
agent.use_protocol("a2a", role="server", config="a2aserver.conf")

@agent.skill("example.invoke")
def handle(payload):
    return {"received": dict(payload)}
```

The application imports only `agent_nebula_secureagent`. Protocol execution, security, listener lifecycle, and Agent Nebula integration are delegated through SecureAgent to Platform.

## Files

- `main.py` — SecureAgent application code.
- `secureagent.conf` — generic application identity and filesystem roots.
- `a2aserver.conf` — A2A server configuration.
- `Makefile` — standard init/run/clean commands.

## Prerequisites

Python 3.12+, uv, and the sibling `agent-nebula-secureagent` repository. `openssl` is required by initialization.

## Initialize

```bash
make init
```

Initialization creates only local runtime material needed by this example. Generated private keys and secrets are stored below `secrets/` with restrictive permissions and are ignored by Git. Registry API keys are never invented: set `NEBULA_ONBOARDING_API_KEY` or provision `secrets/onboarding-api-key` yourself.

## Run

```bash
make run
```

The configured A2A listener starts on port 9015. Use an official A2A client or a later client example once the SecureAgent client facade is enabled.

## Configuration

`secureagent.conf` contains only generic application settings. Protocol-specific settings remain in `a2aserver.conf`. No Agent Nebula Registry configuration is required.

## Security

This example generates a short-lived local development CA/server identity. It is for local testing only; production certificates must come from the deployment PKI.

## Cleanup

```bash
make clean
```

## Related examples

Return to the [example index](../../README.md) to select the next capability.
