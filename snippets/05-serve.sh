#!/usr/bin/env bash
set -euo pipefail

readonly PORT=${1:-3030}
echo "Starting dev server on port $PORT"

if ! lsof -i :$PORT >/dev/null 2>&1; then
  bun run dev -- --port $PORT --remote
fi
