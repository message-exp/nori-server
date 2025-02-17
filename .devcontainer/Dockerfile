FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y protobuf-compiler grpc-proto

RUN curl -L https://github.com/fullstorydev/grpcurl/releases/download/v1.9.2/grpcurl_1.9.2_linux_amd64.deb -o /tmp/grpcurl.deb && \
    dpkg -i /tmp/grpcurl.deb && \
    rm -f /tmp/grpcurl.deb

COPY pyproject.toml poetry.lock ./
RUN pip install poetry \
    && poetry config virtualenvs.create true