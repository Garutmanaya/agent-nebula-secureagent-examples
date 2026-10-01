# Example 13: Mutual TLS

## Purpose

Mutual TLS extends ordinary HTTPS so both peers authenticate with X.509 certificates. The server proves its identity to the client and the client also presents a certificate trusted by the server.

This example uses the official A2A v1.0 Agent Card security model. Agent Nebula does not replace the A2A security declaration: Platform reads the standard `securitySchemes` and `securityRequirements`, while private verifier material stays outside the Agent Card.

## How the mechanism works

The Agent Card advertises the A2A mutual-TLS security scheme. The client TLS configuration supplies `client.crt` and `client.key`. The server listener is configured with `require_client_certificate=true` and a trust bundle, causing the TLS handshake to reject clients without a trusted certificate before HTTP/A2A processing. Platform then records the satisfied mTLS security requirement in the A2A call context.

Examples 04/05 validate encrypted TLS transport and server certificate verification. Example 13 additionally requires and validates the client certificate. Uvicorn performs certificate-chain validation at the TLS boundary; it does not expose the peer certificate in ASGI scope, so the Platform mTLS adapter treats successful entry past a `CERT_REQUIRED` listener as the authenticated transport fact.

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
make init example-13
make run example-13 server
make run example-13 client
```

The server and client source do not construct Platform or SDK security objects directly; security is configuration-driven through SecureAgent.
