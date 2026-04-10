#!/usr/bin/env bash
# Start the FakeProd API server.
# Usage: ./start.sh [port]   (default port: 8000)
#
# Optional env vars:
#   FAKEPROD_API_KEY   Bearer token agents must send (default: dev-secret-token-abc123)
#   PORT               Override port (same as the positional arg)

set -euo pipefail

PORT="${1:-${PORT:-8000}}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> FakeProd API"
echo "    Swagger UI : http://localhost:${PORT}/docs"
echo "    ReDoc      : http://localhost:${PORT}/redoc"
echo "    Bearer key : ${FAKEPROD_API_KEY:-dev-secret-token-abc123}"
echo ""

cd "$SCRIPT_DIR"

# Install deps into a venv if not already present.
if [[ ! -d .venv ]]; then
  echo "==> Creating virtualenv..."
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

pip install -q -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port "$PORT" --reload
