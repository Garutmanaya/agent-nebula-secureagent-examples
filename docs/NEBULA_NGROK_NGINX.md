# Public Agent Nebula examples: Nginx + ngrok

This setup exposes only `examples-nebula/` over a single assigned ngrok development domain. Standalone `examples/` do not require a tunnel.

## Prerequisites

- A persistent ngrok development domain from your ngrok account and an installed/authenticated ngrok agent.
- Nginx installed on the developer host.
- Local HTTPS agent servers running on the ports declared in `examples.json` and their `a2aserver*.conf` files.
- A local CA bundle that validates those servers' certificates. Do **not** disable upstream certificate verification.
- Agent Nebula enrollment, Registry and OAuth prerequisites: [registration](NEBULA_REGISTRATION.md) and [OAuth/policy](NEBULA_OAUTH_POLICY.md).

## Configure

Copy `.env.example` to `.env` and configure:

```ini
AGENT_NEBULA_EXAMPLES_ROOT=/opt/agent-nebula/examples
AGENT_HOSTNAME=localhost
NEBULA_URL=https://registry.agentnebula.ai
OAUTH_URL=https://oauth.agentnebula.ai
NGROK_DOMAIN=hydroxide-talon-glucose.ngrok-free.dev
NEBULA_PROXY_CA_FILE=/opt/agent-nebula/examples/nebula-certs/trust-bundle.pem
NEBULA_PROXY_TLS_NAME=localhost
```

`NGROK_DOMAIN` is the hostname assigned to **your** ngrok account. `NEBULA_PROXY_TLS_NAME` must match a SAN on the local server certificate; if the certificate does not cover `localhost`, set this to the name it covers. The CA bundle must validate the local server certificate. The generated proxy binds only to `127.0.0.1:8080`.

For Agent Nebula enrollment, ensure the server CSR contains the names required by the deployed server and trust model. Do not assume ngrok's edge TLS certificate is your origin server certificate.

Generate configuration:

```bash
make nebula-proxy-config
nginx -t -c /opt/agent-nebula/examples/proxy/nginx.conf
nginx -c /opt/agent-nebula/examples/proxy/nginx.conf
ngrok http 8080 --url https://hydroxide-talon-glucose.ngrok-free.dev
```

Start the relevant example server(s) in other terminals, for example:

```bash
make init example-06
make run example-06 server
```

`make init` renders the **public** Agent Card and `supported_interfaces` URLs when `NGROK_DOMAIN` is configured, without changing the local HTTPS listener. The public route for Example 06 is `/example-06/`. Example 09 has two server routes generated from its two A2A server configurations.

## Verify

```bash
curl -fsS https://hydroxide-talon-glucose.ngrok-free.dev/example-06/.well-known/agent-card.json
```

Check that the returned Agent Card advertises the public `/example-06/` URL. Register this **public Agent Card URL** with the hosted Registry, then verify discovery and OAuth-scoped invocation in Explorer. Repeat for each desired integration example.

## Limitations and security

- ngrok's HTTP tunnel terminates public TLS at its edge. It does **not** forward the original TLS client certificate to the origin. Do not use it to claim end-to-end client-certificate mTLS validation.
- Nginx uses certificate-verified HTTPS to local servers; no `proxy_ssl_verify off` fallback is provided.
- Do not expose local standalone examples, private keys, onboarding API keys, or admin endpoints through additional Nginx routes.
- Public Agent Card retrieval and actual remote invocation must both succeed; successful registration alone is not proof of reachability.
- Nginx/ngrok process management is intentionally explicit: this generator does not install system packages, configure ngrok credentials, or create privileged system services.
