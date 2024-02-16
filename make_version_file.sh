#!/usr/bin/env sh

CODE_HASH=$(find proxycroak  \( -type d -name .mypy_cache -prune \) -o \( -type d -name __pycache__ -prune \) -o \( -type f -not -name "*.log" -not -name "*.webp" -exec sha256sum {} \; \) | sort | sha256sum | awk '{print $1}')

echo $CODE_HASH

echo -n "$(date +'%Y.%m.%d')\n$CODE_HASH" > VERSION
