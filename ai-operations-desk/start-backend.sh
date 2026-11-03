#!/bin/sh
set -eu
cd "$(dirname "$0")/backend"
exec .venv/bin/langgraph dev --host 127.0.0.1 --port 2024 --no-browser --allow-blocking
