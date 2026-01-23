param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("all", "web-only")]
  [string]$Mode,

  [string]$ApiBaseUrl
)

$ErrorActionPreference = "Stop"
$DistDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ConfigPath = Join-Path $DistDir "web\config.json"

function Fail([string]$msg) {
  Write-Host "❌ $msg" -ForegroundColor Red
  exit 1
}

function Command-Exists([string]$cmd) {
  return $null -ne (Get-Command $cmd -ErrorAction SilentlyContinue)
}

function Get-PythonCmd {
  if (Command-Exists "python3") { return "python3" }
  if (Command-Exists "python")  { return "python" }
  if (Command-Exists "py")      { return "py -3" }
  return $null
}

function Write-Config([string]$url) {
  $dir = Split-Path -Parent $ConfigPath
  New-Item -ItemType Directory -Force -Path $dir | Out-Null

  $data = @{}
  if (Test-Path $ConfigPath) {
    try {
      $data = Get-Content $ConfigPath -Raw | ConvertFrom-Json
    } catch {
      $data = @{}
    }
  }

  # Ensure we have a mutable object
  if ($data -isnot [hashtable] -and $data -isnot [pscustomobject]) {
    $data = @{}
  }

  $data | Add-Member -Force NoteProperty apiBaseUrl $url
  ($data | ConvertTo-Json -Depth 10) | Set-Content -Encoding UTF8 $ConfigPath

  Write-Host "✔ Config updated: apiBaseUrl = $url"
}

function Open-Browser([string]$url) {
  try {
    Start-Process $url | Out-Null
  } catch {
    Write-Host "🌐 Open this in your browser: $url"
  }
}

if ($Mode -eq "all") {
  Write-Host "▶ Checking requirements for FULL stack…"

  if (-not (Command-Exists "docker")) {
    Fail "Docker is not installed. Please install Docker Desktop."
  }

  # Check Docker daemon is running (equivalent to `docker info`)
  docker info *> $null
  if ($LASTEXITCODE -ne 0) {
    Fail "Docker is installed but not running. Start Docker Desktop and try again."
  }

  docker compose version *> $null
  if ($LASTEXITCODE -ne 0) {
    Fail "Docker Compose plugin not available."
  }

  $py = Get-PythonCmd
  if (-not $py) {
    Fail "Python 3 is required to update config.json."
  }

  Write-Config "http://127.0.0.1:8000"

  Write-Host "▶ Starting Postgres + API + Web…"
  Push-Location $DistDir
  docker compose up -d --build
  Pop-Location

  Write-Host "✔ Services started"
  Write-Host "🌐 Web: http://localhost:8080"
  Write-Host "🔌 API: http://localhost:8000"

  Open-Browser "http://localhost:8080"
}

elseif ($Mode -eq "web-only") {
  if (-not $ApiBaseUrl) {
    Fail "web-only requires -ApiBaseUrl http://<LAN_IP>:8000"
  }

  Write-Host "▶ Checking requirements for WEB ONLY…"

  $py = Get-PythonCmd
  if (-not $py) {
    Fail "Python 3 is required (python/python3/py -3)."
  }

  Write-Config $ApiBaseUrl

  Write-Host "🌐 Serving web at http://localhost:8080"
  Open-Browser "http://localhost:8080"

  Push-Location (Join-Path $DistDir "web")
  # Invoke python command string safely
  if ($py -eq "py -3") {
    py -3 -m http.server 8080
  } elseif ($py -eq "python3") {
    python3 -m http.server 8080
  } else {
    python -m http.server 8080
  }
  Pop-Location
}
