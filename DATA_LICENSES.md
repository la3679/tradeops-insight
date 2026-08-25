# Data licenses and source policy

TradeOps Copilot uses synthetic trades, synthetic policies, and small public reference fixtures only. Public providers never supply the synthetic trades, outcomes, approvals, or operational metrics shown by the application.

## Current source decisions

| Source                          | Intended use                                                       | Current decision                                                                                                              | Terms or documentation                                                        |
| ------------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Project-authored synthetic data | Trades, exceptions, memos, policies, evaluations                   | Permitted under the repository license; must remain obviously synthetic                                                       | `LICENSE` and `docs/product/non-goals.md`                                     |
| GLEIF Global LEI Index          | Legal-entity reference context and small test fixtures             | Approved: access is free and LEI reference data is provided under CC0; do not use GLEIF branding or imply endorsement         | <https://www.gleif.org/en/meta/lei-data-terms-of-use>                         |
| SEC EDGAR JSON APIs             | Optional issuer metadata, filing history, and selected public text | Approved only through documented APIs with an identifying user agent, caching, bounded rate, and provenance; no browser calls | <https://www.sec.gov/search-filings/edgar-application-programming-interfaces> |
| U.S. Treasury Fiscal Data API   | Treasury auction/security reference context                        | Approved in principle; verify the selected dataset endpoint, fields, and current terms before committing a fixture            | <https://fiscaldata.treasury.gov/api-documentation/>                          |
| FINRA fixed-income pages        | Domain references and license-compatible aggregate context         | Reference-only by default. Do not ingest or redistribute fee-based TRACE feeds, subscriber data, or licensed identifiers      | <https://www.finra.org/filing-reporting/trace/data>                           |

## Required provenance

Before a public record or derived fixture is committed, `data/provenance/manifest.json` must record:

- provider and dataset name;
- source and terms URLs;
- retrieval timestamp in UTC;
- transformation and sanitization notes;
- committed row/document count;
- SHA-256 hash of the committed artifact;
- reviewer and license decision.

Do not commit large upstream datasets. Source synchronization must be explicit, cached, rate-limited, retry-bounded, and optional. CI uses recorded sanitized fixtures and never requires public-network access.

## Restricted material

Real trade/customer/account data, employer material, proprietary identifiers, fee-based feeds, credentials, and sources with unclear redistribution terms are prohibited. When terms are ambiguous, cite the source for domain background and generate an independent synthetic fixture instead.
