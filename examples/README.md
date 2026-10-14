# Standalone SecureAgent examples

These examples run locally without Agent Nebula Registry registration, Nginx, or ngrok. They cover A2A protocol bindings, native tasks, security schemes, and A2UI. Some scenarios require locally generated certificates, secrets, or browser dependencies; check each linked README.

From the repository root, install dependencies and initialize the external runtime once:

```bash
make install
make env-init
```

Then start a server in one terminal and its client in another:

```bash
make list
make init example-01
make run example-01 server
```

In another terminal:

```bash
make run example-01 client
```

For local TLS/security examples, `make pki-init` and `make secrets-init` may be required; consult the example README before initialization. For certificate and environment preparation, see [initialization](../docs/INITIALIZATION.md) and the [root README](../README.md).

## Catalog

| ID | Example | Description |
|---|---|---|
| example-01 | [A2A Hello](01-a2a-hello/README.md) | a minimal SecureAgent A2A server and client exchanging a message through JSON-RPC. |
| example-02 | [A2A Multi-Skill](02-a2a-multiskill/README.md) | one SecureAgent advertising multiple A2A skills and explicit client-side skill invocation. |
| example-03 | [A2A Multi-Binding](03-a2a-multi-binding/README.md) | the same A2A skills over JSON-RPC, HTTP+JSON, and gRPC protocol bindings. |
| example-04 | [A2A HTTPS](04-a2a-https/README.md) | certificate-verified A2A over HTTPS using generated development TLS material. |
| example-05 | [A2A Multi-Binding + TLS](05-a2a-multi-binding-tls/README.md) | JSON-RPC/HTTPS, HTTP+JSON/HTTPS, and gRPC/TLS with the same A2A skills. |
| example-10 | [API Key Security](10-a2a-api-key/README.md) | A2A v1.0 API Key Security security example. |
| example-11 | [HTTP Authentication](11-a2a-http-auth/README.md) | A2A v1.0 HTTP Authentication security example. |
| example-12 | [OpenID Connect](12-a2a-openid-connect/README.md) | A2A v1.0 OpenID Connect security example. |
| example-13 | [Mutual TLS](13-a2a-mtls/README.md) | A2A v1.0 Mutual TLS security example. |
| example-14 | [Multiple Security Schemes](14-a2a-multiple-security/README.md) | A2A v1.0 Multiple Security Schemes security example. |
| example-15 | [Native A2A Tasks](15-a2a-tasks/README.md) | Native a2a-sdk multi-skill Message and Task execution through SecureAgent. |
| example-17 | [Native A2A Artifacts](17-a2a-artifacts/README.md) | Native a2a-sdk artifact creation and TaskStore persistence. |
| example-18 | [Native A2A Streaming](18-a2a-streaming/README.md) | Native a2a-sdk streaming Task status and artifact events. |
| example-19 | [Native A2A Push Notifications](19-a2a-push-notifications/README.md) | Native A2A push notification configuration CRUD and callback delivery. |
| example-20 | [Native A2A Extended Agent Card](20-a2a-extended-agent-card/README.md) | Authenticated native get_extended_agent_card retrieval of a richer Agent Card. |
| example-21 | [Combined Native A2A Capabilities](21-a2a-combined/README.md) | Combined native A2A streaming, Task, artifact, push-notification, and Extended Agent Card capabilities. |
| example-22 | [A2UI Basic](22-a2ui-basic/README.md) | Application-owned A2UI v1.0 Basic Catalog presentation over native a2a-sdk. |
| example-23 | [A2UI Rich](23-a2ui-rich/README.md) | Application-owned A2UI v1.0 Agent Nebula Rich Catalog presentation over native a2a-sdk. |
| example-24 | [A2UI Catalog Negotiation](24-a2ui-catalog-negotiation/README.md) | A2UI v1.0 Agent Card capability advertisement and per-turn renderer catalog negotiation. |
| example-25 | [A2UI Skill Result](25-a2ui-skill-result/README.md) | Multiple native A2A skills independently produce application-owned A2UI v1.0 results. |
| example-26 | [A2UI Actions on Native A2A](26-a2ui-actions/README.md) | Browser A2UI v1.0 action and synchronized data model over native a2a-sdk execution. |
| example-27 | [A2UI Forms on Native A2A](27-a2ui-forms/README.md) | Browser-edited A2UI v1.0 form state and submission over native a2a-sdk execution. |
| example-28 | [A2UI Tables](28-a2ui-tables/README.md) | Structured tabular presentation |
| example-29 | [A2UI Charts](29-a2ui-charts/README.md) | Chart presentation driven by application data |
| example-30 | [A2UI Multi-Skill](30-a2ui-multi-skill/README.md) | Different skills producing different A2UI surfaces |
| example-31 | [A2UI + Native A2A Tasks](31-a2ui-tasks/README.md) | Native a2a-sdk Task artifact carrying an application-owned A2UI v1.0 presentation. |
| example-32 | [A2UI + Native A2A Streaming](32-a2ui-streaming/README.md) | Native a2a-sdk streaming Task artifact carrying incremental A2UI v1.0 updates. |
