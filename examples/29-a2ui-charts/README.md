# Example 29 — A2UI Charts

## Purpose

Demonstrates a data-driven Agent Nebula Rich Catalog `BarChart`. The application owns the chart presentation JSON and supplies only business data at execution time.

## Flow

```text
AgentCard A2UI capability -> native A2A request -> ChartExecutor
                                                |
                                                v
                                presentation.json + series data
                                                |
                                                v
                                    A2UI DataPart -> BarChart
```

Catalog identifiers used by the client are discovered from the AgentCard.

## Run

```bash
make init example-29
make run example-29 server
make run example-29 client
make run example-29 browser
```

Open `http://localhost:9129` for browser validation.
