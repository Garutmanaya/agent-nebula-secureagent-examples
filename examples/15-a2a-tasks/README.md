# Example 15 — Native A2A Tasks

This example validates the isolated `server_a2a_sdk` execution path without changing the existing A2A server implementation.

It proves that Agent Nebula can advertise and deterministically dispatch multiple Agent Card skills while the selected application code uses the official `a2a-sdk` execution contract directly.

The `hello` skill publishes one native A2A `Message`. The `generate-reports` skill creates a native A2A `Task`, transitions it to working, publishes daily, weekly, and monthly artifacts with `TaskUpdater`, and completes the Task. The client uses the native SDK `send_message()`, `get_task()` and `list_tasks()` operations.

The Agent Nebula skill-selection extension is used only to select which advertised skill receives the request. It does not select or transform the resulting Message or Task.

## Lifecycle

Use the same repository lifecycle as every other example:

```text
make init example-15
make run example-15 server
make run example-15 client
make clean example-15
```

No Example 15-specific Makefile or lifecycle script is required.
