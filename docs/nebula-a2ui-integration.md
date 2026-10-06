# Agent Nebula A2UI Integration

## Scope and ownership

Agent Nebula carries A2UI as an A2A protocol extension. SecureAgent does not define an A2UI surface API, component API, action API, or data-model API. The application owns complete A2UI JSON protocol documents. Native `a2a-sdk` carries those documents in A2A messages, and the browser renderer processes them with `@a2ui/web_core` and registered catalogs.

```text
Application JSON                         Renderer
(createSurface/update...)                @a2ui/web_core
        |                                     ^
        v                                     |
AgentExecutor -> A2A DataPart -> A2A Client -> browser bridge
                   application/a2ui+json
```

The boundaries are:

- **SecureAgent / Platform**: load configuration, compose the A2A server/client, advertise configured extensions, security, registry/lifecycle, and skill dispatch.
- **a2a-sdk**: AgentCard, A2A Message/Part transport, AgentExecutor/RequestContext/EventQueue, client calls, extension activation, tasks/streaming where used.
- **Application**: business logic, application data, selection/loading of complete A2UI JSON documents.
- **A2UI renderer**: protocol validation, surface lifecycle, data binding, action construction, and rendering using registered catalogs.

## `a2ui.conf` and AgentCard advertisement

An A2UI-enabled example supplies `a2ui.conf` to SecureAgent:

```ini
[a2ui]
enabled = true
version = v1.0
supported_catalog_ids = https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json
default_catalog_id = https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json
accepts_inline_catalogs = false
```

Platform translates that configuration into the A2UI extension entry in the native AgentCard. Conceptually:

```text
a2ui.conf
   |
   v
SecureAgent / Platform
   |
   v
AgentCard.capabilities.extensions[]
   |
   +-- A2UI extension URI
       params
         v1.0
           supportedCatalogIds
           acceptsInlineCatalogs
```

The AgentCard is authoritative. Example clients do not hard-code the A2UI extension URI. They resolve the AgentCard, identify the A2UI extension by its v1.0 catalog parameters, and activate the discovered URI through native a2a-sdk service parameters.

## Catalogs

Every A2UI surface identifies the catalog used by the surface. A catalog is the contract between the JSON sent by the application and the components/functions implemented by the renderer.

The shared browser registers the official Basic Catalog and the Agent Nebula Rich Catalog once:

```text
examples/common/a2ui-web/src/catalogs.js
        |
        +-- Basic Catalog
        +-- Agent Nebula Rich Catalog
        |
        v
MessageProcessor(SUPPORTED_CATALOGS)
```

A catalog URI is an identifier for negotiation; it does not mean the browser dynamically downloads arbitrary component code. Renderer implementations are registered locally.

The Basic Catalog intentionally does not provide specialized `Table` or `Chart` wire components. Examples therefore must either compose a presentation from catalog-defined primitives or use a separately defined and registered custom catalog. They must not invent an undeclared component name on the wire.

## Client negotiation

The client first resolves the AgentCard, discovers the A2UI extension, and advertises renderer catalog support in `SendMessageRequest.metadata`:

```text
GET /.well-known/agent-card.json
        |
        v
find A2UI extension + advertised catalogs
        |
        v
SendMessageRequest.metadata
  a2uiRendererCapabilities
    v1.0
      supportedCatalogIds
        |
        + X-A2A-Extensions / native a2a-sdk extension activation
        |
        v
A2A server
```

Renderer capabilities are request metadata. On the server, native `RequestContext.metadata` is the corresponding application-facing access point. They are not read from `context.message.metadata`.

When an example also needs Agent Nebula skill selection, the client discovers both extensions from the AgentCard, places the selected skill under the discovered skill-selection metadata key, and activates both extension URIs through native a2a-sdk.

## A2UI over A2A

A2UI protocol documents are structured JSON. In these examples they are transported as an A2A `DataPart` with media type `application/a2ui+json`:

```text
A2A Message
  parts[]
    DataPart
      media_type = application/a2ui+json
      data
        messages[]
          { version: v1.0, createSurface: ... }
          { version: v1.0, updateDataModel: ... }
          ...
```

`a2ui_transport.py` is only a thin example-local A2A `DataPart` helper. It does not implement A2UI semantics.

## Surface creation

The complete surface definition lives in JSON. Python loads the document and may bind invocation-specific business data into its data model; it does not define component trees or create an alternate surface API.

```text
presentation.json
  version: v1.0
  createSurface
    surfaceId
    catalogId
    components[]
    dataModel
        |
        v
application loads JSON
        |
        +-- bind runtime business data
        |
        v
AgentExecutor
        |
        v
new_message([A2A DataPart])
        |
        v
A2A client/browser
        |
        v
MessageProcessor.processMessages()
        |
        v
SurfaceModel + registered catalog renderer
```

`createSurface` creates the renderer-side surface and chooses its catalog. Later `updateComponents`, `updateDataModel`, and `deleteSurface` messages operate on that surface. A2UI v1.0 also defines `actionResponse` for synchronous client-initiated RPC behavior.

## Actions and forms

Actions originate in a catalog component declared in application JSON. The renderer resolves bindings and constructs the A2UI action. The browser bridge transports that A2UI document back inside a native A2A Message.

```text
Button / form component
        |
        v
@a2ui/web_core
  resolves bound action context
  reads synchronized surface model
        |
        v
A2UI action document
        |
        v
A2A Message/DataPart
        |
        v
AgentExecutor
  validates action + business input
        |
        v
application-owned update JSON
        |
        v
A2A Message/DataPart
        |
        v
MessageProcessor -> existing surface updated
```

If `createSurface.sendDataModel` is enabled, the renderer can return synchronized surface state. In these examples that state is request metadata (`a2uiClientDataModel`) and is read through `RequestContext.metadata`. Business validation remains application logic.

## Tables and charts

Examples 28 and 29 use components declared by the Agent Nebula Rich Catalog. Example 28 renders structured application data with `DataTable`; Example 29 renders application data with `BarChart`. The component definitions remain in application-owned JSON presentation files. Python binds business data and transports the resulting A2UI messages; it does not construct a second component model.

The client discovers the A2UI extension and advertised catalog IDs from the AgentCard instead of duplicating catalog URI constants in Python.

## Multi-skill

A2UI does not change A2A skill dispatch. Example 30 uses Agent Nebula's existing skill-selection extension to select a native AgentExecutor. Each skill independently owns its A2UI JSON presentation:

```text
AgentCard
  skills: inventory, traffic
  extensions: skill-selection, A2UI
        |
        v
Client selects skill + activates both extensions
        |
        v
SecureAgent native A2A dispatch
        |
        +-- inventory AgentExecutor -> inventory.json
        |
        +-- traffic AgentExecutor   -> traffic.json
        |
        v
native A2A Message containing A2UI DataPart
```

Platform does not choose the A2UI surface and does not translate skill results into UI.

## Common browser renderer

The shared renderer is under `examples/common/a2ui-web`:

- `src/catalogs.js` registers supported catalogs.
- `src/surfaceState.js` creates the official `MessageProcessor`, performs strict v1.0 processing, and exposes synchronized renderer data.
- `src/Renderer.jsx` maps validated catalog components to browser presentation and delegates registered Rich components.
- `src/main.jsx` fetches A2UI documents from the example bridge and returns renderer actions/state to the bridge.

This code is shared presentation infrastructure only. It is not part of SecureAgent and is not an A2UI protocol implementation replacement; `@a2ui/web_core` remains responsible for A2UI parsing, validation, lifecycle, bindings, and action construction.

## End-to-end flow

```text
1. Server startup
   a2ui.conf -> SecureAgent/Platform -> AgentCard A2UI extension

2. Discovery
   client -> /.well-known/agent-card.json
          <- A2UI extension + supportedCatalogIds + skills

3. Activation
   client -> native a2a-sdk call context -> activate discovered A2UI URI

4. Renderer capability negotiation
   SendMessageRequest.metadata
     a2uiRendererCapabilities.v1.0.supportedCatalogIds

5. Skill execution
   native a2a-sdk -> RequestContext -> AgentExecutor

6. UI creation
   application loads complete presentation.json
   application binds business data only

7. A2UI transport
   AgentExecutor -> A2A Message -> DataPart(application/a2ui+json)

8. Rendering
   browser -> @a2ui/web_core MessageProcessor -> SurfaceModel -> catalog renderer

9. Interaction (Actions/Forms)
   renderer action + synchronized state -> A2A -> AgentExecutor

10. Incremental result
   application loads update JSON -> updateDataModel/updateComponents -> A2A -> existing surface
```


## Native Tasks, streaming, and security

Examples 31–34 verify that A2UI composes with native A2A lifecycle and Agent Nebula security without adding alternate abstractions:

- Example 31 carries A2UI in a native Task artifact and exposes the actual Task metadata in browser validation.
- Example 32 carries incremental A2UI messages in native streaming artifact updates and forwards each update to the persistent browser `MessageProcessor` as it arrives.
- Example 33 applies the existing HTTPS/OAuth A2A security path to a request carrying A2UI; there is no A2UI-specific security layer.
- Example 34 combines HTTPS/OAuth, AgentCard-driven multi-skill dispatch, native Task/streaming behavior, and A2UI presentation in one agent.

Across these examples, the AgentCard remains authoritative for A2UI extension discovery and advertised catalog IDs. Native `a2a-sdk` types own Message, Task, Artifact, status, and streaming semantics.

The architectural invariant is: **A2A transports and dispatches; A2UI describes UI; the application owns UI JSON and business behavior; the renderer owns rendering; SecureAgent does not duplicate any of those protocol APIs.**
