# 02 🪨 Minecraft Bedrock Server

**Category:** 🖥️ Game Servers
**Difficulty:** ⭐ Beginner
**Time:** 20 minutes

## What You'll Make
Set up a Minecraft Bedrock Edition server — perfect for players on Xbox, PlayStation, Nintendo Switch, mobile, and Windows 10/11 Edition. Cross-platform play out of the box!

## What You'll Learn
- Difference between Java and Bedrock servers
- Setting up a Bedrock Dedicated Server (BDS)
- Cross-platform multiplayer configuration

## What You'll Need
- Windows, Linux, or Mac (Linux recommended for best performance)
- At least 1GB RAM free
- Players on any Bedrock platform to connect

## Java vs Bedrock — Quick Guide
| Feature | Java | Bedrock |
|---------|------|---------|
| Platforms | PC only | PC, Console, Mobile |
| Mods | Huge ecosystem | Limited |
| Performance | Heavier | Lighter |
| Price | Separate purchase | Included with console |

## How to Run
```bash
cd code
python3 bedrock_server.py
```

## Manual Setup
1. Download BDS from: https://www.minecraft.net/en-us/download/server/bedrock
2. Unzip to a folder
3. On Linux: `./bedrock_server`
4. On Windows: `bedrock_server.exe`

## Connecting (Bedrock)
- **Same network:** Add server → Your local IP → Port 19132
- **Over internet:** Your public IP + port forwarding on 19132 (UDP)
- **Xbox/Console:** Requires a workaround app like BedrockConnect

## Key Settings (server.properties)
```properties
server-name=My Bedrock Server
max-players=10
gamemode=survival
difficulty=normal
allow-cheats=false
server-port=19132
```

## Important Ports
| Port | Protocol | Purpose |
|------|----------|---------|
| 19132 | UDP | IPv4 connections |
| 19133 | UDP | IPv6 connections |
