# Agent Nebula SecureAgent — Examples and Integration Tests

**Build and test standards-based A2A agents locally; then connect them to [Agent Nebula](https://agentnebula.ai) for registration, discovery, OAuth-scoped invocation, and policy-controlled access.**

This repository is the public, executable starting point for `agent-nebula-secureagent`. It contains 34 numbered scenarios, grouped by whether they require the hosted Agent Nebula platform. Start with a standalone example; use the platform-integrated examples to exercise the Registry and security services.

## What is SecureAgent?

`agent-nebula-secureagent` is a configuration-driven Python interface for building A2A agents and clients. Application code defines business skills and selects protocols; the underlying Agent Nebula Platform integration uses the official A2A Python SDK for protocol behavior. The security SDK supplies reusable security mechanisms. **SecureAgent is not the hosted Registry:** local examples do not require an Agent Nebula account.

```text
Application / skills / example clients
                  |
       agent-nebula-secureagent
                  |
        agent-nebula-platform
             /           \
     official A2A SDK   agent-nebula-sdk (security)
                  |
           A2A interfaces
                  |
     optional: Agent Nebula Registry / OAuth / Policy / Explorer
```

### A2A and A2UI

**A2A** defines Agent Cards, skills, messages, tasks, artifacts, streaming, and interoperable protocol bindings (JSON-RPC, HTTP+JSON, and gRPC where configured). SecureAgent examples use the official A2A SDK instead of implementing a second wire protocol. **A2UI v1.0** carries structured, renderer-consumable UI updates over A2A; the A2UI examples cover catalogs, forms, actions, tables, charts, tasks, and streaming. A2UI does not replace A2A transport or authentication.

See [configuration](docs/CONFIGURATION.md), [A2UI integration](docs/nebula-a2ui-integration.md), and the [example catalogs](#example-catalogs).

## Configuration-driven development

Each example keeps checked-in templates under `config/`. `make init example-NN` resolves templates into an **external runtime directory**, rather than modifying source configuration or committing secrets.

| File / input | Responsibility |
|---|---|
| `config/secureagent.conf` | Application/runtime identity, logging, and general runtime settings. |
| `config/a2aserver.conf` | A2A listener, TLS settings, Agent Card, supported interfaces, advertised skills, and security schemes. |
| `config/a2aclient.conf` (or `a2aclient*.conf`) | A2A client connection and transport/security settings. |
| `config/nebula.conf` (when present) | Agent Nebula Registry connection, trust, and registration behavior. |
| `config/a2ui.conf` (when present) | A2UI catalog support and negotiation preferences. |
| `presentation.json` (when present) | Example-owned A2UI presentation data/catalog references. |
| `.env` (from `.env.example`) | Shared runtime root, hostname, and external service URLs; not credentials. |
| `examples.json` | Authoritative example directory, initialization mode, certificate profile, and runnable processes. |

Not every example uses every file. For the exact configuration lifecycle, see [configuration](docs/CONFIGURATION.md) and [initialization](docs/INITIALIZATION.md).

## A2A authentication and security

The reusable security layer supports the A2A authentication mechanisms demonstrated here: **API key, HTTP Bearer, OpenID Connect, mutual TLS, and OAuth 2.0**, including combinations of requirements. The examples distinguish **advertising a security scheme in an Agent Card** from **validating credentials at the server**. OAuth scopes can restrict individual skills; Agent Nebula integration adds hosted registration and policy-controlled workflows. These are different responsibilities, and neither should be bypassed for a passing test.

Use [standalone security examples 10–14](examples/README.md) to test local mechanisms, and [Agent Nebula OAuth/skill-scope examples 07–08](examples-nebula/README.md) for platform-integrated flows. Read the [security guide](docs/SECURITY.md) for the example coverage and boundaries. The standard ngrok HTTP endpoint is **not** a replacement for end-to-end client-certificate mTLS; example 13 runs locally.

## Quick start: no Registry account required

Prerequisites: Python/`uv`, plus any dependencies called out by the individual example README. From the repository root:

```bash
make install
make env-init
make list
make init example-01
make run example-01 server
```

In a second terminal:

```bash
make run example-01 client
```

To remove the example's disposable runtime snapshot: `make clean example-01`. Certificates and shared secrets are preserved. The default external runtime root is `/opt/agent-nebula/examples`; override it with `AGENT_NEBULA_EXAMPLES_ROOT` as needed. See [standalone setup and catalog](examples/README.md).

## Example catalogs

### Standalone — [`examples/`](examples/README.md)

Run without Agent Nebula Registry registration, Nginx, or ngrok. Local TLS/security prerequisites vary by example.

| # | Example | Demonstrates |
|---:|---|---|
| 01 | [A2A Hello](examples/01-a2a-hello/README.md) | Minimal A2A client/server smoke test. Resolves the Agent Card and invokes one `hello` skill through JSON-RPC over local HTTP. |
| 02 | [A2A Multi-Skill](examples/02-a2a-multiskill/README.md) | Establishes multi-skill as the normal SecureAgent model. Advertises three skills and makes the client explicitly select, invoke, and validate every skill. |
| 03 | [A2A Multi-Binding](examples/03-a2a-multi-binding/README.md) | Registers the same skills once and verifies every skill independently over JSON-RPC, HTTP+JSON, and gRPC using binding-specific client instances. |
| 04 | [A2A HTTPS](examples/04-a2a-https/README.md) | Retains the multi-skill model and adds certificate-verified HTTPS using a generated local CA and server identity; the client tests every skill without disabling TLS verification. |
| 05 | [A2A Multi-Binding + TLS](examples/05-a2a-multi-binding-tls/README.md) | Verifies every skill over JSON-RPC/HTTPS, HTTP+JSON/HTTPS, and gRPC/TLS. |
| 10 | [API-Key Protected Agent](examples/10-a2a-api-key/README.md) | Verifies an A2A `APIKeySecurityScheme` using an externally configured header credential and native SDK invocation. |
| 11 | [HTTP Authentication](examples/11-a2a-http-auth/README.md) | Verifies `HTTPAuthSecurityScheme` with an opaque Bearer credential; HTTP Bearer syntax remains distinct from OAuth. |
| 12 | [OpenID Connect](examples/12-a2a-openid-connect/README.md) | Verifies `OpenIdConnectSecurityScheme` with a locally provisioned test JWT and issuer/audience/signature validation. |
| 13 | [Mutual TLS](examples/13-a2a-mtls/README.md) | Verifies `MutualTlsSecurityScheme` with mandatory client-certificate authentication at the TLS boundary. |
| 14 | [Multiple Security Schemes](examples/14-a2a-multiple-security/README.md) | Verifies compound A2A security by requiring API key AND HTTP Bearer in one `SecurityRequirement`. |
| 15 | [Native A2A Tasks](examples/15-a2a-tasks/README.md) | Verifies native `a2a-sdk` Message and Task execution, artifacts, `get_task()`, and `list_tasks()` with application-owned Task lifecycle. |
| 17 | [Native A2A Artifacts](examples/17-a2a-artifacts/README.md) | Verifies native artifact IDs, names, Parts, and TaskStore persistence through `get_task()`. |
| 18 | [Native A2A Streaming](examples/18-a2a-streaming/README.md) | Verifies `streaming=true` with native Task, status, and artifact update events through `Client.send_message()`. |
| 19 | [Native A2A Push Notifications](examples/19-a2a-push-notifications/README.md) | Verifies native push configuration create/get/list/delete operations and callback delivery. |
| 20 | [Native A2A Extended Agent Card](examples/20-a2a-extended-agent-card/README.md) | Verifies authenticated native `get_extended_agent_card()` retrieval of a distinct richer Agent Card. |
| 21 | [Combined Native A2A Capabilities](examples/21-a2a-combined/README.md) | Combines native streaming, Task/artifact, push-notification, and Extended Agent Card capabilities in one scenario. |
| 22 | [A2UI Basic](examples/22-a2ui-basic/README.md) | Verifies an application-owned A2UI v1.0 Basic Catalog presentation transported through native A2A. |
| 23 | [A2UI Rich](examples/23-a2ui-rich/README.md) | Verifies an application-owned Agent Nebula Rich Catalog presentation over native A2A. |
| 24 | [A2UI Catalog Negotiation](examples/24-a2ui-catalog-negotiation/README.md) | Verifies AgentCard A2UI catalog advertisement and per-turn renderer capability negotiation. |
| 25 | [A2UI Multi-Skill Results](examples/25-a2ui-skill-result/README.md) | Verifies multiple native A2A skills independently producing application-owned A2UI results. |
| 26 | [A2UI Actions](examples/26-a2ui-actions/README.md) | Verifies browser A2UI actions and synchronized state through the native A2A execution path. |
| 27 | [A2UI Forms](examples/27-a2ui-forms/README.md) | Verifies browser-edited form state and submission through native A2A execution. |
| 28 | [A2UI Tables](examples/28-a2ui-tables/README.md) | Verifies a Rich Catalog DataTable driven by application data. |
| 29 | [A2UI Charts](examples/29-a2ui-charts/README.md) | Verifies a Rich Catalog BarChart driven by application data. |
| 30 | [A2UI Multi-Skill](examples/30-a2ui-multi-skill/README.md) | Verifies AgentCard-driven skill selection with different A2UI surfaces per skill. |
| 31 | [A2UI + Native Tasks](examples/31-a2ui-tasks/README.md) | Verifies a native A2A Task whose artifact carries an application-owned A2UI presentation. |
| 32 | [A2UI + Native Streaming](examples/32-a2ui-streaming/README.md) | Verifies native A2A streaming artifact updates producing visible incremental A2UI updates. |

### Agent Nebula integrated — [`examples-nebula/`](examples-nebula/README.md)

These examples use Agent Nebula registration/discovery and, where applicable, hosted OAuth and skill scopes. For hosted Explorer to reach a developer-run agent, its advertised Agent Card and A2A endpoints must be publicly reachable. The planned Nginx + ngrok setup is **DOC-P4**, not part of this documentation patch.

| # | Example | Demonstrates |
|---:|---|---|
| 06 | [Agent Nebula Registration & Discovery](examples-nebula/06-nebula-registration-discovery/README.md) | Registers the provider with Agent Nebula Registry, discovers it by capability, and invokes every skill through the discovered record. |
| 07 | [Agent Nebula OAuth](examples-nebula/07-nebula-oauth/README.md) | Adds OAuth-protected A2A invocation after Registry discovery and verifies every skill. |
| 08 | [Skill-Level OAuth](examples-nebula/08-nebula-skill-oauth/README.md) | Verifies deterministic skill selection and distinct least-privilege OAuth scopes per skill. |
| 09 | [Agent-to-Agent](examples-nebula/09-nebula-agent-to-agent/README.md) | Runs a dual-role SecureAgent that serves A2A while discovering and invoking a downstream Registry provider. |
| 16 | [Native A2A Tasks + HTTPS + OAuth](examples-nebula/16-a2a-tasks-https-oauth/README.md) | Combines native Message/Task execution with Agent Nebula registration/discovery, HTTPS, and OAuth. |
| 33 | [A2UI + HTTPS + OAuth](examples-nebula/33-a2ui-security/README.md) | Verifies existing Agent Nebula HTTPS/OAuth security protecting native A2A carrying A2UI. |
| 34 | [A2UI Combined](examples-nebula/34-a2ui-combined/README.md) | Combines HTTPS/OAuth, multi-skill dispatch, native Task/streaming, and A2UI without new protocol abstractions. |

## Agent Nebula Enterprise Registry Hub

[Agent Nebula](https://agentnebula.ai) provides a hosted environment for publishing and discovering A2A agents and testing security-controlled invocation. The platform includes an **A2A Registry**, **Playground**, **Explorer**, **OAuth services**, **policy services**, and **account management**.

The account ownership model is **Publisher → Provider → Agents**: a publisher account manages providers; a provider publishes and manages agent registrations. An Agent Card describes the agent's capabilities, endpoints, and advertised security requirements. Registry discovery and Explorer invocation require reachability and appropriate authorization; successful registration alone does not prove the agent is reachable.

Start at [agentnebula.ai](https://agentnebula.ai) to create an account. Then follow the existing [Agent Nebula integration guide](docs/agent-nebula-integration.md) and [registration/discovery example](examples-nebula/06-nebula-registration-discovery/README.md) for provider onboarding, certificate enrollment, onboarding credentials, registration, discovery, and invocation. [Platform-integrated examples](examples-nebula/README.md) provide the ordered test path. The full hosted onboarding and Nginx/ngrok automation are DOC-P3 and DOC-P4 deliverables.

## Developer documentation

- [Standalone setup and complete catalog](examples/README.md)
- [Agent Nebula setup and complete catalog](examples-nebula/README.md)
- [Architecture and repository boundaries](docs/ARCHITECTURE.md)
- [Configuration reference](docs/CONFIGURATION.md)
- [Security and authentication examples](docs/SECURITY.md)
- [Initialization and external filesystem](docs/INITIALIZATION.md)
- [Adding an example](docs/ADDING_AN_EXAMPLE.md)
- [Agent Nebula integration](docs/agent-nebula-integration.md)
- [A2UI integration](docs/nebula-a2ui-integration.md)

## Repository conventions

Examples are executable acceptance scenarios, not illustrative snippets: clients must exercise the capabilities advertised by their example and exit nonzero on assertion failure. Preserve numbered example IDs and the shared `make init/run/clean example-NN` lifecycle. Application code stays at the SecureAgent public boundary; do not reimplement A2A protocol handling, duplicate security enforcement, or commit credentials, certificates, or runtime output.

### Agent Nebula hosted onboarding guides

- [Account, provider, certificates, agent registration, and discovery](docs/NEBULA_REGISTRATION.md)
- [OAuth-scoped skills and policy-controlled invocation](docs/NEBULA_OAUTH_POLICY.md)
- [Nginx + ngrok integration status](docs/NEBULA_NGROK_NGINX.md)

For publicly reachable registered agents, see [Nginx + ngrok setup](docs/NEBULA_NGROK_NGINX.md).
