# Example 26 — A2UI Actions over Native A2A

This example validates a real browser interaction end to end. The application creates the A2UI surface directly, the shared browser uses `@a2ui/web_core`, and a button click produces a standard A2UI v1.0 renderer-to-agent `action` message. That action is carried in a native `a2a-sdk` `DataPart` and handled by the same native `AgentExecutor` that created the surface.

```text
presentation.json -> CounterPresenter -> native A2A -> common/a2ui-web
                                                        |
                                                 user clicks Increment
                                                        |
                                      A2UI action + renderer data model
                                                        |
                                      native A2A -> CounterExecutor
                                                        |
                                           A2UI updateDataModel
                                                        |
                                      same MessageProcessor updates UI
```

SecureAgent provides configuration and Agent Nebula skill selection only. It does not create, parse, map, or handle A2UI on behalf of the application.

## Run

```bash
make init example-26
make run example-26 server
make run example-26 client
make run example-26 browser
```

Open `http://localhost:9126` and click **Increment**. The displayed counter must change from `0` to `1`, then continue incrementing on subsequent clicks without recreating the surface.

The browser test is the primary acceptance test: it verifies the actual renderer action, native A2A return path, synchronized data model, incremental provider update, and persistent renderer state.
