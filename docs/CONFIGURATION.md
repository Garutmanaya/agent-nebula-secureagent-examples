# Configuration model

The examples preserve the SecureAgent/Platform configuration boundary. `secureagent.conf` is generic. Protocol configuration belongs to the protocol. `nebula.conf` is optional and independent.

A2A Agent Card data is part of `a2aserver.conf`; no `agent-card.json` is used. This keeps one authoritative A2A server configuration and avoids synchronization between two representations.

Planned REST/MCP files contain only comments until Platform defines their loader schemas. The examples repository must not invent a configuration contract ahead of Platform.
