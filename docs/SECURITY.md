# A2A security in SecureAgent examples

SecureAgent integrates the reusable `agent-nebula-sdk` security mechanisms with A2A server/client configuration. A security scheme declared in an Agent Card is metadata; the corresponding runtime authentication and authorization checks must also be configured and exercised. Do not disable certificate verification or skip authorization to make a scenario pass.

## Standalone security verification

| Example | Mechanism | What is tested |
|---|---|---|
| [10](../examples/10-a2a-api-key/README.md) | A2A API key | Header credential authentication. |
| [11](../examples/11-a2a-http-auth/README.md) | HTTP Bearer | Bearer authentication distinct from OAuth. |
| [12](../examples/12-a2a-openid-connect/README.md) | OpenID Connect | Locally provisioned JWT issuer, audience, and signature validation. |
| [13](../examples/13-a2a-mtls/README.md) | Mutual TLS | Client certificate verification at the TLS boundary. |
| [14](../examples/14-a2a-multiple-security/README.md) | Multiple requirements | API key AND HTTP Bearer as a combined requirement. |

These examples do **not** require Agent Nebula Registry registration. HTTPS and TLS transport examples [04](../examples/04-a2a-https/README.md) and [05](../examples/05-a2a-multi-binding-tls/README.md) also run locally.

## Hosted OAuth and policy integration

| Example | Platform-dependent behavior |
|---|---|
| [06](../examples-nebula/06-nebula-registration-discovery/README.md) | Provider registration and Registry discovery. |
| [07](../examples-nebula/07-nebula-oauth/README.md) | OAuth-protected invocation. |
| [08](../examples-nebula/08-nebula-skill-oauth/README.md) | Different OAuth scopes for individual skills. |
| [09](../examples-nebula/09-nebula-agent-to-agent/README.md) | Registry discovery and downstream agent invocation. |
| [16](../examples-nebula/16-a2a-tasks-https-oauth/README.md) | OAuth-protected A2A tasks over HTTPS. |
| [33](../examples-nebula/33-a2ui-security/README.md) | OAuth-protected A2UI transport. |
| [34](../examples-nebula/34-a2ui-combined/README.md) | Combined secured A2A/A2UI capabilities. |

The Agent Card advertises OAuth metadata and per-skill `security_requirements` where configured. Scope enforcement must be verified with the configured authorization server and agent security layer; declaring a scope alone does not grant or enforce access. For hosted policy setup and allow/deny test expectations, see the [OAuth and policy guide](NEBULA_OAUTH_POLICY.md).

## Tunnel boundary

An ngrok **HTTP** endpoint terminates TLS at ngrok. It does not forward the original TLS client certificate to the local A2A server. Keep the mutual-TLS example local unless a separately validated TLS-passthrough setup is used. Do not treat forwarded headers as proof of end-to-end mTLS.
