# Agent Nebula A2A / A2UI Integration Requirements

## 1. Purpose

This document defines the architectural contract for Agent Nebula's integration with the official A2A SDK and A2UI. It applies to:

- `agent-nebula-sdk`
- `agent-nebula-platform`
- `agent-nebula-secureagent`
- `agent-nebula-secureagent-examples`
- `agent-nebula-solutions`
- `agent-nebula-explorer`
- `agent-nebula-playground`
- `agent-nebula-studio`

These requirements are the migration and code-review baseline. Existing code should be retained only when it implements a documented Agent Nebula responsibility or necessary composition around the official protocols.

## 2. Core Principle

> **Agent Nebula composes around the official protocols; it does not implement parallel versions of them.**

```text
Application / Solution
        │
        │ native A2A + A2UI programming model
        ▼
┌──────────────────────────────────────────┐
│              Agent Nebula                │
│                                          │
│  Configuration                           │
│  Security                                │
│  Registration / Discovery                │
│  Nebula extensions (for example,         │
│  explicit multi-skill selection)         │
│  Server / client composition             │
└────────────────────┬─────────────────────┘
                     │
                     ▼
              official a2a-sdk
                     │
                     ▼
                A2A transports
```

If `a2a-sdk` or A2UI already defines a concept, API, model, lifecycle, catalog, or protocol behavior, Agent Nebula must use that definition rather than create a competing equivalent.

## 3. Official `a2a-sdk` Is Authoritative

All standard A2A functionality must use the official `a2a-sdk`. This includes, but is not limited to:

- Agent Card models and standard capabilities
- `Message`
- `Task`
- `Artifact`
- task states and lifecycle
- `RequestContext`
- `EventQueue`
- `TaskUpdater`
- task storage
- cancellation
- continuation and multi-turn interaction
- streaming
- status updates
- artifacts
- push notifications
- native client operations
- native server request handling
- standard transports and bindings

Agent Nebula must not introduce competing abstractions such as `PlatformTask`, `TaskExecutionContext`, `TaskResult`, `TaskArtifactResult`, `NebulaTaskUpdater`, `NebulaMessage`, or `NebulaArtifact` when the SDK already supplies the required abstraction.

## 4. Native Application Execution Must Be Preserved

Application code owns application behavior. A selected skill must be able to use the normal `a2a-sdk` programming model directly.

```text
RequestContext + EventQueue
            │
            ▼
   Application AgentExecutor
            │
            ├── Message
            ├── Task
            ├── Task status updates
            ├── Artifact
            ├── streaming events
            └── other native A2A results
```

The application decides what a request produces. Platform must not decide that one skill returns a `Message`, another returns a `Task`, or another creates a streaming task.

Therefore:

- do not introduce Platform execution metadata such as `execution=TASK` or `SkillExecutionMode`;
- do not infer result type from skill metadata;
- do not convert application results into `Message` or `Task` based on Platform-defined rules;
- do not require `SkillResult`, `SkillInvocation`, `A2AResultMapper`, or equivalent Nebula abstractions for standard native execution.

Optional convenience APIs may exist only when they do not restrict or replace direct access to native `a2a-sdk` behavior.

## 5. Multi-Skill Selection Is a Nebula Extension, Not an Execution Model

Explicit multi-skill selection is an Agent Nebula extension. Its responsibility ends at dispatch.

```text
A2A request
     │
     ▼
Nebula skill-selection extension
     │
     ├── skill A ──► AgentExecutor A
     ├── skill B ──► AgentExecutor B
     └── skill C ──► AgentExecutor C
                         │
                         ▼
                 native A2A execution
```

Skill selection answers only:

> **Which application executor receives this request?**

It must not determine what result type the selected executor produces. The selected application executor must retain the native `RequestContext`, `EventQueue`, and other SDK facilities needed to implement standard A2A behavior directly.

## 6. `server_a2a_sdk` Is the A2A Server Execution Path

The execution path proven by Examples 15 and 16 is the baseline:

```text
Transport
   │
   ▼
a2a-sdk server route
   │
   ▼
ServerCallContextBuilder
   │
   ▼
Nebula security integration
   │
   ▼
DefaultRequestHandler
   │
   ▼
A2ASdkAgentExecutor
   │
   ▼
Nebula skill dispatch
   │
   ▼
Application AgentExecutor
   │
   ▼
native a2a-sdk results/events
```

Tasks, cancellation, context, artifacts, streaming, push notifications, A2UI, and future standard capabilities must continue through this execution path.

A2UI must not introduce a second server execution model. Examples 15 and 16 are proven native baselines and must not be modified merely to accommodate A2UI.

## 7. Security Is Infrastructure, Not Application Execution

SecureAgent/Platform may configure and enforce security mechanisms such as OAuth, DPoP, mTLS, JWT-based mechanisms, credentials, TLS, and security-context construction.

```text
Request
   │
   ▼
Transport
   │
   ▼
Authentication / security validation
   │
   ▼
A2A request handler
   │
   ▼
Application AgentExecutor
```

Requirements:

- authentication and security-context creation occur before application business execution;
- official `a2a-sdk` integration points must be used where available;
- enabling security must not require application code to adopt Nebula-specific Message, Task, result, or execution models;
- security must remain independent of the application's choice of native A2A result type.

## 8. Configuration-Driven Composition Is a SecureAgent Responsibility

SecureAgent exists to simplify composition around the official SDK. Legitimate responsibilities include:

- configuration loading and validation;
- security configuration;
- transport and binding configuration;
- server composition;
- client composition;
- Agent Card integration;
- registration and discovery integration;
- explicit Agent Nebula extensions;
- multi-skill registration and dispatch.

These responsibilities must not expand into reimplementation of the underlying A2A programming model.

## 9. Native Client APIs Must Remain Native

SecureAgent may construct and configure an authenticated A2A client:

```python
client = await agent.a2a_client(...)
```

After construction, standard operations should remain SDK-owned wherever possible.

```text
SecureAgent
    │
    │ configuration / security / discovery
    ▼
native A2A client
    │
    ├── send_message()
    ├── get_task()
    ├── list_tasks()
    ├── cancel_task()
    ├── subscribe()
    └── other SDK operations
```

Do not create Nebula wrappers that merely rename or proxy standard SDK client operations.

## 10. Standard A2A Application Code Must Remain Portable

Normal `a2a-sdk` application and example code should work with SecureAgent with only the changes required for Agent Nebula configuration, security, registration/discovery, skill selection, or explicit Nebula extensions.

Developers should not have to rewrite native `AgentExecutor`, `RequestContext`, `EventQueue`, `TaskUpdater`, `Message`, `Task`, or `Artifact` usage into Agent Nebula-specific equivalents.

This portability requirement is a migration acceptance test for every repository.

## 11. A2UI Uses the Same Native A2A Execution Model

A2UI remains an A2A extension and must travel through the same native A2A execution path.

```text
Application
    │
    │ native A2UI protocol structures
    ▼
A2A Message / DataPart
    │
    ▼
server_a2a_sdk
    │
    ▼
A2A transport
    │
    ▼
A2UI renderer
```

There must not be separate A2A and Nebula-A2UI execution models.

## 12. Native A2UI Protocol Structures Are Authoritative

Platform/SecureAgent must not create duplicate APIs or models for standard A2UI concepts. Do not add equivalents of:

- `create_a2ui_surface()`
- `update_a2ui_surface()`
- `set_a2ui_action_handler()`
- `send_a2ui_action()`
- `A2UIResult`
- `NebulaSurface`
- `NebulaComponent`
- `NebulaAction`

Likewise, `SkillResult.ui` or `A2AResultMapper` must not be required for native A2UI execution.

A2UI application results remain controlled by the application rather than inferred, selected, or converted by Platform.

## 13. A2UI Catalogs Remain A2UI Concepts

Agent Nebula must not duplicate:

- the Basic Catalog;
- Rich/custom catalogs;
- catalog components;
- catalog component schemas;
- catalog-specific component models.

The Basic Catalog is a provided A2UI catalog, not a special Agent Nebula protocol type. Rich and custom catalogs follow the same A2UI catalog model.

```text
A2UI protocol
    │
    ├── Basic Catalog
    ├── Rich Catalog
    └── other/custom catalogs
```

Catalog negotiation and extension metadata may be integrated with configuration and the Agent Card when required, but catalog definitions remain A2UI-owned concepts.

## 14. A2UI Presentation Belongs to the Application

The pattern validated by Examples 23-27 is the baseline:

```text
presentation.json
       │
       ▼
Application Presenter
       │
       ├── presentation definition
       └── runtime/business data
       │
       ▼
A2UI protocol JSON
       │
       ▼
native A2A DataPart
       │
       ▼
A2UI renderer
```

The application controls its presentation and result. Platform must not infer a UI from business results.

## 15. A2UI Actions and Forms Remain A2UI-over-A2A

The interaction model validated by Examples 26 and 27 must be preserved:

```text
Browser component
      │
      ▼
A2UI action / bound data
      │
      ▼
native A2A Message
      │
      ▼
Nebula skill dispatch
      │
      ▼
Application AgentExecutor
      │
      ▼
application handles action
      │
      ▼
A2UI updateDataModel / updateComponents
      │
      ▼
native A2A response
      │
      ▼
persistent A2UI MessageProcessor
      │
      ▼
Browser update
```

Do not add a parallel application action protocol or SecureAgent action API.

## 16. Agent Card Is Authoritative

The native Agent Card is authoritative for advertised:

- agent identity and description;
- skills;
- capabilities;
- interfaces and bindings;
- security requirements;
- standard A2A features;
- protocol extensions.

Agent Nebula Registry operates around the native Agent Card. It must not introduce a separate application execution description that competes with it.

Nebula-specific behavior must be represented as an explicit extension when protocol metadata is required.

## 17. Registration and Discovery Are Surrounding Services

Registration and discovery are valid Agent Nebula responsibilities.

```text
Agent Card
    │
    ▼
Nebula Registry
    │
    ▼
Discovery
    │
    ▼
selected Agent Card
    │
    ▼
native A2A client interaction
```

Registry data may index and search Agent Card information, but it must not become a parallel A2A application model. Discovery should identify suitable agents; subsequent A2A behavior remains governed by the selected Agent Card and native protocol APIs.

## 18. Convenience APIs Have a Strict Acceptance Rule

Convenience APIs are allowed only when they:

1. reduce repetitive configuration or composition code;
2. do not hide required native functionality;
3. do not change protocol semantics;
4. remain optional where native SDK use is appropriate;
5. do not force applications into Nebula-specific result or execution models.

```text
Does this simplify composition?
          │
         YES
          ▼
Does native a2a-sdk/A2UI functionality remain accessible?
          │
         YES
          ▼
Potentially valid convenience API
```

A wrapper that merely reproduces, renames, or proxies an SDK API should normally be removed.

## 19. Examples Are Executable Documentation

Examples define how developers are expected to use SecureAgent. They are not disposable test programs.

Example code must be:

- readable and consistently formatted;
- commented by responsibility rather than line-by-line narration;
- separated into files by functionality;
- configuration-driven with configuration, secrets, and runtime data externalized where appropriate;
- split into server/client/browser/application/presentation responsibilities where applicable;
- object-oriented only when classes represent real responsibilities;
- sufficiently realistic to demonstrate a maintainable application structure.

Avoid giant single-file examples. Also avoid artificial wrapper classes such as `MessageManager`, `TaskManager`, `A2UIManager`, or `ProtocolManager` created merely to claim object orientation.

Classes should represent actual responsibilities, for example `ReportExecutor`, `ForecastPresenter`, `InventoryRepository`, or `BookingService`, and should remain pluggable/extendable where that responsibility requires it.

## 20. Examples Must Validate the Architecture, Not Only the Feature

Before implementing a feature, verify that the implementation approach can support the remaining examples, especially the combined scenarios through Example 34.

Do not solve Example N with an approach that requires earlier examples or core APIs to be redesigned when a later example introduces Tasks, streaming, security, actions, or multiple skills.

```text
simple
  ↓
multi-skill
  ↓
Task
  ↓
security
  ↓
context
  ↓
artifacts
  ↓
streaming
  ↓
A2UI
  ↓
actions/forms
  ↓
combined capabilities
```

Capabilities should accumulate while the underlying execution architecture remains stable.

## 21. Runtime Validation Is Required

Compilation, static checks, and unit tests are necessary but are not sufficient for protocol examples.

For A2A examples, validate the intended server/client protocol flow at runtime.

For A2UI examples, real renderer/browser validation is part of protocol validation:

```text
JSON valid
   ≠
A2UI valid

web_core processing
   +
catalog validation
   +
browser rendering
   +
interaction where applicable
   =
useful A2UI validation
```

An example must not be marked complete until its intended runtime path has been exercised successfully.

## 22. Migration Rule for Solutions, Explorer, Playground, and Studio

Use the same decision tree for each repository. Do not migrate obsolete Nebula abstractions one-for-one.

```text
Existing code
    │
    ▼
Is this standard A2A functionality?
    │
   YES ─────────► use a2a-sdk
    │
    NO
    ▼
Is this standard A2UI functionality?
    │
   YES ─────────► use native A2UI
    │
    NO
    ▼
Is this configuration/security/
registration/discovery/composition?
    │
   YES ─────────► SecureAgent/Platform
    │
    NO
    ▼
Is this a genuine Nebula extension?
    │
   YES ─────────► explicit extension
    │
    NO
    ▼
Is this application/business/UI logic?
                  │
                 YES
                  ▼
              application
```

Migration must preserve behavior while moving each responsibility to its correct owner.

## 23. Repository Responsibilities After Migration

| Repository / dependency | Primary responsibility |
| --- | --- |
| `agent-nebula-sdk` | Security protocols and security primitives |
| `agent-nebula-platform` | Integration/composition infrastructure, security integration, official A2A SDK integration, and explicit Nebula protocol extensions |
| `agent-nebula-secureagent` | Simplified configuration-driven facade, server/client composition, registration/discovery integration, and multi-skill integration |
| official `a2a-sdk` | Standard A2A protocol models, APIs, lifecycle, client/server behavior, Tasks, Messages, artifacts, streaming, and related standard functionality |
| A2UI | Standard A2UI protocol structures, catalogs, components, actions, data-model semantics, and renderer protocol behavior |
| Solutions / Explorer / Playground / Studio | Application behavior, native `AgentExecutor` implementations, presenters, business logic, native A2A/A2UI usage, and application UI |

Ownership should remain explicit. A capability must not be moved into Platform or SecureAgent merely because multiple applications use it; first determine whether it is already a standard A2A/A2UI capability or reusable application/library functionality.

## 24. Backward Compatibility Must Not Preserve the Wrong Architecture

Migration should minimize unnecessary breakage, but backward compatibility is not a reason to retain a parallel protocol model indefinitely.

When an existing Nebula API duplicates official `a2a-sdk` or A2UI behavior:

1. migrate dependent repositories to the native API;
2. verify the migrated runtime behavior;
3. identify remaining consumers;
4. remove or deprecate the redundant API only after consumers have migrated.

Do not introduce new dependencies on legacy abstractions during the migration period.

## 25. Cleanup Is Deferred Until Repository Migration Is Complete

Do **not** aggressively remove legacy SecureAgent/Platform APIs while Solutions, Explorer, Playground, or Studio still depend on them. The migration must first establish that all consumers operate correctly through the native model.

After all dependent repositories have migrated and passed runtime validation, perform a dedicated cleanup of `agent-nebula-secureagent` and `agent-nebula-platform`.

### 25.1 `agent-nebula-secureagent` cleanup

Review and remove or simplify APIs that duplicate native protocol behavior, including where present:

- legacy skill execution/result abstractions used instead of native `AgentExecutor` execution;
- `SkillResult`/`SkillInvocation` requirements for standard A2A execution;
- A2UI surface creation/update helpers;
- A2UI action-handler registration or action-sending helpers;
- A2UI result wrappers or `SkillResult.ui` coupling;
- wrappers around native Task operations such as get/list/cancel/subscribe;
- wrappers around standard Message, Task, Artifact, streaming, or status APIs;
- obsolete compatibility paths that bypass `server_a2a_sdk`;
- duplicate client/server composition code left from pre-`a2a-sdk` implementations;
- configuration fields that existed only to support removed execution abstractions;
- dead imports, exports, tests, examples, and documentation for removed APIs.

Retain SecureAgent functionality that still provides genuine value: configuration-driven composition, security setup, registration/discovery integration, Agent Card integration, and explicit Nebula extensions such as multi-skill selection.

### 25.2 `agent-nebula-platform` cleanup

Review and remove or simplify Platform code that duplicates official A2A/A2UI functionality, including where present:

- legacy A2A server/executor paths superseded by `server_a2a_sdk`;
- result mappers that convert application results into Platform-selected Message/Task forms;
- Platform-owned Task, Message, Artifact, status, or execution models;
- Task lifecycle helpers already supplied by `a2a-sdk`;
- duplicate Task storage/request handling when the SDK implementation satisfies the requirement;
- duplicate native client operation adapters;
- A2UI surface/component/action/result models;
- A2UI execution or action-dispatch paths separate from native A2A execution;
- duplicated Basic/Rich catalog models or catalog-specific protocol types;
- compatibility adapters whose only purpose was to support removed SecureAgent APIs;
- obsolete protocol configuration and composition branches;
- dead tests, fixtures, exports, documentation, and dependencies.

Retain Platform functionality required for security integration, official SDK composition, configuration, telemetry/observability, and explicitly documented Nebula extensions.

### 25.3 Cleanup acceptance criteria

Cleanup is complete only when:

- Solutions, Explorer, Playground, Studio, and maintained examples no longer import removed legacy APIs;
- standard A2A application code still uses native SDK types and lifecycle semantics;
- A2UI applications still use native A2UI structures through the same A2A execution path;
- `server_a2a_sdk` is the maintained A2A server path;
- security still executes before application business logic;
- multi-skill dispatch still forwards native execution context without controlling results;
- registry/discovery still operates around the native Agent Card;
- unit, integration, protocol runtime, and browser/A2UI validation pass;
- obsolete code, configuration, documentation, dependencies, and compatibility tests are removed together rather than left as dead surface area.

The cleanup should be performed as a separate, reviewable phase after migration, not mixed into application migration patches unless a removal is required to make the native path work.

## 26. Migration Acceptance Checklist

For each migrated repository or example, verify:

- [ ] Standard A2A functionality uses official `a2a-sdk` APIs and models.
- [ ] Standard A2UI functionality uses native A2UI protocol structures/catalogs.
- [ ] No new duplicate Message, Task, Artifact, surface, component, action, or result abstraction was introduced.
- [ ] Application `AgentExecutor` controls its native A2A results.
- [ ] Multi-skill selection only selects/dispatches the application skill.
- [ ] Security occurs before application execution and does not change application result semantics.
- [ ] Agent Card remains authoritative for advertised capabilities, skills, interfaces, security, and extensions.
- [ ] Native A2A client operations remain available.
- [ ] A2UI uses the same `server_a2a_sdk` execution path.
- [ ] Application/business/presentation logic remains outside Platform/SecureAgent.
- [ ] Code is organized by real responsibility and does not introduce artificial wrappers.
- [ ] Runtime validation appropriate to the capability has passed.
- [ ] The implementation approach remains compatible with later combined-capability scenarios.

## 27. Frozen Migration Objective

> **Agent Nebula should make standard A2A/A2UI applications easier to configure, secure, register, discover, and compose without changing how standard A2A/A2UI applications are programmed.**

Use this code-review test:

```text
If we remove Nebula-specific configuration,
security, discovery, and extensions...

Does the remaining application still look
like normal a2a-sdk / A2UI code?

                YES
                 │
                 ▼
        boundary is probably correct
```

This contract governs the Examples 01-14 revalidation and the subsequent migration of Solutions, Explorer, Playground, and Studio. After those migrations are complete, use Section 25 as the cleanup contract for SecureAgent and Platform.
