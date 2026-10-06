# Example 28 — A2UI Tables

## Purpose

Demonstrates a structured table using the Agent Nebula Rich Catalog `DataTable` component. Application data is bound into application-owned `presentation.json`; Python does not construct a parallel UI component model.

## Flow

```text
AgentCard A2UI capability -> native A2A request -> InventoryExecutor
                                                |
                                                v
                                  presentation.json + row data
                                                |
                                                v
                                   A2UI DataPart -> DataTable
```

Catalog identifiers used by the client are discovered from the AgentCard.

## Run

```bash
make init example-28
make run example-28 server
make run example-28 client
make run example-28 browser
```

Open `http://localhost:9128` for browser validation.
