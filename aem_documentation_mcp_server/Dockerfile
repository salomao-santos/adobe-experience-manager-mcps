# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM public.ecr.aws/docker/library/python:3.13-alpine AS builder

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Prefer the system python
ENV UV_PYTHON_PREFERENCE=only-system

# Python optimization
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies and uv
RUN apk update && \
    apk add --no-cache --virtual .build-deps \
    build-base \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy project files
COPY pyproject.toml README.md LICENSE NOTICE ./
COPY adobelabs ./adobelabs

# Install dependencies
RUN source $HOME/.local/bin/env && \
    uv venv && \
    uv pip install -e .

# Production stage
FROM public.ecr.aws/docker/library/python:3.13-alpine

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# Install runtime dependencies and create application user
RUN apk update && \
    apk add --no-cache ca-certificates && \
    update-ca-certificates && \
    addgroup -S app && \
    adduser -S app -G app -h /app

# Copy application from builder
COPY --from=builder --chown=app:app /app /app

# Run as non-root
USER app
WORKDIR /app

# Entry point
ENTRYPOINT ["adobelabs.aem-documentation-mcp-server"]
