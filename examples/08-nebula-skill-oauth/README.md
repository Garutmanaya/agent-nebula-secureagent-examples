# 08 — Skill-Level OAuth / Least Privilege

This example connects the Agent Nebula skill-selection extension to OAuth least privilege. Each advertised A2A skill has a distinct OAuth scope. The client selects an exact `AgentSkill.id`; Platform resolves that skill's security requirement before sending the request and requests only the required scope. The provider validates authorization before dispatch.

Agent Nebula's **Policy** service is conceptually downstream of OAuth authorization: deployments can use policy to decide whether a subject/client/resource/scope combination is permitted. The example intentionally keeps policy logic outside SecureAgent business handlers.

Acceptance criterion: Registry discovery succeeds and all three skills succeed with their own scope requirements.
