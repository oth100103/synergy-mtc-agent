# Backend und Agent-Service von UnderCover (Python 3.12 mit uv)
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
# Erst nur die Abhängigkeiten installieren (wird gecacht)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
# Dann den Code
COPY backend ./backend
COPY agent ./agent
COPY data ./data
COPY api_rules.py ./
RUN uv sync --frozen --no-dev
ENV PATH="/app/.venv/bin:$PATH"
