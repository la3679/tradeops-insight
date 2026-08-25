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

# TradeOps Copilot — agent guidelines

TradeOps Copilot is an independent educational portfolio project. It is not
affiliated with any financial institution, does not execute trades, and uses
only synthetic or public data.

## Ownership boundaries

Security, authorization, financial/business rules, model behaviour, and all
backend logic are **owned and reviewed outside Lovable**. Lovable's scope in
this repository is frontend structure, presentation, accessibility, and
design-system work.

- Do not add authentication/authorization enforcement, entitlement logic, or
  secret handling here.
- Do not encode financial rules, pricing, break-classification, or settlement
  logic as frontend behaviour.
- Do not add model/LLM calls, external API integrations, or data persistence
  without an explicit, separately reviewed request.

## Review requirements

All Lovable output is a draft: it requires human review and tests before it is
relied upon. Treat generated code as unverified until reviewed.

## Coding rules

- TypeScript strict mode; no casual `any`. Model unknown data as `unknown` and
  narrow it.
- No `console.log` in production paths.
- No invented performance, accuracy, latency, or compliance claims in copy.
- All mock data must be deterministic and clearly labelled as synthetic.
- Colors, spacing, and typography come from design tokens in `src/styles.css`;
  never hardcode color utilities in components.
- Keep components small and focused; prefer composition over prop explosions.
