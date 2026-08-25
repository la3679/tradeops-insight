# Evaluation methodology

Owner: AI maintainer. Purpose: explain the replayable 50-case suite.

`golden-v1` contains exactly 50 deterministic cases covering the twelve exception categories plus missing evidence, malicious evidence, malformed input, low confidence, citation gates, provider fallback, each review decision, idempotency, and version conflict. Every case records case type, expected status, dataset, prompt, provider, and model versions.

Run `uv run --directory backend --locked python ../scripts/run_eval.py`. Temperature and estimated cost are zero in mock mode. A release fails on any unexpected result. New behavior adds cases without rewriting old expectations unless an explicit dataset version documents the reason.
