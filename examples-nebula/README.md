# Agent Nebula integration examples

These examples exercise hosted Agent Nebula registration/discovery and, where configured, OAuth-scoped A2A invocation. They are **not** required to run the [standalone examples](../examples/README.md). The public endpoint setup using Nginx + ngrok is planned for DOC-P4; do not assume it is automated yet.

## Platform onboarding and test path

1. Create a publisher account at [agentnebula.ai](https://agentnebula.ai) and create a provider. The ownership hierarchy is **Publisher → Provider → Agents**.
2. Follow the [registration and onboarding guide](../docs/NEBULA_REGISTRATION.md) and [Example 06](06-nebula-registration-discovery/README.md) for provider enrollment, certificate signing, onboarding credentials, registration, and discovery.
3. Make the agent's advertised Agent Card and A2A interface endpoints reachable from the hosted Registry/Explorer. A public ngrok domain alone does not rewrite Agent Card URLs; that integration is planned for DOC-P4.
4. Configure `.env` from [`.env.example`](../.env.example), including `NEBULA_URL` and `OAUTH_URL`; use the actual hosted service URLs and trusted certificates.
5. Prepare runtime and certificates with `make env-init`, `make nebula-pki-init`, and the applicable enrollment/secret steps documented by the example. **Do not generate substitute hosted credentials locally.**
6. Run registration/discovery first (06), then OAuth (07), skill-scoped OAuth (08), and the remaining integrated scenarios as needed. The OAuth-scope example is the entry point for least-privilege skill invocation; policy behavior must be validated against the configured hosted service.

From the repository root, after completing the example's prerequisites:

```bash
make install
make list
make init example-06
make run example-06 server
```

In a second terminal:

```bash
make run example-06 client
```

See [configuration](../docs/CONFIGURATION.md), [security](../docs/SECURITY.md), and [initialization](../docs/INITIALIZATION.md). The example-specific README is authoritative for required certificates, secrets, and processes (Example 09 includes multiple agents).

## Catalog

| ID | Example | Description |
|---|---|---|
| example-06 | [Agent Nebula Registration & Discovery](06-nebula-registration-discovery/README.md) | Agent Nebula provider registration, Registry discovery, and invocation through the discovered A2A Agent Card. |
| example-07 | [Agent Nebula OAuth](07-nebula-oauth/README.md) | OAuth-protected A2A invocation after Agent Nebula Registry discovery. |
| example-08 | [Skill-Level OAuth](08-nebula-skill-oauth/README.md) | skill-level OAuth scopes and least-privilege authorization for multiple A2A skills. |
| example-09 | [Agent-to-Agent](09-nebula-agent-to-agent/README.md) | a dual-role SecureAgent serving A2A while discovering and invoking a downstream Agent Nebula provider. |
| example-16 | [Native A2A Tasks + HTTPS + OAuth](16-a2a-tasks-https-oauth/README.md) | Agent Nebula registration/discovery and OAuth-protected HTTPS native a2a-sdk Message and Task execution. |
| example-33 | [A2UI + HTTPS + OAuth](33-a2ui-security/README.md) | Existing Agent Nebula HTTPS/OAuth security protecting native A2A carrying A2UI v1.0. |
| example-34 | [A2UI Combined](34-a2ui-combined/README.md) | HTTPS + OAuth + multi-skill native Task/streaming + A2UI without new protocol abstractions. |

## Hosted integration guides

- [Publisher/provider onboarding, certificates, registration, and discovery](../docs/NEBULA_REGISTRATION.md)
- [OAuth scopes, policy boundaries, and authorization acceptance tests](../docs/NEBULA_OAUTH_POLICY.md)
- [Nginx + ngrok public endpoint prerequisite (DOC-P4 pending)](../docs/NEBULA_NGROK_NGINX.md)

## Public endpoint automation

For hosted Registry/Explorer access, configure the [Nginx + ngrok public endpoint](../docs/NEBULA_NGROK_NGINX.md). Standalone examples do not require this setup.
