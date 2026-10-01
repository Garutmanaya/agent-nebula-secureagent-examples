# Example 14: Multiple Security Schemes

## Purpose

A2A follows OpenAPI-style security requirement semantics: separate requirement entries are alternatives (OR), while multiple schemes inside one requirement must all succeed (AND).

This example uses the official A2A v1.0 Agent Card security model. Agent Nebula does not replace the A2A security declaration: Platform reads the standard `securitySchemes` and `securityRequirements`, while private verifier material stays outside the Agent Card.

## How the mechanism works

This example advertises API Key and HTTP Bearer and requires both in one requirement entry: `api_key AND http_bearer`. The client security resolver must find credentials for both and the interceptor applies both headers. The server independently validates both before dispatch. To express alternatives, use two `[[agent_card.security_requirements]]` entries instead; that is `api_key OR http_bearer`.

Using an AND case makes the composition visible in one successful request. The README documents the equivalent OR form; both semantics are covered by Platform security-service tests.

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
make init example-14
make run example-14 server
make run example-14 client
```

The server and client source do not construct Platform or SDK security objects directly; security is configuration-driven through SecureAgent.
