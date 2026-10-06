# Example 32 — A2UI + Native A2A Streaming

## Purpose

Verifies native `a2a-sdk` Task streaming with incremental A2UI artifact updates. Each A2A artifact event is forwarded by the browser bridge as it arrives, allowing the persistent A2UI `MessageProcessor` to update the existing chart surface visibly.

## Flow

```text
Task WORKING
  -> artifact createSurface
  -> artifact updateDataModel #1
  -> artifact updateDataModel #2
  -> artifact updateDataModel #3
Task COMPLETED
```

The stream is native A2A streaming; the browser transport only forwards received A2UI protocol messages incrementally. Catalog IDs are discovered from the AgentCard.

## Run

```bash
make init example-32
make run example-32 server
make run example-32 client
make run example-32 browser
```

Open `http://localhost:9132` and verify that the chart updates incrementally rather than appearing only in its final state.
