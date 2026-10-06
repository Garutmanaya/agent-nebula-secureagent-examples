# Example 30 — A2UI Multi-Skill

## Purpose

Verifies interactive AgentCard-driven skill selection. The browser discovers the advertised skills, renders selectable choices, and invokes the selected skill through the existing Agent Nebula skill-selection extension. Each skill owns its own A2UI presentation.

## Flow

```text
AgentCard skills -> selection surface -> skill.select action
                                      -> skill-selection extension
                                      -> selected AgentExecutor
                                      -> selected-skill-surface
```

A2UI remains presentation/action protocol; it does not replace A2A skill dispatch. Catalog IDs and extension URIs are discovered from the AgentCard.

## Run

```bash
make init example-30
make run example-30 server
make run example-30 client
make run example-30 browser
```

Open `http://localhost:9130` and switch repeatedly between the advertised skills. The previous result surface is removed before the next result surface is created.
