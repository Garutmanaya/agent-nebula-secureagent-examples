# Example 33 — A2UI + HTTPS + OAuth

## Purpose

Verifies that existing Agent Nebula HTTPS/OAuth security protects a normal native A2A request carrying an A2UI v1.0 DataPart. A2UI does not introduce a separate authentication or authorization layer.

## Flow

```text
AgentCard discovery -> HTTPS/OAuth client -> native A2A request
                                         -> AgentExecutor
                                         -> A2UI DataPart
                                         -> Rich BarChart
```

The A2UI extension URI and catalog IDs are discovered from the AgentCard. Security remains in the existing Agent Nebula A2A security path and executes before application business logic.

## Run

This example uses the `oauth-nebula` initialization profile and Agent Nebula certificate material.

```bash
make init example-33
make run example-33 server
make run example-33 client
make run example-33 browser
```

Open `http://localhost:9133` for browser validation.
