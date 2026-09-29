# 09 — A2A Client + Provider Agent

This is the first multi-agent Agent Nebula workflow. A downstream math agent registers `math.add`. A second SecureAgent is simultaneously an A2A provider and client: it exposes `operations.add`, discovers `math.add` through the **Agent Nebula Registry**, invokes the discovered provider, and returns the result to its caller.

No LLM is involved. Discovery and deterministic `skill_id` dispatch make the routing explicit and testable. This is the foundation for later enterprise orchestration examples.

Run three terminals after `make init example-09`: `make run example-09 provider`, `make run example-09 orchestrator`, then `make run example-09 client`.
