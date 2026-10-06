# Example 31 — A2UI + Native A2A Tasks

## Purpose

Verifies that application-owned A2UI can be carried by a native `a2a-sdk` Task artifact. `TaskUpdater` owns the native Task lifecycle; the application artifact carries the A2UI DataPart. No SecureAgent Task/result abstraction is introduced.

## Flow

```text
SendMessage -> AgentExecutor -> TaskUpdater(WORKING)
                            -> native Artifact[A2UI DataPart]
                            -> TaskUpdater(COMPLETED)
                            -> browser renders Task metadata + report
```

The browser exposes the actual Task ID, state, and artifact name so the example visibly proves native Task semantics in addition to rendering the report. Catalog IDs are discovered from the AgentCard.

## Run

```bash
make init example-31
make run example-31 server
make run example-31 client
make run example-31 browser
```

Open `http://localhost:9131` for browser validation.
