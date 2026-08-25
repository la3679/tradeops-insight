# ADR-0009: Synthetic and public-data governance

- **Status:** Accepted
- **Date:** 2026-08-24

## Context

The portfolio needs realistic reference context without employer, customer, account, position, or transaction data. Some public financial datasets carry fees, redistribution restrictions, attribution requirements, or unclear automated-access terms. “Publicly reachable” does not mean reusable.

## Decision

Generate all trade, exception, memo, policy, approval, user, and outcome records deterministically from documented seeds. Use reserved fictional identifiers and names that cannot be confused with customer records.

Admit a public source only after recording its owner, authoritative URL, dataset/API, fields used, retrieval method, terms or license, attribution, cache/redistribution policy, retention, and review date in `DATA_LICENSES.md`. Each derived record carries source, retrieval time, content digest, and transformation version.

The initial external legal-entity adapter targets GLEIF data covered by its CC0 terms. U.S. Treasury Fiscal Data and SEC data remain candidate enrichments subject to adapter-specific review and respectful access controls. Fee-based FINRA feeds, CUSIP-licensed data, and unclear sources are excluded.

## Consequences

### Positive

- The demo is reproducible without exposing or implying private information.
- Public-source use is reviewable and removable.
- Cached and derived data retain provenance.
- CI remains offline and independent of third-party availability.

### Negative

- Synthetic scenarios require deliberate design to remain realistic.
- Source terms and schemas must be periodically reviewed.
- Some useful market datasets are intentionally unavailable.

## Guardrails

- External adapters use allowlisted hosts, identifiable user agents where required, timeouts, size limits, bounded retries, caching, and circuit breakers.
- Public content is treated as untrusted input and cannot supply model instructions.
- A source-term change can disable synchronization without disabling the core demo.
- No public-source record is represented as a live trading signal or recommendation.

## References

- [GLEIF open data terms](https://www.gleif.org/en/about/open-data)
- [U.S. Treasury Fiscal Data API](https://fiscaldata.treasury.gov/api-documentation/)
- [SEC developer resources](https://www.sec.gov/about/developer-resources)
