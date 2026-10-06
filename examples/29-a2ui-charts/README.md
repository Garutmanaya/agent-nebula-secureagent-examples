# Example 29 — A2UI Charts

Application-owned complete A2UI v1.0 JSON is transported in native A2A `DataPart` payloads and rendered by the shared `@a2ui/web_core` browser with the registered `@agent-nebula/a2ui-rich` catalog. This example uses the Rich Catalog `BarChart` component exactly as defined by the catalog contract.

The client advertises the Agent Nebula Rich Catalog, the Agent Card advertises the same catalog from `a2ui.conf`, and the application sends a `createSurface` whose `catalogId` selects that catalog. Runtime chart values are supplied through the A2UI data model.

```bash
make init example-29
make run example-29 server
make run example-29 client
make run example-29 browser
```

Browser: `http://localhost:9129`.
