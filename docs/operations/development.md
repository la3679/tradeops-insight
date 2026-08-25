# Developer setup

- **Owner:** Project maintainer
- **Purpose:** Provide one reproducible local command surface for the web and API foundations.

## Prerequisites

- Node.js 22 or 24 and npm
- Python 3.12
- [`uv`](https://docs.astral.sh/uv/)
- GNU Make for the convenience targets
- Docker with Compose for PostgreSQL/Redis-backed workflows; unit checks do not require Docker

## Bootstrap

```bash
make bootstrap
```

This installs the committed npm and `uv` lockfiles. No model key is required.

## Run the applications

Run the web console:

```bash
npm run dev
```

Run the API in a second terminal:

```bash
make run-api
```

The API publishes process health at `/health/live`, dependency readiness at `/health/ready`, service identity at `/api/v1/meta/version`, and non-production OpenAPI documentation at `/docs`.

## Quality commands

| Command          | Coverage                                      |
| ---------------- | --------------------------------------------- |
| `make format`    | Prettier and Ruff formatting                  |
| `make lint`      | ESLint and Ruff rules                         |
| `make typecheck` | TypeScript and strict mypy checks             |
| `make test`      | Python tests with branch coverage gate        |
| `make build`     | Web production build and Python distributions |
| `make verify`    | Complete local release gate                   |

## Configuration

API settings use the `TRADEOPS_` prefix. For example, `TRADEOPS_ENVIRONMENT=test` selects test behavior. The source-controlled defaults are safe for local synthetic-data use; secrets and provider credentials must come from the environment or a secret store and must never enter `.env` files committed to Git.

## Current environment limitation

The API and web checks are reproducible without containers. If Docker is unavailable, report container-backed checks as not run rather than treating them as passed. Alembic offline SQL rendering still verifies migration structure.

## Persistence services

Start the loopback-only PostgreSQL and Redis services, then migrate the database:

```bash
make infra-up
make migrate
```

The values in `.env.example` are local demo credentials, not deployable secrets. PostgreSQL volumes are preserved by `make infra-down`; no standard Make target destroys them.
