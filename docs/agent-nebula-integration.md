# Agent Nebula integration prerequisites

Examples in `examples-nebula/` move from standalone A2A interoperability into Agent Nebula enterprise integration. [agentnebula.ai](https://agentnebula.ai/) is the project home.

- **Registry** — registers enterprise agents and their Agent Cards/capabilities and provides discovery to clients. A2A remains the protocol used between agents.
- **OAuth** — protects A2A resources using security requirements advertised in the official Agent Card. Client credential acquisition and token validation are Platform/SDK responsibilities, not business-skill code.
- **Policy** — provides authorization decisions behind the security layer in deployments that enable policy enforcement. Examples do not embed policy rules in SecureAgent handlers.

## Local integration inputs

The examples default to Registry `https://localhost:8000` and OAuth `https://localhost:8092`. Adjust `nebula.conf` and the Agent Card OAuth metadata/token URLs when your deployment differs.

Before `make init` for Registry examples, provide:

```bash
export AGENT_NEBULA_TRUST_BUNDLE_FILE=/path/to/agent-nebula-trust-bundle.pem
export NEBULA_ONBOARDING_API_KEY='...'
```

The shared initializer copies external trust material into the example's managed `.runtime` tree. It never invents Registry credentials. The Registry must also be able to reach and trust the provider's advertised HTTPS Agent Card URL. For non-local deployments, replace the generated development server certificate with an identity trusted by that deployment and advertise a reachable hostname.

OAuth examples additionally generate local EC private keys for RFC 7523 client authentication and DPoP. The OAuth authorization server itself must be running and trusted by the configured Agent Nebula trust bundle.

## Hosted developer onboarding

Use the [registration walkthrough](NEBULA_REGISTRATION.md) and [OAuth/policy test guide](NEBULA_OAUTH_POLICY.md). The [ngrok/Nginx automation](NEBULA_NGROK_NGINX.md) is a separate DOC-P4 task.
