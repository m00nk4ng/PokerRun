#!/usr/bin/env bash
set -euo pipefail

DIST_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_PATH="$DIST_DIR/web/config.json"

fail() {
  echo "❌ $1"
  exit 1
}

check_command() {
  command -v "$1" >/dev/null 2>&1
}

usage() {
  echo "Usage:"
  echo "  ./start.sh all"
  echo "  ./start.sh web-only <API_BASE_URL>"
  echo ""
  echo "Examples:"
  echo "  ./start.sh all"
  echo "  ./start.sh web-only http://192.168.1.50:8000"
}

open_browser() {
  local url="$1"
  if command -v open >/dev/null 2>&1; then
    open "$url" || true
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$url" || true
  else
    echo "🌐 Open this in your browser: $url"
  fi
}

write_config() {
  local api_url="$1"

  CONFIG_PATH="$CONFIG_PATH" API_BASE_URL="$api_url" python3 - <<'PY'
import json, os

path = os.environ.get("CONFIG_PATH")
api_url = os.environ.get("API_BASE_URL")

if not path:
    raise SystemExit("CONFIG_PATH environment variable is missing")
if not api_url:
    raise SystemExit("API_BASE_URL environment variable is missing")

os.makedirs(os.path.dirname(path), exist_ok=True)

data = {}
if os.path.exists(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}

data["apiBaseUrl"] = api_url

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"✔ Config updated: apiBaseUrl = {api_url}")
PY
}



MODE="${1:-}"
[[ -z "$MODE" ]] && usage && exit 1

case "$MODE" in
  all)
    echo "▶ Checking requirements for FULL stack…"

    check_command docker || fail "Docker is not installed. Please install Docker first."
    docker info >/dev/null 2>&1 || fail "Docker is installed but not running. Start Docker Desktop and try again."
    docker compose version >/dev/null 2>&1 || fail "Docker Compose plugin not found."

    check_command python3 || fail "python3 is required to update config.json."

    write_config "http://127.0.0.1:8000"

    echo "▶ Starting Postgres + API + Web…"
    (cd "$DIST_DIR" && docker compose up -d --build)

    echo "✔ Services started"
    echo "🌐 Web: http://localhost:8080"
    echo "🔌 API: http://localhost:8000"

    open_browser "http://localhost:8080"
    ;;
    
  web-only)
    API_URL="${2:-}"
    [[ -z "$API_URL" ]] && usage && exit 1

    echo "▶ Checking requirements for WEB ONLY…"
    check_command python3 || fail "Python 3 is required (python3)."

    write_config "$API_URL"

    echo "🌐 Serving web at http://localhost:8080"
    open_browser "http://localhost:8080"

    (cd "$DIST_DIR/web" && python3 -m http.server 8080)
    ;;
    
  *)
    usage
    exit 1
    ;;
esac
