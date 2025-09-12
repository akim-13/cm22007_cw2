FROM python:3.11-slim

WORKDIR /app

# Install git and pre-commit stuff for code quality checks.

RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pre-commit black isort flake8 flake8-bugbear mypy
