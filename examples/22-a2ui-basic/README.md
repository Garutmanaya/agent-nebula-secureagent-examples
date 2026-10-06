# Example 22 — A2UI Basic

This example demonstrates an application-owned A2UI v1.0 Basic Catalog presentation over the native `a2a-sdk` execution path. SecureAgent supplies configuration and the Agent Nebula multi-skill extension only. The application constructs A2UI protocol JSON directly and transports it in a native A2A `DataPart`.

The browser is shared infrastructure under `examples/common/a2ui-web`. It uses the same packaged `@a2ui/web_core` and Rich catalog artifacts as Agent Nebula Solutions so later A2UI examples do not create independent renderers. `presentation.json` remains the application presentation manifest.

## Run

```bash
make a2ui-init
make a2ui-web-build
make init example-22
make run example-22 server
```

In another terminal:

```bash
make run example-22 client
make run example-22 browser
```

Open `http://localhost:9123`. The visible Regional Forecast surface is the browser-level acceptance test.

By default `make a2ui-init` reads packages from the sibling `../agent-nebula-a2ui` repository. Set `AGENT_NEBULA_A2UI_SOURCE` when the package repository is elsewhere.
