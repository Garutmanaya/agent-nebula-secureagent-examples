# SecureAgent architecture and boundaries

SecureAgent is the application-facing Python API for defining agent skills, selecting roles, and loading configuration. `agent-nebula-platform` integrates FastAPI transport, official A2A Python SDK request handling, and security middleware. `agent-nebula-sdk` provides the reusable security protocol functionality. The A2A SDK owns protocol messages, tasks, artifacts, and wire semantics; example applications should not reimplement these APIs.

```text
Example business skills / example client
                  |
       agent-nebula-secureagent
                  |
        agent-nebula-platform
          /               \
   official A2A SDK     agent-nebula-sdk
          |               |
     A2A protocol      Security protocols
          \               /
           A2A endpoints
                  |
    optional hosted Agent Nebula services
    Registry / OAuth / Policy / Explorer
```

## Protocol responsibilities

- **A2A**: Agent Card, skill metadata, protocol bindings, messages, tasks, artifacts, and streaming.
- **A2UI v1.0**: structured UI payloads delivered through A2A; catalog and renderer negotiation are distinct from transport.
- **Security**: A2A Agent Cards advertise schemes and requirements, while the configured security implementation performs validation and authorization.
- **Agent Nebula Registry**: optional remote registration/discovery and platform integration. It is not required to run standalone examples.

## Example boundaries

`examples/` is local-first; `examples-nebula/` uses Registry and/or hosted OAuth. The shared `examples.json`, `scripts/example-lifecycle.py`, and root Makefile resolve and run both groups without duplicating lifecycle logic. Each example owns its templates and README; generated files belong under the external runtime root.

See [configuration](CONFIGURATION.md), [initialization](INITIALIZATION.md), and the [root README](../README.md).
