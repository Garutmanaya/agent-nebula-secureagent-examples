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

The suite is intentionally small. Historical examples have been moved to `examples-legacy/` for reference; they are not the supported example/test sequence. New examples are added only after the capability and expected verification matrix are agreed.

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
| 10 | [API-Key Protected Agent](examples/10-a2a-api-key/README.md) | Reserved for API-key endpoint security; current Platform server composition lacks the required external verifier configuration boundary, so no fake runnable example is provided. |
| 11 | [A2A + A2UI v1.0 Acceptance](examples/11-a2a-a2ui/README.md) | Verifies multi-skill A2A selection, A2UI v1.0 Agent Card advertisement, complete `SkillResult` preservation, A2UI DataPart output, and ordinary non-A2UI fallback. |

## Verification philosophy

Examples are executable acceptance tests, not isolated snippets. A client must exercise every feature claimed by its example. Multi-skill examples invoke every advertised skill; multi-binding examples invoke every skill through every binding; security examples validate the configured security path rather than bypassing verification. Assertion failures produce a non-zero client process exit so these scenarios can later be incorporated into integration/CI execution.

The A2A skill model is independent of protocol binding. A skill is registered once through SecureAgent and Platform exposes the same A2A semantics through the configured JSON-RPC, HTTP+JSON, or gRPC interfaces. Binding-specific business handlers are deliberately avoided.

## Quick start

From a workspace where this repository and `agent-nebula-secureagent` are siblings:

```bash
make install
cd examples/01-a2a-hello
make init
make run server
```

Run the client in another terminal:

```bash
make run client
```

Examples 02–04 use the same lifecycle. Example 03 additionally requires the Platform A2A gRPC dependency/extra; Example 04 requires OpenSSL during initialization.

## Configuration boundaries

Configuration remains responsibility-oriented and local to each example for now. `secureagent.conf` contains generic application/runtime settings. `a2aserver.conf` owns the A2A listener and Agent Card. A2A clients use one or more `a2aclient*.conf` files to constrain the transport/security behavior being tested. TLS material is generated under the example directory when required. Configuration externalization is intentionally outside this phase.

## Repository layout

```text
examples/          Current agreed executable scenarios
examples-legacy/   Historical reference examples
docs/              Example authoring/configuration notes
scripts/           Shared initialization and cleanup helpers
```

## Design rules

1. Application code imports `agent_nebula_secureagent`, not Platform or protocol SDK internals.
2. Every current example includes both server and verification client when client/server interaction is part of the capability.
3. Business skills are registered once and remain independent of A2A protocol binding.
4. Clients test all skills/bindings/security behavior claimed by the example.
5. Security verification is never disabled to make an example pass.
6. Externally issued credentials are provisioned rather than fabricated.
7. Historical experiments stay in `examples-legacy/`; they do not expand the supported suite.
