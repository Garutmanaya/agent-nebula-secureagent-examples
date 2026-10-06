# Agent Nebula SecureAgent Examples

This repository is the executable learning and integration suite for `agent-nebula-secureagent`. Each current example is a complete client/server scenario that verifies a defined SecureAgent capability end to end. Application code stays at the SecureAgent public boundary; examples do not reimplement protocol transport, A2A wire models, security negotiation, or Platform lifecycle behavior.

SecureAgent expresses application intent: business skills, protocol roles, and configuration selection. Agent Nebula Platform owns A2A transports, official A2A SDK integration, deterministic skill dispatch, TLS/security composition, lifecycle, and later Agent Nebula Registry integration. `agent-nebula-sdk` remains the low-level standards/security layer beneath Platform.

```text
Application / example
        ↓
agent-nebula-secureagent
        ↓
agent-nebula-platform
        ↓
official protocol SDKs + agent-nebula-sdk
```

The suite is intentionally scoped to the maintained executable scenarios. New examples are added only after the capability and expected verification matrix are agreed.

## Current examples

| # | Example | Description |
|---:|---|---|
| 01 | [A2A Hello](examples/01-a2a-hello/README.md) | Minimal A2A client/server smoke test. Resolves the Agent Card and invokes one `hello` skill through JSON-RPC over local HTTP. |
| 02 | [A2A Multi-Skill](examples/02-a2a-multiskill/README.md) | Establishes multi-skill as the normal SecureAgent model. Advertises three skills and makes the client explicitly select, invoke, and validate every skill. |
| 03 | [A2A Multi-Binding](examples/03-a2a-multi-binding/README.md) | Registers the same skills once and verifies every skill independently over JSON-RPC, HTTP+JSON, and gRPC using binding-specific client instances. |
| 04 | [A2A HTTPS](examples/04-a2a-https/README.md) | Retains the multi-skill model and adds certificate-verified HTTPS using a generated local CA and server identity; the client tests every skill without disabling TLS verification. |
| 05 | [A2A Multi-Binding + TLS](examples/05-a2a-multi-binding-tls/README.md) | Verifies every skill over JSON-RPC/HTTPS, HTTP+JSON/HTTPS, and gRPC/TLS. |
| 06 | [Agent Nebula Registration & Discovery](examples/06-nebula-registration-discovery/README.md) | Registers the provider with Agent Nebula Registry, discovers it by capability, and invokes every skill through the discovered record. |
| 07 | [Agent Nebula OAuth](examples/07-nebula-oauth/README.md) | Adds OAuth-protected A2A invocation after Registry discovery and verifies every skill. |
| 08 | [Skill-Level OAuth](examples/08-nebula-skill-oauth/README.md) | Verifies deterministic skill selection and distinct least-privilege OAuth scopes per skill. |
| 09 | [Agent-to-Agent](examples/09-nebula-agent-to-agent/README.md) | Runs a dual-role SecureAgent that serves A2A while discovering and invoking a downstream Registry provider. |
| 10 | [API-Key Protected Agent](examples/10-a2a-api-key/README.md) | Verifies an A2A `APIKeySecurityScheme` using an externally configured header credential and native SDK invocation. |
| 11 | [HTTP Authentication](examples/11-a2a-http-auth/README.md) | Verifies `HTTPAuthSecurityScheme` with an opaque Bearer credential; HTTP Bearer syntax remains distinct from OAuth. |
| 12 | [OpenID Connect](examples/12-a2a-openid-connect/README.md) | Verifies `OpenIdConnectSecurityScheme` with a locally provisioned test JWT and issuer/audience/signature validation. |
| 13 | [Mutual TLS](examples/13-a2a-mtls/README.md) | Verifies `MutualTlsSecurityScheme` with mandatory client-certificate authentication at the TLS boundary. |
| 14 | [Multiple Security Schemes](examples/14-a2a-multiple-security/README.md) | Verifies compound A2A security by requiring API key AND HTTP Bearer in one `SecurityRequirement`. |
| 15 | [Native A2A Tasks](examples/15-a2a-tasks/README.md) | Verifies native `a2a-sdk` Message and Task execution, artifacts, `get_task()`, and `list_tasks()` with application-owned Task lifecycle. |
| 16 | [Native A2A Tasks + HTTPS + OAuth](examples/16-a2a-tasks-https-oauth/README.md) | Combines native Message/Task execution with Agent Nebula registration/discovery, HTTPS, and OAuth. |
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
| 33 | [A2UI + HTTPS + OAuth](examples/33-a2ui-security/README.md) | Verifies existing Agent Nebula HTTPS/OAuth security protecting native A2A carrying A2UI. |
| 34 | [A2UI Combined](examples/34-a2ui-combined/README.md) | Combines HTTPS/OAuth, multi-skill dispatch, native Task/streaming, and A2UI without new protocol abstractions. |

## Verification philosophy

Examples are executable acceptance tests, not isolated snippets. A client must exercise every feature claimed by its example. Multi-skill examples invoke every advertised skill; multi-binding examples invoke every skill through every binding; security examples validate the configured security path rather than bypassing verification. Assertion failures produce a non-zero client process exit so these scenarios can later be incorporated into integration/CI execution.

The A2A skill model is independent of protocol binding. A skill is registered once through SecureAgent and Platform exposes the same A2A semantics through the configured JSON-RPC, HTTP+JSON, or gRPC interfaces. Binding-specific business handlers are deliberately avoided.

## Quick start

All lifecycle commands run from the repository root. Example source stays in the repository; generated configuration, certificates, secrets, data, logs, and temporary runtime state live under an external filesystem root.

```bash
make install
export AGENT_NEBULA_EXAMPLES_ROOT=/opt/agent-nebula/examples   # optional; this is the default
make env-init
make list
make init example-01
make run example-01 server
```

Run the client in another terminal:

```bash
make run example-01 client
```

Clean only disposable runtime state with:

```bash
make clean example-01
```

Certificates and secrets are intentionally preserved by `clean`.

## External environment contract

`AGENT_NEBULA_EXAMPLES_ROOT` selects the external environment root and defaults to `/opt/agent-nebula/examples`. `make env-init` creates the durable top-level filesystem without overwriting existing operator-provided material:

```text
/opt/agent-nebula/examples/
├── certs/                 # local development PKI
├── nebula-certs/          # Agent Nebula enrollment/approved PKI
├── config/
├── data/
├── logs/
├── secrets/
├── tmp/
└── runtime/
    └── example-01/
        ├── config/
        ├── data/
        ├── logs/
        └── tmp/
```

`certs/` contains the shared local development PKI created by `make pki-init`. `nebula-certs/` contains Agent Nebula enrollment keys/CSRs and the certificates/trust bundle approved by Agent Nebula. `secrets/` contains shared non-PKI credentials. The runtime tree is disposable; these durable sources are not.

## Configuration boundaries

Checked-in configuration remains self-contained with each example under `examples/<name>/config/`. These files are source templates and are never modified in place. `make init example-NN` copies and resolves them into `$AGENT_NEBULA_EXAMPLES_ROOT/runtime/example-NN/config/`, including external data/runtime, certificate, and secret paths. Application code receives the generated configuration directory through `AGENT_NEBULA_EXAMPLE_CONFIG_DIR`.

`secureagent.conf` contains generic application/runtime settings. `a2aserver.conf` owns the A2A listener and Agent Card. A2A clients use one or more `a2aclient*.conf` files. `nebula.conf` remains optional and independent.

## Lifecycle catalog

`examples.json` is the authoritative lifecycle catalog. It defines each example's directory, display name, what the example demonstrates, initialization mode, and runnable processes. `make init` and `make run` display this metadata before execution. Add lifecycle behavior through the shared scripts rather than per-example Makefiles.

## Repository layout

```text
examples/          Current executable scenarios; each owns its config/ templates
examples.json      Example identity, description, initialization, and process catalog
docs/              Example authoring/configuration/lifecycle documentation
scripts/           Shared external environment and lifecycle implementation
```

## Design rules

1. Application code imports `agent_nebula_secureagent`, not Platform or protocol SDK internals.
2. Every current example includes both server and verification client when client/server interaction is part of the capability.
3. Business skills are registered once and remain independent of A2A protocol binding.
4. Clients test all skills/bindings/security behavior claimed by the example.
5. Security verification is never disabled to make an example pass.
6. Externally issued credentials are provisioned rather than fabricated.
7. Maintained examples stay focused on standards-based A2A/A2UI behavior and documented Agent Nebula extensions.

### Shared external environment

Example source code and checked-in configuration templates stay in this repository. Runtime state, certificates, and secrets live under `AGENT_NEBULA_EXAMPLES_ROOT` (default `/opt/agent-nebula/examples`).

```bash
make env-init
make pki-init              # standalone/local TLS examples
make nebula-pki-init       # generate Agent Nebula enrollment keys + CSRs
make secrets-init       # secured examples; imports supported values from environment
make init example-01
make run example-01 server
make run example-01 client
make clean example-01
```

`make pki-init` creates one development CA plus shared server/client certificates and keys under `certs/`. Every `make init example-NN` copies the current shared `certs/` and `secrets/` contents into that example's disposable `runtime/example-NN/` tree. `make clean` removes only the example runtime snapshot and never removes shared certificates or secrets.

## Agent Nebula certificate profile

Agent Nebula connected examples use a separate PKI profile from the local development CA. Run `make nebula-pki-init` to create `nebula-certs/server.key`, `server.csr`, `client.key`, and `client.csr`. Submit the CSRs through Agent Nebula, then install the approved `server.crt`, `client.crt`, and `trust-bundle.pem` in `nebula-certs/`.

`examples.json` selects `certificate_profile: "nebula"` for Agent Nebula registration/OAuth examples. `make init` copies that profile into `runtime/example-NN/certs/`; standalone examples continue to receive the local `certs/` profile. Application configuration always uses runtime-local `certs/...` paths.

## Environment URLs

All examples use a common external runtime root, and Agent Nebula-integrated examples use two canonical service URLs. Copy the
checked-in template once and update it for the deployment:

```bash
cp .env.example .env
```

```dotenv
AGENT_NEBULA_EXAMPLES_ROOT=/opt/agent-nebula/examples
NEBULA_URL=https://YOUR_HOSTNAME:8000
OAUTH_URL=https://YOUR_HOSTNAME:8092
```

`AGENT_NEBULA_EXAMPLES_ROOT` is the external root for shared certificates, secrets, and per-example runtime state; child paths are derived from it rather than configured independently. `NEBULA_URL` renders `[nebula] base_url`. `OAUTH_URL` renders both OAuth metadata
and token endpoints, keeping the RFC 7523 client-assertion audience aligned with
the authorization server hostname. Shell-exported values override `.env`.

