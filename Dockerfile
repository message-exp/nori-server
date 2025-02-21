FROM python:3.12-slim AS base

ENV POETRY_VERSION=2.0.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PATH="/opt/poetry/bin:$PATH"

RUN apt-get update && apt-get install -y gcc grpc-proto libpq-dev protobuf-compiler && \
    rm -rf /var/lib/apt/lists/* && \
    pip install poetry

FROM base AS builder

COPY pyproject.toml poetry.lock /app/

WORKDIR /app

RUN poetry install --no-root

FROM base

WORKDIR /app

COPY --from=builder /app /app

COPY src /app/src
COPY scripts /app/scripts
RUN poetry run python scripts/generate.py

CMD ["poetry", "run", "python", "src/main.py"]
