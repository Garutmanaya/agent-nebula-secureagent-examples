# 02. A2A multi-skill

## Purpose

Verify deterministic multi-skill dispatch through the SecureAgent A2A client and server. The server registers `hello`, `echo`, and `add` once through `agent.a2a_skill()`. The client resolves the Agent Card, verifies that all three skills are advertised, then explicitly selects and invokes every skill.

This example is the baseline for subsequent examples: multi-skill behavior is treated as normal agent behavior rather than a special case.

## Test coverage

`make run example-02 client` fails with a non-zero exit if the Agent Card is incomplete, skill selection is incorrect, or any response differs from the expected result. It tests `JSON-RPC × {hello, echo, add}`.

## Run

```bash
make init example-02
make run example-02 server
```

In another terminal:

```bash
make run example-02 client
```

The server listens on `http://localhost:9002/`. No TLS or application authentication is used yet.

## Files

`main.py` contains the three business handlers. `client.py` is the executable verification client. `config/a2aserver.conf` publishes the Agent Card and JSON-RPC interface; `config/a2aclient.conf` selects JSON-RPC.

## Cleanup

```bash
make clean example-02
```
