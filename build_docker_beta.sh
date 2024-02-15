#!/usr/bin/env sh

# Build the beta containers

CODE_HASH=$(find proxycroak  \( -type d -name .mypy_cache -prune \) -o \( -type d -name __pycache__ -prune \) -o \( -type f -not -name "*.log" -not -name "*.webp" -exec sha256sum {} \; \) | sort | sha256sum | awk '{print $1}')

echo $CODE_HASH


# Build the nginx container
docker build -t proxycroak-nginx:beta nginx -f nginx/Dockerfile.beta

# Build the proxycroak flask app
docker build -t proxycroak-web:beta . -f Dockerfile.beta --build-arg CODE_HASH=$CODE_HASH
