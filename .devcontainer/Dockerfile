FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

ENV PYTHONUNBUFFERED 1

RUN  apt-get update && apt-get install -y protobuf-compiler grpc-proto

COPY pyproject.toml poetry.lock ./
RUN pip install poetry \
    && poetry config virtualenvs.create false