# Example 28 — A2UI Tables

Application-owned complete A2UI v1.0 JSON is transported in native A2A `DataPart` payloads and rendered by the shared `@a2ui/web_core` browser. The Agent Nebula Rich Catalog provides the `DataTable` component used by this example. The table definition stays entirely in `presentation.json`; runtime rows are supplied through the A2UI data model.

```bash
make init example-28
make run example-28 server
make run example-28 client
make run example-28 browser
```

Browser: `http://localhost:9128`.
