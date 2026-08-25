# Release process

Owner: release maintainer. Purpose: make releases reviewable and reproducible.

1. Update version, changelog, state, docs, evaluation, performance, and data-license evidence.
2. Run format, lint, types, unit/integration, coverage, contract, E2E, evaluation, container build, docs links, dependency/license, secret, code, and image scans.
3. Review reachable history for secrets, proprietary references, and personal data.
4. Verify Docker quick start from a clean clone and inspect screenshots/accessibility.
5. Push without rewriting Lovable-consumed history; require green CI/security checks.
6. Tag `v0.1.0`, create release notes/SBOM, and verify badges/links/default branch.

Any failed correctness/high/critical security gate blocks release. Public visibility is allowed only after privacy, data, license, and history audits pass.
