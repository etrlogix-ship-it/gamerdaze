# 03 🪓 Valheim Server

**Category:** 🖥️ Game Servers
**Difficulty:** ⭐⭐ Intermediate
**Time:** 30 minutes

## What You'll Make
Run your own Valheim dedicated server for you and your Viking crew. Persistent world, your own rules, no sleeping schedule conflicts!

## What You'll Need
- Steam account (Valheim Dedicated Server is free on Steam)
- Linux server or PC with 4GB+ RAM recommended
- SteamCMD installed

## Install SteamCMD
```bash
# Ubuntu/Debian
sudo apt install steamcmd

# Or download from: https://developer.valvesoftware.com/wiki/SteamCMD
```

## How to Run
```bash
cd code
python3 valheim_server.py
```

## Manual Start Command
```bash
./valheim_server.x86_64 \
  -name "My Viking Server" \
  -port 2456 \
  -world "MyWorld" \
  -password "secretpassword" \
  -public 1
```

## Key Settings
| Setting | Description |
|---------|-------------|
| `-name` | Server name shown in browser |
| `-world` | World save file name |
| `-password` | Password to join (min 5 chars) |
| `-public 1` | Show in public server list |
| `-port 2456` | Default port (open 2456-2458 UDP) |

## Ports to Forward
- 2456 UDP
- 2457 UDP
- 2458 UDP

## World Backups
World files are at: `~/.config/unity3d/IronGate/Valheim/worlds/`
Back these up regularly! (See project 17)
