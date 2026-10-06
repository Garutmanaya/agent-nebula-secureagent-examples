# Example 30 — A2UI Multi-Skill

The browser discovers the agent's skills from the AgentCard and presents them as clickable A2UI choices. Selecting a skill sends an A2UI `skill.select` action; the browser bridge validates the selected ID against the AgentCard and invokes that skill through the existing Agent Nebula skill-selection extension. Each native A2A skill then returns its own application-owned A2UI JSON surface.

- `inventory` → Rich `DataTable`
- `traffic` → Rich `BarChart`

Skill-selection and A2UI extension URIs are discovered from the AgentCard and activated with native a2a-sdk service parameters.

```bash
make init example-30
make run example-30 server
make run example-30 client
make run example-30 browser
```

Open `http://localhost:9130` and select either advertised skill.
