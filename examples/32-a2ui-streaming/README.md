# Example 32 — A2UI + Native A2A Streaming

Demonstrates native `a2a-sdk` streaming with application-owned A2UI v1.0 protocol messages carried by Task artifact updates.

The application emits one `createSurface` message followed by three `updateDataModel` messages through native `TaskUpdater.add_artifact(...)` streaming events. SecureAgent does not implement a separate A2UI streaming abstraction.

```text
A2A request
    |
    v
native AgentExecutor / TaskUpdater
    |
    +-- WORKING
    +-- artifact update: createSurface
    +-- artifact update: updateDataModel
    +-- artifact update: updateDataModel
    +-- artifact update: updateDataModel
    +-- COMPLETED
             |
             v
        A2UI renderer
```

Run the server, client, and browser through the repository `make run example-32 ...` targets. Browser validation is available at `http://localhost:9132`.
