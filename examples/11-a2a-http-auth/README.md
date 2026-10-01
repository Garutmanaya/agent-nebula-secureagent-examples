# Example 11: HTTP Authentication

## Purpose

HTTP authentication uses the standard `Authorization` header. This example uses the Bearer authentication scheme with an opaque provisioned credential.

This example uses the official A2A v1.0 Agent Card security model. Agent Nebula does not replace the A2A security declaration: Platform reads the standard `securitySchemes` and `securityRequirements`, while private verifier material stays outside the Agent Card.

## How the mechanism works

The Agent Card advertises `httpAuthSecurity` with `scheme=Bearer`. The client therefore sends `Authorization: Bearer <credential>`. Platform verifies both the advertised scheme and the credential. A wrong prefix, missing value, or invalid value is rejected before the A2A request reaches the agent skill.

Bearer describes the HTTP authorization syntax; it does not by itself define OAuth. Example 07 demonstrates OAuth token acquisition. Here the Bearer value is a statically provisioned opaque credential.

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
make init example-11
make run example-11 server
make run example-11 client
```

The server and client source do not construct Platform or SDK security objects directly; security is configuration-driven through SecureAgent.
