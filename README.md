## macOS / Linux
### Method A: Run everything (Postgres + FastAPI + Web)
```
chmod +x ./start.sh
./start.sh all
```

### Method B: Run web only (point to LAN API)
```
chmod +x ./start.sh
./start.sh web-only http://192.168.1.50:8000
```


## Windows (PowerShell)
### Method A: Run everything (Postgres + FastAPI + Web)
```
.\start.ps1 -Mode all
```

### Method B: Run web only (point to LAN API)
```
.\start.ps1 -Mode web-only -ApiBaseUrl "http://192.168.1.50:8000"
```