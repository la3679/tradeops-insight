<!-- LOVABLE:BEGIN -->

> [!IMPORTANT]
> This project is connected to [Lovable](https://lovable.dev). Avoid rewriting
> published git history — force pushing, or rebasing/amending/squashing commits
> that are already pushed — as it rewrites history on Lovable's side and the
> user will likely lose their project history.
>
> Commits you push to the connected branch sync back to Lovable and show up in
> the editor, so keep the branch in a working state.

<!-- LOVABLE:END -->

# TradeOps Copilot agent guidelines

TradeOps Copilot is an independent educational portfolio project. It is not affiliated with, endorsed by, or derived from the proprietary systems of any financial institution. It never executes trades and uses only synthetic or license-compatible public data.

## Repository map

- `apps/web`: React/TypeScript operations console.
- `apps/api`: FastAPI application and transport adapters.
- `apps/worker`: asynchronous jobs and outbox consumers.
- `packages`: domain, data-connector, orchestration, and observability packages.
- `data`: small synthetic fixtures and provenance manifests only.
- `docs`: architecture, decisions, operations, evaluation, security, and guides.
- `evals`: versioned deterministic evaluation cases and runners.
- `infra`: local containers, telemetry provisioning, and optional AWS reference code.
- `scripts`: repeatable developer and release utilities.

Do not create artificial services or shared packages when a clear module boundary is enough. Domain logic must not depend on FastAPI, an LLM provider, a vector store, or a public-data API.

## Command surface

Use the root `Makefile` as the documented interface once available: `make bootstrap`, `make format`, `make lint`, `make typecheck`, `make test`, `make eval`, `make build`, and `make verify`. Until a command exists, use the package-native equivalent and record the exact result in `PROJECT_STATE.md`.

Never claim a command passed unless it was run. Report checks as passed, failed, not run, or not applicable.

## Clean-room and security rules

- Never request, copy, infer, imitate, or commit employer code, prompts, schemas, credentials, infrastructure details, private documents, internal names, branding, screenshots, or datasets.
- Never use real customer, trader, counterparty, employee, account, position, or transaction data.
- Never expose API keys, tokens, authorization headers, raw prompts, or secret-bearing traces.
- Treat model output, public records, uploaded documents, and retrieved chunks as untrusted data.
- No unrestricted shell, arbitrary code, unrestricted SQL, broad database mutation, or arbitrary outbound-network tool may be exposed to a model.
- Money, quantities, dates, permissions, policy checks, validation, and final action authorization remain deterministic.
- Material or uncertain demo-state changes require a recorded human approval and an idempotency key.
- Frontend visibility is never an authorization boundary; enforce protected operations server-side.
- External adapters use explicit allowlists, timeouts, bounded retries, circuit breakers, validation, caching, and provenance.

Lovable owns presentation work only. Security decisions, authorization enforcement, financial rules, model/tool permissions, secrets, and backend mutations require reviewed repository code.

## Engineering standards

### Python

- Use supported Python, `uv`, typed public APIs, Pydantic v2 models, SQLAlchemy 2 async patterns, Ruff, and strict or near-strict type checking.
- Inject external clients at boundaries; do not hide mutable global clients.
- Use a domain-specific error taxonomy. Never swallow broad exceptions.
- Store monetary and quantity values with fixed precision and timestamps in UTC.

### TypeScript and React

- Keep `strict: true`; avoid `any`, production `console.log`, and scattered direct `fetch` calls.
- Separate server state, UI state, and presentation. Do not duplicate backend rules.
- Use semantic HTML, visible focus, keyboard navigation, error boundaries, and accessible names.
- Keep components focused and use design tokens from `src/styles.css`.

### General

- Prefer clear names and pragmatic SOLID boundaries over speculative abstraction.
- Keep installs reproducible with committed lockfiles.
- Update docs beside behavior, configuration, contracts, or architecture.
- Do not leave dead code, commented-out implementations, unresolved TODO features, or user-facing placeholders in a release.

## Tests and review

- Add behavior and boundary tests with each capability, including negative authorization, idempotency, retries, conflicts, and fallback paths.
- CI must not depend on public internet or real-model credentials.
- Use recorded, sanitized fixtures for external adapters and deterministic mock-provider evaluations.
- Review every generated diff. Lovable and model-generated code are drafts until tests, type checks, lint, and build pass.
- Run the smallest relevant checks before each commit and the full `make verify` gate before release.

## Git discipline

- Work on focused branches; keep `main` stable.
- Use Conventional Commits and stage files selectively by purpose.
- Commit coherent tested units; never create filler, empty, backdated, whitespace-only, or artificially split commits.
- Push checkpoints after roughly three to five meaningful commits and update `PROJECT_STATE.md` with the last SHA, commands, known issues, and next actions.
- Do not squash the complete initial-release history or rewrite history consumed by Lovable or collaborators.

## Definition of done

A change is complete only when its behavior, tests, types, lint, formatting, security implications, documentation, and operational impact have been addressed; generated artifacts are current; no secrets or restricted material are present; and `PROJECT_STATE.md` reflects reality.
