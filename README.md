# Agent Nebula SecureAgent Examples

This repository is the learning and reference catalog for `agent-nebula-secureagent`, the protocol-neutral developer interface over Agent Nebula Platform. The examples intentionally keep application code at the SecureAgent boundary: normal examples do not import Platform, the official A2A SDK, or `agent-nebula-sdk` directly.

SecureAgent expresses application intent — business skills, selected protocols, and optional Agent Nebula integration. Platform owns protocol servers/clients, security composition, lifecycle, A2UI, Registry integration, health and other operational plugins. SDK supplies reusable standards/security primitives below Platform.

```text
Application code
      ↓
agent-nebula-secureagent
      ↓
agent-nebula-platform
  ├── A2A
  ├── REST
  ├── MCP
  ├── A2UI
  └── Nebula integration
      ↓
agent-nebula-sdk
```

## Example index

`CURRENT` means the example maps to an adapter available in the current SecureAgent/Platform code. `PLANNED` examples define the intended common API shape but are deliberately not presented as runnable until the corresponding adapter exists. MCP examples are included now so Platform MCP work has concrete SecureAgent acceptance targets.

| # | Example | Category | Status | What it demonstrates |
|---:|---|---|---|---|
| 01 | [Basic A2A server](examples/01-a2a-hello/README.md) | A2A | CURRENT | Minimal SecureAgent A2A server and one business skill. |
| 02 | [Async A2A skill](examples/02-a2a-async-skill/README.md) | A2A | CURRENT | Use an async business handler without protocol-specific code. |
| 03 | [Custom OAuth scope](examples/03-a2a-custom-scope/README.md) | A2A | CURRENT | Declare an explicit skill scope in the SecureAgent API. |
| 04 | [Structured input](examples/04-a2a-structured-input/README.md) | A2A | CURRENT | Consume a mapping payload and validate required business fields. |
| 05 | [Structured result](examples/05-a2a-structured-result/README.md) | A2A | CURRENT | Return structured JSON-compatible data from a skill. |
| 06 | [Application paths](examples/06-a2a-application-paths/README.md) | Configuration | CURRENT | Separate product and runtime roots with application.conf. |
| 07 | [Listener configuration](examples/07-a2a-listener/README.md) | Configuration | CURRENT | Configure A2A host and port in a2aserver.conf. |
| 08 | [TLS A2A server](examples/08-a2a-tls/README.md) | Security | CURRENT | Run the A2A listener with a generated local certificate. |
| 09 | [Provider metadata](examples/09-a2a-provider-metadata/README.md) | A2A | CURRENT | Publish Agent Card provider organization and URL. |
| 10 | [Content modes](examples/10-a2a-content-modes/README.md) | A2A | CURRENT | Publish Agent Card input and output content modes. |
| 11 | [Agent capabilities](examples/11-a2a-capabilities/README.md) | A2A | CURRENT | Publish A2A streaming/push/extended-card capability flags. |
| 12 | [Skill metadata](examples/12-a2a-skill-metadata/README.md) | Skills | CURRENT | Keep SecureAgent skill identity aligned with Agent Card skill metadata. |
| 13 | [OAuth protected A2A](examples/13-a2a-oauth-protected/README.md) | Security | CURRENT | Advertise OAuth2 and let Platform compose protected-resource validation. |
| 14 | [OAuth scoped skill](examples/14-a2a-oauth-scope/README.md) | Security | CURRENT | Use matching SecureAgent and Agent Card OAuth scopes. |
| 15 | [OAuth plus TLS](examples/15-a2a-oauth-tls/README.md) | Security | CURRENT | Combine listener TLS with OAuth-protected A2A requests. |
| 16 | [Nebula registration](examples/16-nebula-registration/README.md) | Nebula | CURRENT | Register an A2A provider with Agent Nebula using separate nebula.conf. |
| 17 | [Nebula TLS identity](examples/17-nebula-mtls/README.md) | Nebula | CURRENT | Configure outbound Registry TLS client identity separately from A2A. |
| 18 | [Nebula plus A2A OAuth](examples/18-nebula-oauth-a2a/README.md) | Nebula | CURRENT | Combine Registry registration with OAuth-protected A2A. |
| 19 | [Documentation metadata](examples/19-a2a-documentation-metadata/README.md) | A2A | CURRENT | Publish Agent Card documentation and icon URLs. |
| 20 | [Agent versioning](examples/20-a2a-versioning/README.md) | A2A | CURRENT | Publish and evolve Agent Card version metadata. |
| 21 | [Platform health](examples/21-a2a-health-ready/README.md) | Platform | CURRENT | Use the Platform-composed server and its operational health integration. |
| 22 | [Production filesystem layout](examples/22-production-layout/README.md) | Configuration | CURRENT | Use explicit /opt-style product and runtime directory concepts with local-safe paths. |
| 23 | [A2A client](examples/23-a2a-client/README.md) | A2A Client | PLANNED | Prepared for the protocol-neutral SecureAgent client adapter. |
| 24 | [OAuth A2A client](examples/24-a2a-oauth-client/README.md) | A2A Client | PLANNED | Prepared for SecureAgent client discovery, DCR, token acquisition and invocation. |
| 25 | [A2A server and client](examples/25-a2a-dual-role/README.md) | A2A | PLANNED | Prepared for composing server and client roles through one SecureAgent facade. |
| 26 | [A2UI surface](examples/26-a2ui-surface/README.md) | A2UI | PLANNED | Prepared for a public SecureAgent A2UI facade over Platform A2UI. |
| 27 | [REST server](examples/27-rest-server/README.md) | REST | PLANNED | Prepared for the common SecureAgent REST server adapter. |
| 28 | [OAuth protected REST](examples/28-rest-oauth/README.md) | REST | PLANNED | Prepared for REST plus Platform OAuth protected-resource composition. |
| 29 | [MCP server](examples/29-mcp-server/README.md) | MCP | PLANNED | Prepared for MCP server support after Platform MCP implementation. |
| 30 | [MCP client](examples/30-mcp-client/README.md) | MCP | PLANNED | Prepared for MCP client support after Platform MCP implementation. |

## Quick start

From a workspace where this repository and `agent-nebula-secureagent` are siblings:

```bash
make install
cd examples/01-a2a-hello
make init
make run
```

Every example uses the same lifecycle:

```bash
make init
make run
make clean
```

## Configuration convention

Configuration remains top-level and responsibility-oriented. We do not introduce a separate `agent-card.json`.

| File | Owner | Purpose |
|---|---|---|
| `application.conf` | Platform | Generic application identity and product/runtime roots. |
| `a2aserver.conf` | A2A | A2A listener, TLS, complete Agent Card, A2A security declarations. |
| `a2aclient.conf` | A2A | A2A client/discovery/security configuration once the SecureAgent client adapter is enabled. |
| `nebula.conf` | Nebula integration | Optional Registry endpoint, TLS and registration lifecycle. |
| `restserver.conf` | REST | Reserved for the common REST adapter. |
| `mcpserver.conf` / `mcpclient.conf` | MCP | Reserved for Platform MCP configuration. |

Only files required by an example are present. Protocol configuration does not leak into `application.conf`, and Registry configuration does not become an A2A requirement.

## Initialization and secrets

Shared scripts under `scripts/` prevent thirty examples from implementing certificate/key handling differently. `make init` creates runtime directories and, where required, generates short-lived local development certificates and OAuth client key material.

The scripts never fabricate externally issued credentials. For Nebula examples, supply the onboarding API key explicitly:

```bash
export NEBULA_ONBOARDING_API_KEY='...provisioned value...'
make init
```

Generated material is Git-ignored. Private-key and secret directories use restrictive permissions. The local CA is for examples only, not production deployment.

## Design rules for examples

1. Application code imports `agent_nebula_secureagent`, not protocol/runtime internals.
2. Configuration stays in the established top-level `.conf` files.
3. One example teaches one primary concept.
4. Security examples do not disable TLS verification.
5. Externally issued secrets are provisioned, never invented.
6. Planned capabilities are labeled explicitly instead of being simulated with fake implementations.
7. Each example README explains purpose, API, files, initialization, configuration, security and cleanup.

## MCP acceptance targets

Examples 29 and 30 intentionally use the same `SecureAgent.use_protocol()` vocabulary as A2A/REST. When MCP is added to Platform, the goal is to activate these examples by implementing the adapter/configuration boundary rather than introducing `SecureMCPAgent` or a second public programming model.
