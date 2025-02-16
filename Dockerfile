FROM python:3.12-alpine AS base

ENV POETRY_VERSION=2.0.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PATH="/opt/poetry/bin:$PATH"

RUN apk add --no-cache bash curl grpc-proto protobuf-compiler&& \
    curl -sSL https://install.python-poetry.org | python3 -

FROM base AS builder

COPY pyproject.toml poetry.lock /app/

WORKDIR /app

RUN poetry install --no-root --extras dev

FROM base

WORKDIR /app

COPY --from=builder /app /app

COPY src /app/src

CMD ["poetry", "run", "python", "src/main.py"]
