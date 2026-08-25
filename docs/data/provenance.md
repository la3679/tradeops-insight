# Data source and provenance guide

Owner: data maintainer. Purpose: make every committed public fixture auditable.

`data/provenance/manifest.json` is authoritative. A fixture is accepted only when its source and terms URLs, UTC retrieval time, transformation, row count, path, and SHA-256 hash are present and verified. GLEIF, SEC EDGAR, and Treasury fixtures contain one transformed public record each and never supply trade data.

To refresh: review current terms and robots/rate guidance; fetch only from the allowlist with a descriptive user agent and timeout; minimize fields; inspect for personal/confidential content; recompute the hash; update the manifest and `DATA_LICENSES.md`; run provenance and full tests; obtain review. The default application remains fixture-only, so builds and tests never require the network.
