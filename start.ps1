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
  Write-Host ("ERROR: " + $msg) -ForegroundColor Red
  exit 1
}

function Usage {
  Write-Host "Usage:"
  Write-Host "  .\start.ps1 -Mode all"
  Write-Host "  .\start.ps1 -Mode web-only -ApiBaseUrl http://<LAN_IP>:8000"
  Write-Host ""
  Write-Host "Examples:"
  Write-Host "  .\start.ps1 -Mode all"
  Write-Host "  .\start.ps1 -Mode web-only -ApiBaseUrl http://192.168.1.50:8000"
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
    Write-Host ("Open this in your browser: " + $url)
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

  Write-Host ("Config updated: apiBaseUrl = " + $url)
}

if (-not $Mode) {
  Usage
  exit 1
}

switch ($Mode) {
  "all" {
    Write-Host "Checking requirements for FULL stack..."

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

    Write-Config "http://127.0.0.1:8000"

    Write-Host "Starting Postgres + API + Web..."
    Push-Location $DistDir
    docker compose up -d --build
    Pop-Location

    Write-Host "Services started"
    Write-Host "Web: http://localhost:8080"
    Write-Host "API: http://localhost:8000"

    Open-Browser "http://localhost:8080"
  }

  "web-only" {
    if (-not $ApiBaseUrl) {
      Usage
      Fail "web-only requires -ApiBaseUrl http://<LAN_IP>:8000"
    }

    Write-Host "Checking requirements for WEB ONLY..."

    $py = Get-Python
    if (-not $py) {
      Fail "Python 3 is required (python/python3/py -3)."
    }

    Write-Config $ApiBaseUrl

    Write-Host "Serving web at http://localhost:8080"
    Open-Browser "http://localhost:8080"

    Push-Location (Join-Path $DistDir "web")
    & $py.Name @($py.Args + @("-m", "http.server", "8080"))
    Pop-Location
  }

  default {
    Usage
    exit 1
  }
}
