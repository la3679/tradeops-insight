# Data attribution and license review

Application trades, exceptions, policies, users, and audit events are independently generated synthetic data licensed with this repository under Apache-2.0.

The public fixture set contains one transformed record from each source:

| Source                    | Purpose                      | Terms                                                                    |
| ------------------------- | ---------------------------- | ------------------------------------------------------------------------ |
| GLEIF Global LEI Index    | entity-reference shape       | [GLEIF terms](https://www.gleif.org/en/meta/lei-data-terms-of-use)       |
| SEC EDGAR Submissions API | public filer-reference shape | [SEC developer resources](https://www.sec.gov/about/developer-resources) |
| U.S. Treasury Fiscal Data | security schedule shape      | [Fiscal Data API](https://fiscaldata.treasury.gov/api-documentation/)    |

Exact URLs, retrieval timestamps, transformations, row counts, paths, and SHA-256 hashes are in `data/provenance/manifest.json`. These sources provide reference context only; they did not provide synthetic trade records. Re-users must review current source terms before redistributing refreshed data.
