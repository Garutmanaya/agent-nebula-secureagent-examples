# 10 — API-Key Protected Agent — Platform prerequisite

This example is intentionally **not marked executable yet**. The current Platform has an `A2AApiKeyAuthenticator` and the A2A client can supply API-key credentials, but `SecureAgent` server composition has no configuration path that constructs/injects the required server-side `ApiKeyAuthenticator` from external secret material. Advertising an API-key `SecurityScheme` today would therefore fail closed at startup.

Do not bypass that check or hard-code a verifier in the example. The prerequisite is a Platform-owned server credential/verifier configuration boundary. Once added, this example should verify: Registry registration/discovery, HTTPS, API-key scheme advertisement, valid-key success, missing-key rejection, invalid-key rejection, and all advertised skills.

Agent Nebula Registry onboarding API keys and A2A endpoint API keys are separate credentials and must remain separate configuration concerns.
