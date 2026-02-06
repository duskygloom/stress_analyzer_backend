FROM python:3.10-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

WORKDIR /app

RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]
