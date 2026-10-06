# Example 23 — A2UI Mixed Basic + Rich Catalog

This example extends the Example 23 architecture without adding another A2UI API. The application owns one declarative `presentation.json` containing both standard Basic Catalog components and Agent Nebula Rich Catalog components. Rich components identify their catalog with `catalogId`; Python does not interpret either catalog.

The execution path remains native:

```text
presentation.json
        |
WeatherDashboardPresenter     application data binding only
        |
A2UI v1.0 createSurface JSON
        |
native a2a-sdk DataPart / Message
        |
examples/common/a2ui-web
        |
web_core + Basic Catalog + Rich Catalog
        |
real browser surface
```

SecureAgent supplies configuration and the Agent Nebula skill-selection extension. Standard A2A execution comes from `a2a-sdk`, and the application creates A2UI protocol JSON directly.

## Run

```bash
make init example-23
make run example-23 server
```

In another terminal:

```bash
make run example-23 client
make run example-23 browser
```

Open `http://localhost:9124` for the final validation. The surface must visibly combine Basic `Text`/layout components with Rich `StatusBadge` and `MetricGroup` components. A browser rendering failure means the example has not passed, even if the CLI protocol checks succeed.

The shared browser is intentionally reused unchanged from Example 23. Example 23 validates that catalog composition is data/presentation driven rather than implemented by an example-specific renderer.
