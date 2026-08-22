FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl make \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && ln -s /root/.local/bin/uv /usr/local/bin/uv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /project