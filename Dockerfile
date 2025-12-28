FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync

# Copy migrations and other static files
COPY app /app

# Source files will be mounted via volume, so no need to copy main.py or other app files
EXPOSE 8080

CMD ["sh", "-c", "uv run alembic upgrade head && uv run python main.py"]
