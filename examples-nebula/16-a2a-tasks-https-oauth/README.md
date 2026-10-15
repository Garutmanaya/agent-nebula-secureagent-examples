# Example 16 — Native A2A Tasks + HTTPS + OAuth

This example combines the proven Example 15 native `a2a-sdk` execution path with the proven Example 07 Agent Nebula registration, Registry discovery, HTTPS, and OAuth profile lifecycle.

The server registers its HTTPS Agent Card with Agent Nebula using the onboarding API key. The client discovers that registered provider, resolves its Agent Card, and uses the configured OAuth client profile and trust bundle before invoking it.

The application execution remains native `a2a-sdk`: `hello` publishes a native `Message`, while `generate-reports` owns a native `Task` lifecycle and publishes daily, weekly, and monthly artifacts. Platform security executes before the selected application executor.

## Lifecycle

Use the standard repository lifecycle:

```text
make init example-16
make run example-16 server
make run example-16 client
make clean example-16
```

`example-16` uses `init_mode = oauth-nebula` and `certificate_profile = nebula`, exactly like the existing Agent Nebula OAuth examples. Initialization therefore expects approved Agent Nebula certificates, the onboarding API key, and the shared OAuth authentication/DPoP keys. Dynamic Client Registration persists the OAuth client ID under the Example 16 runtime `data/client-id` path.

## Hosted-platform prerequisites

Complete [Agent Nebula registration and discovery](../../docs/NEBULA_REGISTRATION.md) before this test. Review the [OAuth scopes and policy test matrix](../../docs/NEBULA_OAUTH_POLICY.md). Configure the public endpoint using the [Nginx + ngrok setup guide](../../docs/NEBULA_NGROK_NGINX.md).
