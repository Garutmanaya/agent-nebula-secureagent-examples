# Agent Nebula OAuth scopes and policy-controlled invocation

These tests require the hosted Agent Nebula services and registered agents. Start with [registration and discovery](NEBULA_REGISTRATION.md); standalone [`examples/`](../examples/README.md) do not require the Registry.

## Security boundaries

```text
Publisher → Provider → registered Agent Card
                             │
A2A client → Registry discovery → advertised OAuth security requirements
                             │
                    OAuth client/token acquisition
                             │
                    A2A request with access token
                             │
              SecureAgent security enforcement
                             │
                     Authorized skill dispatch
```

The **onboarding API key** is for Registry onboarding. An **OAuth access token** is for invoking a protected A2A resource. A **skill scope** constrains which operation the token may authorize. **Policy** adds a separate authorization decision when configured in the hosted deployment. A valid token alone does not establish that every skill is permitted.

Do not place authorization checks inside business skill handlers when the existing security layer owns enforcement. Use the Agent Card as the authoritative source for advertised security requirements and skills.

## Test sequence

| Example | What to test | Required evidence |
|---|---|---|
| [06 — Registration & Discovery](../examples-nebula/06-nebula-registration-discovery/README.md) | Provider registration, discovery, unprotected invocation | Agent found by Registry and skills invoked |
| [07 — OAuth](../examples-nebula/07-nebula-oauth/README.md) | OAuth-protected A2A invocation | Correct token obtained and protected skills succeed |
| [08 — Skill-Level OAuth](../examples-nebula/08-nebula-skill-oauth/README.md) | Distinct scopes per skill | Client selects skill, requests required scope, invocation succeeds |
| [09 — Agent-to-Agent](../examples-nebula/09-nebula-agent-to-agent/README.md) | Discovery and downstream A2A invocation | Orchestrating agent invokes discovered downstream agent |
| [16 — Tasks + HTTPS + OAuth](../examples-nebula/16-a2a-tasks-https-oauth/README.md) | OAuth-protected native Message and Task | Task/artifact retrieval works under configured security |
| [33 — A2UI + Security](../examples-nebula/33-a2ui-security/README.md) | OAuth-protected A2UI over A2A | Authorized UI payload received |
| [34 — Combined](../examples-nebula/34-a2ui-combined/README.md) | Multi-skill, Task/streaming, OAuth, A2UI | Combined scenario succeeds |

Run each example from the repository root using its README prerequisites. For example:

```bash
make init example-08
make run example-08 server
# In another terminal:
make run example-08 client
```

The shared initializer requires provider certificates, trust material, onboarding credentials, and OAuth client material where applicable. Review [initialization](INITIALIZATION.md) and [security](SECURITY.md) before running.

## Authorization acceptance matrix

Use this matrix when validating a hosted policy configuration. **These are intended checks, not claims that the current example clients already automate every negative case.**

| Scenario | Expected outcome |
|---|---|
| Valid token, correct skill scope, policy allows | Invocation succeeds |
| Missing token on protected endpoint | Request rejected before skill execution |
| Valid token, insufficient skill scope | Request rejected before skill execution |
| Valid token and scope, policy denies | Request rejected when policy enforcement is enabled |
| Expired or invalid token | Request rejected before skill execution |

Record the requested skill ID, required scope, token's granted scope (without logging token secrets), policy decision if exposed, and observed response. Do not assert policy enforcement from a successful OAuth-only invocation. A separate automated denial test may be needed after inspecting the actual policy API and current example client behavior.

## Configuration and secrets

Set `NEBULA_URL` and `OAUTH_URL` to the actual hosted service origins in `.env`. Agent Cards and OAuth metadata must advertise compatible URLs and security requirements. Keep onboarding API keys, OAuth private keys, and certificate private keys out of Git. See [configuration](CONFIGURATION.md) and [Example 07](../examples-nebula/07-nebula-oauth/README.md) for the existing OAuth client-registration flow.
