# Example 24 — A2UI Catalog Negotiation

## Purpose

Verifies A2UI v1.0 capability negotiation without duplicating catalog identifiers in application Python. The AgentCard advertises the server catalogs, the client derives its renderer capability list from that advertisement, and the request activates the discovered A2UI extension through native A2A service parameters.

## Flow

```text
AgentCard -> A2UI extension + supportedCatalogIds
                         |
                         v
client renderer capabilities in SendMessageRequest.metadata
                         |
                         v
server selects a mutually supported catalog -> createSurface
```

The AgentCard is authoritative for the A2UI extension URI and advertised catalog IDs.

## Run

```bash
make init example-24
make run example-24 server
make run example-24 client
```
