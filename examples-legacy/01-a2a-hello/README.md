# 01. Basic A2A hello — server and client

**Category:** A2A  
**Status:** CURRENT

## Purpose

Minimal end-to-end SecureAgent A2A example with one server, one client, and one
business skill. It verifies that the SecureAgent client facade delegates Agent Card
discovery and message delivery to Agent Nebula Platform and the official A2A Python
SDK rather than implementing A2A transport in application code.

The server advertises the `hello` skill. The client resolves the server Agent Card and
explicitly selects `hello` when sending its message.

## Public API demonstrated

Server:

```python
agent = SecureAgent(config=HERE / "secureagent.conf")
agent.use_protocol("a2a", role="server", config=HERE / "a2aserver.conf")

@agent.skill("hello")
async def hello(payload):
    return {"message": "hello from SecureAgent", "payload": dict(payload)}
```

Client:

```python
agent = SecureAgent(config=HERE / "secureagent.conf")
agent.use_protocol("a2a", role="client", config=HERE / "a2aclient.conf")

card = await agent.resolve_agent_card("http://localhost:9001/")
responses = await agent.send_message_to(
    "http://localhost:9001/",
    data={"name": "Agent Nebula"},
    skill_id="hello",
)
```

The application imports only `agent_nebula_secureagent`. Platform owns Agent Card
resolution, official A2A client construction, request/response wire models, transport,
security integration, and the Agent Nebula skill-selection extension.

## Files

- `main.py` — A2A server and `hello` skill.
- `client.py` — A2A client invocation.
- `secureagent.conf` — shared application/runtime configuration.
- `a2aserver.conf` — server and Agent Card configuration.
- `a2aclient.conf` — client transport configuration.
- `Makefile` — initialization, server/client execution, and cleanup.

## Prerequisites

Python 3.12+, uv, and the sibling `agent-nebula-secureagent` repository.

## Initialize

```bash
make init
```

This introductory HTTP example does not require certificates, OAuth credentials, or
Agent Nebula Registry credentials. Initialization prepares the standard local example
paths used by SecureAgent.

## Run

Start the server in one terminal:

```bash
make run server
```

Then invoke it from another terminal:

```bash
make run client
```

The server listens on `http://localhost:9001/`. The client first resolves the Agent
Card and then sends a data message with `skill_id="hello"`.

## Configuration

`a2aserver.conf` advertises JSON-RPC at `http://localhost:9001/` and the `hello`
skill. `a2aclient.conf` enables JSON-RPC and JSON output for the matching local client.

No configuration externalization is demonstrated in this example.

## Security

This first example intentionally uses local plain HTTP and no application-layer
credentials. TLS, OAuth, mTLS, Registry discovery, and other security scenarios belong
to their dedicated examples.

## Cleanup

```bash
make clean
```

## Related examples

Return to the [example index](../../README.md) to select the next capability.
