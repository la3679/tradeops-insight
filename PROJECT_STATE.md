# Project state

## Current checkpoint

- **Phase:** 1 — architecture and service skeleton
- **Branch:** `feature/initial-project-release`
- **Canonical repository:** `la3679/tradeops-insight` (private; rename to `tradeops-copilot` is pending)
- **Lovable project:** `d5b87042-8fcf-41cf-aa66-075bf21f45ba`
- **Baseline source commit:** `5bcd2c578498136844041f9d359a64f8d38971ef`

## Completed

- Resolved connected GitHub and Lovable identities.
- Confirmed no pre-existing TradeOps repository or duplicate Lovable project.
- Created the private Lovable project and connected its GitHub sync.
- Created `feature/initial-project-release` from `main`.
- Added persistent Lovable project knowledge covering clean-room, security, UI, and review boundaries.
- Reviewed the generated frontend foundation and reconstructed the synced tree in the verification workspace.
- Documented the approved product scope and non-goals.
- Added repository, contribution, security, support, licensing, and data-attribution standards.
- Replaced generated metadata and established repeatable frontend quality commands.
- Added the documentation index, release roadmap, and changelog.

## Last verified commands

| Command              | Result |
| -------------------- | ------ |
| `prettier --check .` | Passed |
| `eslint .`           | Passed |
| `tsc --noEmit`       | Passed |
| `vite build`         | Passed |

## Known issues

- The GitHub repository and Lovable display name still use `tradeops-insight`; rename is pending.
- The starter has no test runner or coverage gates yet.
- Direct private Git cloning is unavailable in this workspace; connected APIs are used for remote commits.
- Docker is not installed in the current verification runtime; Compose validation requires CI or another environment.

## Next three actions

1. Record the initial architecture, trust boundaries, and technology ADRs.
2. Add the Python service workspace and FastAPI health contract.
3. Add the deterministic synthetic exception-domain skeleton.
