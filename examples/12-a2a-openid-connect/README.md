# Example 12: OpenID Connect

## Purpose

OpenID Connect (OIDC) builds identity on OAuth 2.0 and signed tokens. A2A advertises the OIDC discovery URL but does not perform the user/client login or issue tokens.

This example uses the official A2A v1.0 Agent Card security model. Agent Nebula does not replace the A2A security declaration: Platform reads the standard `securitySchemes` and `securityRequirements`, while private verifier material stays outside the Agent Card.

## How the mechanism works

The Agent Card advertises `openIdConnectSecurity`. For this deterministic local example, the client creates a short-lived RS256 JWT using the development client identity. The server validates its signature, `kid`, algorithm, issuer, audience, timestamps and subject using the configured trusted certificate. The token is sent as `Authorization: Bearer <JWT>`.

The local token generation is test provisioning, not an A2A operation and not a production identity provider. In production the credential is obtained from the advertised/trusted OpenID Provider outside A2A and then supplied to the A2A client.

## Agent Nebula implementation path

```text
AgentCard securitySchemes/securityRequirements
        |
        v
A2AServerSecurityFactory
        |
        v
scheme-specific Platform adapter
        |
        v
agent-nebula-sdk security primitive / TLS stack
        |
        v
A2ASecurityServerCallContextBuilder
        |
        v
official a2a-sdk request handler
```

The client resolves the authoritative Agent Card first. `A2AClientSecurityResolver` chooses a satisfiable security requirement and `A2AClientSecurityInterceptor` applies credentials through the official a2a-sdk client interceptor boundary.

## Run

```bash
make pki-init
make secrets-init
make init example-12
make run example-12 server
make run example-12 client
```

The server and client source do not construct Platform or SDK security objects directly; security is configuration-driven through SecureAgent.
