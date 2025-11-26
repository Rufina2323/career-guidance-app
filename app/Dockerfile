# FROM python:3.13-slim

# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# WORKDIR /app

# RUN uv sync

# EXPOSE 8080

# CMD ["uv", "run", "python", "main.py"]
FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync

COPY entities .
COPY services .
COPY main.py .

EXPOSE 8080

CMD ["uv", "run", "python", "main.py"]
