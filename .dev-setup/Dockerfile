FROM python:3.11-slim

WORKDIR /app

# Install git and pre-commit stuff for code quality checks.

RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/*

# Configure git to consider /app a safe directory (needed for CI).
RUN git config --global --add safe.directory /app

RUN pip install --no-cache-dir pre-commit black isort flake8 flake8-bugbear flake8-absolute-import mypy
