# Deterministic reconciliation

- **Owner:** Domain maintainers
- **Purpose:** Describe the framework-free rule input, ordering, and output contract.

The reconciliation facade accepts one immutable synthetic trade plus a caller-assembled context: versioned counterparty and instrument references, comparison financials, evaluation time, seen identifiers/fingerprints, memo conflicts, payload issues, and explicit policies. It performs no I/O.

Rules run in stable order:

1. legal-entity validity, lookup, status, and name;
2. product, instrument, currency, and reference freshness;
3. exact-Decimal quantity, notional, and price comparison;
4. business-day settlement and duplicate detection;
5. confirmation, memo, and normalized-payload checks.

The report preserves every finding in that order. Each finding includes one of twelve stable families, deterministic severity and risk, an explanation, suggested next actions, bounded evidence, and a review flag. The facade never chooses a model, retrieves a document, writes a database, or applies a correction.

## Why invalid values can reach the domain

Transport parsing rejects data that cannot be safely bounded or represented. Operationally meaningful invalid values—such as a short LEI, unsupported product string, or non-ISO currency—remain bounded strings so the system can produce a specific, auditable exception instead of collapsing them into a generic server error.

## Replay contract

Given the same normalized trade, context, policy versions, and Python/domain package version, reconciliation is deterministic. Timestamps are supplied by the caller, not read from the system clock. Set membership and comparisons are side-effect free.
