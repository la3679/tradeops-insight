# Developer setup

Owner: engineering maintainer. Purpose: reproduce local development.

Docker-first: copy `.env.example` to `.env`, run `docker compose up --build -d`, then check `docker compose ps` and `Invoke-RestMethod http://127.0.0.1:8000/api/v1/health/ready`. The web is at port 3000. Use `docker compose logs --tail=200 api worker web` for diagnosis and `docker compose down` to stop without deleting volumes.

Host mode needs Node 24, Bun 1.4, Python 3.14, uv 0.12, and Docker for integration services. Run `bun install --frozen-lockfile`, `uv sync --directory backend --all-groups --locked`, and `npm run dev`. Use `uv run --directory backend uvicorn tradeops.api.app:app --reload` for a host API. Configuration is validated at startup; local values are documented in `.env.example`.

macOS/Linux use `cp .env.example .env` instead of `Copy-Item`. All other commands are cross-platform CLI commands.
