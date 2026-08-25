# AI system card

- **Owner:** AI, product, and security maintainers
- **Purpose:** State what model-assisted behavior can and cannot do in the initial release.

## Intended behavior

Model-assisted components may triage a documented exception, summarize bounded evidence, and draft an allowlisted synthetic resolution proposal. Inputs contain synthetic case summaries, deterministic findings, and versioned evidence snippets. Outputs are schema validated and include confidence, assumptions, citations, refusal state, and non-secret provider metadata.

## Authority boundary

Provider output is advisory data. It cannot calculate authoritative amounts/dates, set severity or risk, grant permission, select arbitrary tools, change policy, or mutate state. Deterministic validation and citation gates run afterward. Material or uncertain proposals pause for an authorized supervisor, and the executor accepts only an exact single-use approval.

## Default provider

`mock` is the default and the only provider used by CI. It is deterministic, no-key, and offline. Without evidence it refuses. With evidence, it can select only the first action explicitly supplied by deterministic policy and cites the exact first chunk. Adversarial evidence text cannot add an action.

The mock provider demonstrates contracts and control flow; its confidence is not a measured probability and it makes no quality claim about a hosted model.

## Optional providers

OpenAI, Bedrock, and local adapters are optional boundaries. They require explicit startup configuration, must use the same typed contract, and do not silently fall back to another hosted provider. Real-provider evaluations run separately from deterministic CI and record provider/model/config versions.

## Known limitations

- Current behavior does not establish production accuracy, fairness, latency, cost, or operational benefit.
- Synthetic policies and cases do not represent any financial institution's procedures.
- Provider refusals and citation presence do not alone prove factual correctness.
- Prompt injection, unsupported claims, missing citations, provider failure, and stale evidence must remain explicit evaluation categories.

## Data handling

No real trade, customer, account, employee, employer, credential, authorization token, or secret is permitted. Raw prompts/responses are not logged by default. Telemetry stores bounded metadata and approved redacted digests.
