# 03. A2A multi-binding

## Purpose

Verify that one SecureAgent business-skill set is exposed through all three A2A 1.0 protocol bindings supported by Platform: JSON-RPC, HTTP+JSON, and gRPC. Skills are registered once; the protocol adapters provide different wire bindings over the same A2A semantics and dispatcher.

## Test coverage

The client first validates the Agent Card advertises exactly the expected three bindings and three skills. It then creates a separate SecureAgent client instance for each binding. Each client configuration permits only that binding, preventing fallback from hiding a broken transport.

The complete matrix is nine invocations: `{JSON-RPC, HTTP+JSON, gRPC} × {hello, echo, add}`. Any failure exits non-zero.

## Run

```bash
make init example-03
make run example-03 server
```

In another terminal:

```bash
make run example-03 client
```

HTTP-hosted Agent Card discovery and A2A routes use port `9003`; the gRPC A2A listener uses `localhost:50053`. The Platform installation must include its A2A gRPC dependency/extra.

## Design point

There are no JSON-RPC-specific, HTTP+JSON-specific, or gRPC-specific skill handlers. `main.py` registers each business skill once. This example verifies that protocol binding remains a transport concern below the SecureAgent application API.

## Cleanup

```bash
make clean example-03
```
