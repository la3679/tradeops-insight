# Contributing

Thank you for helping improve TradeOps Copilot. This repository is a clean-room educational portfolio project; contributions must preserve its synthetic-only, no-trade-execution boundary.

## Before opening a change

1. Read `AGENTS.md`, `docs/product/product-brief.md`, and `docs/product/non-goals.md`.
2. Search existing issues and decisions before proposing a new dependency or architecture.
3. Open a focused issue for material product, security, data-source, or infrastructure changes.
4. Never include real financial, employer, customer, account, transaction, credential, or proprietary material.

## Development workflow

1. Branch from current `main` using a descriptive prefix such as `feature/`, `fix/`, `docs/`, or `chore/`.
2. Keep changes coherent and add tests beside behavior.
3. Use Conventional Commit messages.
4. Run the relevant formatting, lint, type, test, evaluation, and build commands.
5. Update documentation and `PROJECT_STATE.md` when contracts, behavior, commands, or architecture change.
6. Open a pull request using the repository template and disclose what was not run.

## Pull-request expectations

A reviewable pull request explains the problem and scope; links decisions or issues; includes test evidence; identifies security, privacy, data-license, migration, and operational impact; provides screenshots for meaningful UI changes; and states limitations honestly.

Generated code is welcome only when the contributor has reviewed, understood, tested, and accepts responsibility for it. Do not submit a generated dump or fabricate review evidence.

## Reporting security concerns

Do not open a public issue for a suspected vulnerability or exposed secret. Follow `SECURITY.md`.
