# Example 20 — Native A2A Extended Agent Card

The public Agent Card advertises `extended_agent_card=true` and an API-key security scheme. An authenticated native A2A client then calls `get_extended_agent_card()` and receives a distinct richer Agent Card. The extended card remains an official `a2a-sdk` `AgentCard`; no SecureAgent extended-card API is introduced.

```text
make init example-20
make run example-20 server
make run example-20 client
make clean example-20
```
