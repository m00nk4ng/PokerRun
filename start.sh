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

# Best-effort LAN IP detection (macOS + Linux)
get_lan_ip() {
  local ip=""

  # macOS: try Wi-Fi first, then any active interface
  if [[ "$(uname -s)" == "Darwin" ]]; then
    ip="$(ipconfig getifaddr en0 2>/dev/null || true)"   # Wi-Fi (common)
    [[ -z "$ip" ]] && ip="$(ipconfig getifaddr en1 2>/dev/null || true)" # some Macs
    [[ -z "$ip" ]] && ip="$(route -n get default 2>/dev/null | awk '/interface:/{print $2}' | xargs -I{} ipconfig getifaddr {} 2>/dev/null || true)"
  else
    # Linux: use ip route
    if check_command ip; then
      ip="$(ip route get 1.1.1.1 2>/dev/null | awk '{for(i=1;i<=NF;i++) if ($i=="src") print $(i+1)}' | head -n1)"
    fi
  fi

  # Fallback: parse hostname -I / ifconfig
  if [[ -z "$ip" ]]; then
    if check_command hostname; then
      ip="$(hostname -I 2>/dev/null | awk '{print $1}' || true)"
    fi
  fi

  # Final fallback: localhost
  [[ -z "$ip" ]] && ip="127.0.0.1"

  echo "$ip"
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

# Optional: accept "all" if user types it, but don't require anything.
MODE="${1:-}"
if [[ -n "$MODE" && "$MODE" != "all" ]]; then
  echo "Usage: ./start.sh"
  echo "  (optional: ./start.sh all)"
  exit 1
fi

echo "▶ Checking requirements for FULL stack…"

check_command docker || fail "Docker is not installed. Please install Docker first."
docker info >/dev/null 2>&1 || fail "Docker is installed but not running. Start Docker Desktop and try again."
docker compose version >/dev/null 2>&1 || fail "Docker Compose plugin not found."

check_command python3 || fail "python3 is required to update config.json."

LAN_IP="$(get_lan_ip)"
API_URL="http://${LAN_IP}:8000"
WEB_LAN_URL="http://${LAN_IP}:8080"

write_config "$API_URL"

echo "▶ Starting Postgres + API + Web…"
(cd "$DIST_DIR" && docker compose up -d --build)

echo "✔ Services started"
echo "🌐 Web (this computer): http://localhost:8080"
echo "🌐 Web (LAN):          $WEB_LAN_URL"
echo "🔌 API (LAN):          $API_URL"

open_browser "http://localhost:8080"
