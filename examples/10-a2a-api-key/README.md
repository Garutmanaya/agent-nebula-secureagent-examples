# Example 10: API Key Security

## Purpose

An API key is an opaque credential provisioned to a client. It identifies/authenticates the caller to the A2A server; it does not authenticate the server to the client. HTTPS certificate validation provides server authentication.

This example uses the official A2A v1.0 Agent Card security model. Agent Nebula does not replace the A2A security declaration: Platform reads the standard `securitySchemes` and `securityRequirements`, while private verifier material stays outside the Agent Card.

## How the mechanism works

The Agent Card advertises an `apiKeySecurity` scheme with `location=header` and `name=X-API-Key`. The key value is never published. The client reads its provisioned key from a private secret file and sends `X-API-Key`. The server extracts that header and compares it with its independently provisioned verifier value. Missing or invalid keys fail before A2A skill dispatch.

This example deliberately uses a header key. The current a2a-sdk interceptor boundary safely supports request headers; query/cookie credential mutation is not used here.

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
make init example-10
make run example-10 server
make run example-10 client
```

The server and client source do not construct Platform or SDK security objects directly; security is configuration-driven through SecureAgent.
