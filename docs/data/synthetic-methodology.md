# Synthetic data methodology

- **Owner:** Data and domain maintainers
- **Purpose:** Make demo generation reproducible and clearly separate invented trades from public references.

## Boundary

Every trade, event, memo, confirmation state, exception label, and outcome is invented by this repository. Identifiers use reserved `TRD-DEMO-*`, `EVT-DEMO-*`, and `INST-DEMO-*` forms. Generated legal-entity-like identifiers start with `DEMO` and are never represented as public-source records.

Public adapters may later supply versioned reference context. They do not supply, endorse, or validate synthetic trades.

Every generator or public-source artifact carries a lowercase SHA-256 digest and a source ID registered in `data/provenance/sources.json`. The registry records reviewed terms, intended fields, and allowed hosts separately from the derived snapshot.

## Reproducibility

Generation receives an explicit integer seed and UTC generation time. It uses an isolated pseudo-random generator; it never reads the global random state or system clock. The same configuration and package version produce byte-equivalent value objects.

The default configuration produces 100 counterparties, 100 instruments, 3,000 trades, and 360 labeled exception scenarios. The fast-test profile produces 12 counterparties, 12 instruments, 120 trades, and 24 scenarios.

## Scenario balance

The first labeled records cycle through all twelve exception families. Consecutive cycles alternate resolvable and escalation labels, guaranteeing at least one of each in the fast profile. Baseline financial values are retained separately so deterministic rules can compare the intentionally modified trade with its synthetic confirmation version.

## Deliberate limits

- Prices, amounts, sides, dates, names, and memo phrases cover the rule paths; they do not model market behavior.
- Generated LEI-shaped values are reserved demo identifiers and must not be queried as real counterparties.
- Instrument identifiers are not CUSIPs, ISINs, FIGIs, or another licensed/proprietary scheme.
- Dataset size is portfolio-demo scale, not a throughput or capacity claim.
- The generator is not suitable for investment analysis, simulation, or risk measurement.
