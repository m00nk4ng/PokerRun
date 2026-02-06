<h1 align="center">PokerRun</h1>
PokerRun is a local-first, LAN-enabled poker tracking application consisting of:

- Flutter Web frontend
- FastAPI backend
- PostgreSQL database
- All orchestrated with Docker Compose

The project is designed so one computer hosts the app, and other devices on the same network can access it via a browser (no extra setup required on client machines).

<br>

## Component Version
Flutter front end: v.0.4.5

FastAPI back end: v.0.4.5

<br>

## Requirements

### Host machine (the computer running PokerRun)

You only need:

- Docker Desktop
 - macOS / Windows: https://www.docker.com/products/docker-desktop
 - Linux: Docker Engine + Docker Compose plugin
- Python 3 (only used to update config.json)
 - python3, python, or py -3 are all supported

You **do NOT** need PostgreSQL installed locally.

PostgreSQL runs entirely inside Docker.

### Client machines (other devices on the LAN)

- A modern web browser (Chrome, Safari, Firefox, Edge)
- No installs required

<br>

## How to run

### macOS / Linux

#### Run everything (Postgres + FastAPI + Web)

```
chmod +x ./start.sh
./start.sh
```

What this does:

- Detects your LAN IP
- Updates the frontend config to point to the host’s API
- Starts PostgreSQL, API, and Web via Docker
- Opens the app in your browser

### Windows (PowerShell)
#### Run everything (Postgres + FastAPI + Web)

```
.\start.ps1
```

What this does:

- Detects your LAN IP
- Updates the frontend config to point to the host’s API
- Starts PostgreSQL, API, and Web via Docker
- Opens the app in your browser

If PowerShell blocks script execution, run once:

```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Alternatively, you can start with the following script

```
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

<br>

## Accessing the App

After startup, you will see output similar to:

```
Web (this computer): http://localhost:8080
Web (LAN):          http://192.168.1.50:8080
API (LAN):          http://192.168.1.50:8000
```

### On the host computer

Open:

```
http://localhost:8080
```

### On other devices (same Wi-Fi / LAN)

Open:

```
http://<HOST_LAN_IP>:8080
```

Example:

```
http://192.168.1.50:8080
```

<br>

## How to shutdown

### macOS / Linux / Windows

From the project directory:

```
docker compose down
```

This stops all services but keeps your data.

<br>

## Data Persistence

PokerRun data is stored in a Docker volume:

```
pgdata
```

This means:

- Data persists across restarts
- Data survives `docker compose down`
- Data is deleted only if you run:
 - `docker compose down -v`

### Backups

To back up the database, you can:

- Use pg_dump from inside the Postgres container
- Or back up the Docker volume
