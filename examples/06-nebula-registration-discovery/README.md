# 06 — Agent Nebula Registration & Discovery

## Agent Nebula

[agentnebula.ai](https://agentnebula.ai/) is the enterprise integration layer used by these examples. The **Registry** stores and discovers registered agent identities, Agent Cards, protocols, and capabilities. It complements A2A rather than replacing it: A2A defines interoperable agent communication, while Agent Nebula adds curated enterprise registration/discovery and lifecycle integration.

This example is the first Registry acceptance test. The server registers through `nebula.conf`; the client searches the Registry by capability and invokes the returned provider instead of using a hard-coded provider URL.

Prerequisites: a running Agent Nebula Registry, its CA/trust bundle, an onboarding API key, and network reachability from Registry to the advertised Agent Card. See `../../docs/agent-nebula-integration.md`.
