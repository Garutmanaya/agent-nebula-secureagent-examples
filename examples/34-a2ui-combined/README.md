# Example 34 — A2UI Combined

## Purpose

Combines the final frozen architecture in one secured agent: HTTPS + OAuth, AgentCard-driven multi-skill dispatch, native Task execution, native streaming, and application-owned A2UI presentations. No new protocol or result abstraction is introduced.

## Flow

```text
                 HTTPS + OAuth
                       |
                   AgentCard
                       |
              multi-skill dispatch
                 /           \
        service-report    stream-traffic
             |                 |
        native Task       native streaming
             |                 |
       A2UI artifact      A2UI incremental updates
```

The AgentCard is authoritative for skills, A2UI catalogs, and extension URIs. The application controls native A2A results and presentation JSON; SecureAgent/Platform provide configuration, security, discovery, and protocol composition.

## Run

This example uses the `oauth-nebula` initialization profile and Agent Nebula certificate material.

```bash
make init example-34
make run example-34 server
make run example-34 client
make run example-34 browser
```

Open `http://localhost:9134` and validate both the Task/report path and the incremental streaming path.
