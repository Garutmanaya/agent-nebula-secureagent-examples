# 12 - A2UI v1.0 Actions over A2A

This example verifies the renderer-to-agent direction added in Step 1G. The initial `forecast` invocation returns an interactive A2UI surface. The client then simulates the renderer clicking `recalculate` and sends the A2UI v1.0 `action` over the standard A2A DataPart binding.

The provider receives the action and the renderer data model, recalculates the result, and returns a correlated v1.0 `actionResponse` plus an `updateDataModel` message.

```text
client -> forecast -> provider -> A2UI surface
client -> A2UI action -> A2A -> provider
provider -> actionResponse + updateDataModel -> client
```

Run:

```bash
make init
make run server
```

In another terminal:

```bash
make run client
```

Expected result:

```text
PASS  provider returned the interactive A2UI v1.0 surface
PASS  renderer action reached the provider over A2A
PASS  renderer data model reached the surface owner
PASS  provider returned correlated actionResponse + updated A2UI
RESULT: bidirectional A2UI v1.0 action verification passed
```
