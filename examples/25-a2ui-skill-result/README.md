# Example 25 — A2UI Skill Result

This example proves that Agent Nebula multi-skill selection can dispatch to
independent native `a2a-sdk` `AgentExecutor` implementations and that each
application skill can produce its own A2UI v1.0 result directly.

## Boundary demonstrated

```text
A2A request
    |
    v
Agent Nebula skill-selection extension
    |
    +--> weather AgentExecutor ------> weather.json ------> A2UI surface
    |
    `--> system-health AgentExecutor -> system-health.json -> A2UI surface
                                               |
                                               v
                                      native a2a-sdk Message
```

SecureAgent provides configuration and the Agent Nebula multi-skill extension.
It does not create, convert, or interpret either A2UI result. There is no
`SkillResult.ui`, A2UI result mapper, or SecureAgent A2UI construction API.

Both presentations are application-owned JSON manifests. The shared
`examples/common/a2ui-web` renderer displays both surfaces without adding
Example-25-specific rendering code.

## Run

```bash
make init example-25
make run example-25 server
```

In another terminal:

```bash
make run example-25 client
make run example-25 browser
```

Open `http://localhost:9125` for the browser validation. The page must display
both **Weather Skill Result** and **System Health Skill Result** surfaces.

## Expected verification

The CLI verifies that the two skill IDs select different native executors,
each returns a native A2A Message containing `application/a2ui+json`, and each
surface contains its own presentation and data model. Browser validation then
proves that both provider-owned surfaces are accepted by the same shared A2UI
v1.0 renderer.
