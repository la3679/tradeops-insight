FROM ghcr.io/astral-sh/uv:0.12.2-python3.14-trixie-slim

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get upgrade --yes \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --locked --no-dev --no-install-project
COPY src ./src
COPY alembic.ini ./
COPY migrations ./migrations
RUN uv sync --locked --no-dev

RUN groupadd --system tradeops && useradd --system --gid tradeops --home-dir /app tradeops \
    && chown -R tradeops:tradeops /app
USER tradeops

EXPOSE 8000
CMD ["uv", "run", "--locked", "--no-dev", "uvicorn", "tradeops.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
