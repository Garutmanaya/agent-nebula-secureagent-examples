# 08 — Skill-Level OAuth / Least Privilege

This example connects the Agent Nebula skill-selection extension to OAuth least privilege. Each advertised A2A skill has a distinct OAuth scope. The client selects an exact `AgentSkill.id`; Platform resolves that skill's security requirement before sending the request and requests only the required scope. The provider validates authorization before dispatch.

Agent Nebula's **Policy** service is conceptually downstream of OAuth authorization: deployments can use policy to decide whether a subject/client/resource/scope combination is permitted. The example intentionally keeps policy logic outside SecureAgent business handlers.

Acceptance criterion: Registry discovery succeeds and all three skills succeed with their own scope requirements.

## Hosted-platform prerequisites

Complete [Agent Nebula registration and discovery](../../docs/NEBULA_REGISTRATION.md) before this test. Review the [OAuth scopes and policy test matrix](../../docs/NEBULA_OAUTH_POLICY.md). Public Nginx + ngrok automation is [pending DOC-P4](../../docs/NEBULA_NGROK_NGINX.md).
