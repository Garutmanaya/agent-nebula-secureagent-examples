# Example 27 — A2UI Forms over Native A2A

This example validates browser-edited A2UI form state end to end. The application owns the form in `presentation.json`; `@a2ui/web_core` owns binding browser controls to the A2UI data model; native `a2a-sdk` carries the renderer action and synchronized data model back to the application.

```text
presentation.json
       |
       v
ContactFormPresenter -> native A2A -> common/a2ui-web
                                         |
                                  user edits fields
                                         |
                                  web_core bindings
                                         |
                                   Submit action
                                         |
                            A2UI action + data model
                                         |
                            native A2A -> application
                                         |
                              application validation
                                         |
                              A2UI updateDataModel
                                         |
                             same surface is updated
```

SecureAgent provides configuration and Agent Nebula skill selection only. It does not define a form API, copy browser field values into an application model, or translate the A2UI action.

The `TextField`, `Button`, data bindings, action name, and action context are declared in `presentation.json`. The Python presenter does not interpret component types.

## Run

```bash
make init example-27
make run example-27 server
make run example-27 client
make run example-27 browser
```

Open `http://localhost:9127`.

Enter a name and email address, then select **Submit**. The result text must update without recreating the surface. Try an empty name or an email without `@` to verify that application validation returns through the same A2UI `updateDataModel` path.

The browser interaction is the primary acceptance test. It proves two-way Basic Catalog `TextField` binding, renderer-to-agent action submission, synchronized renderer state, native A2A transport, application validation, and incremental A2UI update processing.
