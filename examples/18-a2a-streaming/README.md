# Example 18 — Native A2A Streaming

Advertises `AgentCard.capabilities.streaming=true` and uses native `Client.send_message()` iteration to observe Task, status, and artifact update events. There is no SecureAgent streaming wrapper.

```text
make init example-18
make run example-18 server
make run example-18 client
make clean example-18
```
