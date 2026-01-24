param(
  [ValidateSet("all")]
  [string]$Mode
)

$ErrorActionPreference = "Stop"

$DistDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ConfigPath = Join-Path $DistDir "web\config.json"

function Fail([string]$msg) {
  Write-Host ("❌ " + $msg) -ForegroundColor Red
  exit 1
}

function Command-Exists([string]$cmd) {
  return $null -ne (Get-Command $cmd -ErrorAction SilentlyContinue)
}

function Get-Python {
  if (Command-Exists "python3") { return @{ Name = "python3"; Args = @() } }
  if (Command-Exists "python")  { return @{ Name = "python";  Args = @() } }
  if (Command-Exists "py")      { return @{ Name = "py";      Args = @("-3") } }
  return $null
}

function Open-Browser([string]$url) {
  try {
    Start-Process $url | Out-Null
  } catch {
    Write-Host ("🌐 Open this in your browser: " + $url)
  }
}

function Write-Config([string]$url) {
  $dir = Split-Path -Parent $ConfigPath
  New-Item -ItemType Directory -Force -Path $dir | Out-Null

  $obj = $null
  if (Test-Path $ConfigPath) {
    try {
      $raw = Get-Content $ConfigPath -Raw
      if ($raw -and $raw.Trim().Length -gt 0) {
        $obj = $raw | ConvertFrom-Json
      }
    } catch {
      $obj = $null
    }
  }

  if (-not $obj) {
    $obj = [pscustomobject]@{}
  }

  $obj | Add-Member -Force NoteProperty apiBaseUrl $url
  ($obj | ConvertTo-Json -Depth 10) | Set-Content -Encoding UTF8 $ConfigPath

  Write-Host ("✔ Config updated: apiBaseUrl = " + $url)
}

function Get-LanIp {
  # Prefer the interface used for default route (best match for LAN)
  try {
    $route = Get-NetRoute -DestinationPrefix "0.0.0.0/0" -ErrorAction Stop |
      Sort-Object -Property RouteMetric, InterfaceMetric |
      Select-Object -First 1

    if ($route) {
      $ip = Get-NetIPAddress -AddressFamily IPv4 -InterfaceIndex $route.InterfaceIndex -ErrorAction Stop |
        Where-Object { $_.IPAddress -and $_.IPAddress -notlike "169.254.*" } |
        Select-Object -First 1

      if ($ip -and $ip.IPAddress) { return $ip.IPAddress }
    }
  } catch {}

  # Fallback: any non-loopback IPv4
  try {
    $ip2 = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction Stop |
      Where-Object {
        $_.IPAddress -and
        $_.IPAddress -ne "127.0.0.1" -and
        $_.IPAddress -notlike "169.254.*"
      } |
      Select-Object -First 1
    if ($ip2 -and $ip2.IPAddress) { return $ip2.IPAddress }
  } catch {}

  return "127.0.0.1"
}

# ------------------------------
# Main (always runs FULL stack)
# ------------------------------

Write-Host "▶ Checking requirements for FULL stack…"

if (-not (Command-Exists "docker")) {
  Fail "Docker is not installed. Please install Docker Desktop first."
}

docker info *> $null
if ($LASTEXITCODE -ne 0) {
  Fail "Docker is installed but not running. Start Docker Desktop and try again."
}

docker compose version *> $null
if ($LASTEXITCODE -ne 0) {
  Fail "Docker Compose plugin not found."
}

$py = Get-Python
if (-not $py) {
  Fail "Python 3 is required to update config.json."
}

$lanIp = Get-LanIp
$apiUrl = "http://$lanIp`:8000"
$webLanUrl = "http://$lanIp`:8080"

Write-Config $apiUrl

Write-Host "▶ Starting Postgres + API + Web…"
Push-Location $DistDir
docker compose up -d --build
Pop-Location

Write-Host "✔ Services started"
Write-Host "🌐 Web (this computer): http://localhost:8080"
Write-Host "🌐 Web (LAN):          $webLanUrl"
Write-Host "🔌 API (LAN):          $apiUrl"

Open-Browser "http://localhost:8080"
