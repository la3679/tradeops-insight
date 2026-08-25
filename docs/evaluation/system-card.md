# AI system card

Owner: AI maintainer. Purpose: state model behavior, controls, and limitations.

The system classifies exceptions and drafts evidence-grounded resolution suggestions. It does not calculate authoritative financial values, execute trades, authorize users, or mutate state directly. Deterministic rules, typed schemas, citations, confidence/assumption fields, injection detection, policy gates, role checks, and human approval surround model output.

The default `mock/deterministic-v1` provider is zero-cost and replayable. Optional providers are adapters, not required capabilities. Expected failures include weak retrieval, unfamiliar language, stale references, contradictory evidence, provider outage, and adversarial documents; safe behavior is escalation. Evaluation measures routing/structure/safety expectations on synthetic cases, not real-world accuracy, fairness, suitability, or compliance.
