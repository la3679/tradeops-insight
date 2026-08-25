# Synthetic data methodology

Owner: domain maintainer. Purpose: document deterministic generation and limits.

The generator uses stable seeds and namespaces to create 2,400 fictional fixed-income trade records. Three hundred records deliberately express all twelve exception families; remaining records are internally consistent controls. Counterparties, identifiers, amounts, dates, memos, statuses, and audit actors are generated—not perturbed real records.

Rules compare immutable facts and produce typed exceptions with explanations, evidence, severity, and review route. Settlement policy v1 implements weekends plus explicit demo holidays; it is not a universal calendar. Distribution and anomaly examples are chosen for test coverage, not realism or performance claims. Dataset or rule changes require a new version, reproducibility test, category-count assertion, and changelog entry.
