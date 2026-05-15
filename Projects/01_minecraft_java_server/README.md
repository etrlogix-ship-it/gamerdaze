# 01 ⛏️ Minecraft Java Server

**Category:** 🖥️ Game Servers
**Difficulty:** ⭐ Beginner
**Time:** 20 minutes

## What You'll Make
Set up your own Minecraft Java Edition server so you and your friends can play together on your own world. No monthly fees, full control, your rules!

## What You'll Learn
- How game servers work
- Running Java applications from the command line
- Basic server configuration

## What You'll Need
- A PC, Mac, or Linux machine with at least 4GB RAM
- Java 17 or higher installed
- Minecraft Java Edition (players connecting need this)

## Install Java
```bash
# Windows — download from adoptium.net
# Mac
brew install openjdk@17
# Linux
sudo apt install openjdk-17-jdk
```

## How to Run
```bash
cd code
python3 minecraft_server.py
```
The script downloads the latest server jar, accepts the EULA, and starts the server automatically.

## Manual Setup (if you prefer)
```bash
# Download server jar from minecraft.net/en-us/download/server
java -Xmx2G -Xms1G -jar server.jar nogui
# Edit eula.txt: change eula=false to eula=true
java -Xmx2G -Xms1G -jar server.jar nogui
```

## Connecting
1. Start the server
2. Open Minecraft Java Edition
3. Multiplayer → Add Server
4. Server Address: `localhost` (for you) or your local IP for friends on same network

## Key Config Files
| File | What it does |
|------|-------------|
| `server.properties` | Game settings, difficulty, max players |
| `ops.json` | Who has operator (admin) privileges |
| `whitelist.json` | Who is allowed to join |
| `banned-players.json` | Who is banned |

## Useful Server Commands
```
/op username       — give someone operator powers
/whitelist add username  — add to whitelist
/ban username      — ban a player
/time set day      — set time to day
/weather clear     — clear weather
stop               — safely shut down server
```

## Recommended server.properties settings
```properties
max-players=10
difficulty=normal
gamemode=survival
white-list=true
enable-command-block=true
```

## Try Changing It!
- Adjust memory allocation (-Xmx flag) based on your RAM
- Install Paper or Spigot instead of vanilla for better performance
- Add plugins (see project 26!)
