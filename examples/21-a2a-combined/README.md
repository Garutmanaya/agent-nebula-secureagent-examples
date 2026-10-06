# Example 21 — Combined Native A2A Capabilities

## Purpose

Combines the native A2A capabilities introduced in Examples 15–20 in one server: Task lifecycle, artifacts, streaming, push notifications, and Extended Agent Card retrieval. The application continues to use official `a2a-sdk` types; SecureAgent supplies composition and configuration.

## Flow

```text
client -> AgentCard -> native A2A operation -> AgentExecutor
                                      |
                                      +-> Task / artifacts / streaming
                                      +-> push configuration
                                      +-> Extended Agent Card
```

## Run

```bash
make init example-21
make run example-21 server
make run example-21 client
```

The client validates each combined capability and exits non-zero on failure.
