# 05 — A2A Multi-Binding + TLS

Closes the transport layer before Agent Nebula integration. The same `hello`, `echo`, and `add` skills are registered once and invoked over JSON-RPC/HTTPS, HTTP+JSON/HTTPS, and gRPC/TLS. `make init example-05` creates a local CA and server identity under `.runtime`; verification is never disabled.

Acceptance criterion: all 9 binding/skill combinations pass.
