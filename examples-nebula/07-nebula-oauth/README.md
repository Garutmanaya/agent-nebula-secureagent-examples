# 07 — OAuth-Protected A2A Agent

## Agent Nebula OAuth

Agent Nebula separates **Registry authentication** from **A2A endpoint authorization**. The onboarding API key authenticates registration/discovery calls to the Registry. The A2A Agent Card independently advertises OAuth 2.0 for invocation. Platform discovers the authorization-server metadata, performs standard client registration when needed, acquires a client-credentials token, and presents it to the protected A2A resource.

In a deployed Agent Nebula environment the OAuth service can consult the policy layer for authorization decisions. Policy remains external to business skill code; this example verifies the client/provider OAuth path, not a custom policy implementation.

The client must discover the provider through Registry and successfully invoke all three OAuth-protected skills. See `../../docs/agent-nebula-integration.md`.

## Hosted-platform prerequisites

Complete [Agent Nebula registration and discovery](../../docs/NEBULA_REGISTRATION.md) before this test. Review the [OAuth scopes and policy test matrix](../../docs/NEBULA_OAUTH_POLICY.md). Configure the public endpoint using the [Nginx + ngrok setup guide](../../docs/NEBULA_NGROK_NGINX.md).
