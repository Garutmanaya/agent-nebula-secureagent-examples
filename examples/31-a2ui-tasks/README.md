# Example 31 — A2UI + Native A2A Tasks

This example proves that A2UI presentation output can be carried by a native
`a2a-sdk` Task artifact without introducing a SecureAgent task or A2UI result
abstraction.

The application owns the native `AgentExecutor`, `TaskUpdater`, Task lifecycle,
business data, and `presentation.json`. SecureAgent provides configuration and
A2A/A2UI composition. The A2UI JSON is transported in a native A2A `DataPart`
inside the Task artifact.

```text
A2A request
    -> native AgentExecutor
    -> native Task / WORKING
    -> native Artifact
         -> A2UI DataPart
              -> createSurface / Rich DataTable
    -> native Task / COMPLETED
    -> browser renderer
```

Run:

```bash
make init example-31
make run example-31 server
make run example-31 client
make run example-31 browser
```

Open `http://localhost:9131` for browser validation.
