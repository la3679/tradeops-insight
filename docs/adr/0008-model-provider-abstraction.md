# ADR 0008: Model-provider abstraction and fallback

Status: accepted. Orchestration depends on a typed provider port. The deterministic mock is the default and CI authority. Optional OpenAI, Bedrock, or local adapters must expose provider/model versions, bounded calls, structured output, and explicit fallback. Provider failures escalate rather than silently changing domain rules.
