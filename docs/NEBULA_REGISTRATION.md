# Agent Nebula: account onboarding and agent registration

This guide applies to [`examples-nebula/`](../examples-nebula/README.md), **not** to standalone [`examples/`](../examples/README.md).

Agent Nebula is the hosted enterprise hub for agent registration, discovery, identity, OAuth and policy services. Begin at [agentnebula.ai](https://agentnebula.ai/). The account ownership model is **Publisher → Provider → Agents**: the publisher account manages providers, and each provider owns its registered agents and associated onboarding/security configuration.

## 1. Create an account and provider

Follow [Example 06, steps 1–2](../examples-nebula/06-nebula-registration-discovery/README.md#1-create-the-publisher-account), which includes UI screenshots for account creation, OTP sign-in, and provider creation. Use the actual hosted platform account rather than a local simulated Registry.

## 2. Prepare the public endpoint

Hosted Registry and Explorer must be able to reach the agent's advertised Agent Card and A2A interface. A laptop-only `localhost` address is **not** reachable from OCI. The planned [Nginx + ngrok integration](NEBULA_NGROK_NGINX.md) is tracked in DOC-P4 and is **not automated by DOC-P3**. Do not register an Agent Card that advertises local-only URLs for hosted discovery/invocation.

The public HTTPS hostname, Agent Card URL, A2A interface URL, certificate SANs, and trusted endpoint identity must agree. The current initializer uses `AGENT_HOSTNAME` for the advertised host; DOC-P4 must verify how public path-based routing is represented before claiming the proxy works end to end.

## 3. Enroll provider certificates

From the repository root, after [environment initialization](INITIALIZATION.md):

```bash
make nebula-pki-init
```

This generates local private keys and certificate-signing requests (CSRs) under `$AGENT_NEBULA_EXAMPLES_ROOT/nebula-certs/`. Follow [Example 06, steps 3–4](../examples-nebula/06-nebula-registration-discovery/README.md#3-generate-the-agent-private-key-and-csr) to submit the CSR in the provider workspace and install issued `server.crt`, `client.crt`, and `trust-bundle.pem`. **Never upload private keys.** Ensure the CSR names the actual endpoint used for the intended TLS connection; the example's default CSR is for local development.

## 4. Create the onboarding credential

In the provider's **Credentials** workspace, create an onboarding API key with the required registration permissions. Follow [Example 06, step 5](../examples-nebula/06-nebula-registration-discovery/README.md#5-generate-the-onboarding-api-key) to store it in `$AGENT_NEBULA_EXAMPLES_ROOT/secrets/onboarding-api-key`, or initialize it using `NEBULA_ONBOARDING_API_KEY` and `make secrets-init`. Do not commit the credential.

The onboarding API key authenticates the registration operation; it is **not** an OAuth access token for invoking A2A skills.

## 5. Configure Registry and initialize

Set `NEBULA_URL` to the deployed Registry origin (for example `https://registry.agentnebula.ai`) and `OAUTH_URL` to the deployed OAuth origin (for example `https://oauth.agentnebula.ai`) in `.env`. Confirm the trust bundle, provider certificates, and public Agent Card URLs before initializing:

```bash
make init example-06
make run example-06 server
```

The provider registers its Agent Card. In another terminal:

```bash
make run example-06 client
```

The client should discover the provider through Registry and invoke `hello`, `echo`, and `add`. See [Example 06, steps 6–7](../examples-nebula/06-nebula-registration-discovery/README.md#6-verify-configuration-before-starting) for the complete prerequisites and acceptance criteria.

## 6. Verify hosted discovery

Confirm that the registered Agent Card advertises a **publicly reachable** HTTPS interface, that the Registry can fetch it, and that hosted Explorer can reach the same interface. Registration alone does not prove reachability or authorization. An unreachable agent must not be represented as a successfully invocable agent.

## Troubleshooting

| Symptom | Check |
|---|---|
| Registry cannot fetch Agent Card | Public DNS/route, ngrok session, Nginx path, advertised Agent Card URL |
| TLS verification failure | Certificate SAN, trusted CA bundle, TLS termination point, configured hostname |
| Registration denied | Publisher/provider ownership, onboarding API key and permissions |
| Agent not discoverable | Registration outcome, Agent Card metadata, liveness and discovery filters |
| Discovered but invocation fails | Advertised A2A interface, transport, OAuth requirements, client trust |

Continue with [OAuth and skill-scope testing](NEBULA_OAUTH_POLICY.md). Detailed proxy automation and verification belong to DOC-P4.
