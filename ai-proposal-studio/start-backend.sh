#!/bin/sh
set -e
cd -- "$(dirname -- "$0")"
export LANGSMITH_TRACING=false
export LANGGRAPH_API_NO_ANALYTICS=1
exec .venv/bin/langgraph dev --host 127.0.0.1 --port 2025 --no-browser --allow-blocking
