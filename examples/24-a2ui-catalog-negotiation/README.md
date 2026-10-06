# Example 24 — A2UI Catalog Negotiation

This example demonstrates the A2UI v1.0 capability handshake over native A2A. The Agent Card advertises the catalogs the agent can generate. The client sends `a2uiRendererCapabilities` in A2A message metadata, ordered by preference. The application selects a mutually supported catalog and identifies that catalog in `createSurface.catalogId`.

No SecureAgent A2UI result abstraction is introduced; the application owns A2UI protocol JSON and native `a2a-sdk` transports it.
