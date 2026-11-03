#!/bin/sh
set -e
cd -- "$(dirname -- "$0")/frontend"
exec npm run dev
