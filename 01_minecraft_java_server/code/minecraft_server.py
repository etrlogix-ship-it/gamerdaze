#!/usr/bin/env python3
"""
Minecraft Java Server Launcher - Project 01
Downloads and starts a Minecraft Java server automatically.
"""

import os
import sys
import subprocess
import urllib.request
import json
import platform

SERVER_DIR = os.path.join(os.path.dirname(__file__), "..", "server_files")
EULA_FILE  = os.path.join(SERVER_DIR, "eula.txt")
JAR_FILE   = os.path.join(SERVER_DIR, "server.jar")
PROPS_FILE = os.path.join(SERVER_DIR, "server.properties")

DEFAULT_PROPS = """#Minecraft server properties
max-players=10
difficulty=normal
gamemode=survival
white-list=false
enable-command-block=true
motd=My Awesome Minecraft Server
pvp=true
spawn-protection=16
view-distance=10
simulation-distance=10
"""

def check_java():
    """Check Java is installed and get version."""
    try:
        result = subprocess.run(["java", "-version"],
                                capture_output=True, text=True)
        version_line = result.stderr.split("\n")[0]
        print(f"  ✅ Java found: {version_line}")
        return True
    except FileNotFoundError:
        print("  ❌ Java not found!")
        print("  Install from: https://adoptium.net")
        if platform.system() == "Darwin":
            print("  Or run: brew install openjdk@17")
        elif platform.system() == "Linux":
            print("  Or run: sudo apt install openjdk-17-jdk")
        return False

def get_latest_version_url():
    """Fetch the latest Minecraft server jar URL from Mojang's API."""
    print("  🌐 Fetching latest Minecraft version info...")
    try:
        manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
        with urllib.request.urlopen(manifest_url, timeout=10) as r:
            manifest = json.loads(r.read())
        latest = manifest["latest"]["release"]
        print(f"  📦 Latest release: {latest}")
        # Find that version's metadata URL
        for v in manifest["versions"]:
            if v["id"] == latest:
                with urllib.request.urlopen(v["url"], timeout=10) as r:
                    version_data = json.loads(r.read())
                return version_data["downloads"]["server"]["url"], latest
    except Exception as e:
        print(f"  ⚠️  Could not fetch version info: {e}")
        return None, None

def download_server():
    """Download the Minecraft server jar."""
    url, version = get_latest_version_url()
    if not url:
        print("  ❌ Could not get download URL.")
        print("  Please download manually from: https://www.minecraft.net/en-us/download/server")
        print(f"  Save as: {JAR_FILE}")
        return False

    print(f"  ⬇️  Downloading Minecraft {version} server...")
    try:
        def progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            pct = min(100, downloaded / total_size * 100) if total_size > 0 else 0
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            print(f"  [{bar}] {pct:.0f}%  ", end="\r")

        urllib.request.urlretrieve(url, JAR_FILE, reporthook=progress)
        print(f"\n  ✅ Downloaded server.jar ({os.path.getsize(JAR_FILE) // (1024*1024)}MB)")
        return True
    except Exception as e:
        print(f"\n  ❌ Download failed: {e}")
        return False

def accept_eula():
    """Write eula.txt with eula=true."""
    with open(EULA_FILE, "w") as f:
        f.write("# By setting eula=true you agree to the Minecraft EULA\n")
        f.write("# https://aka.ms/MinecraftEULA\n")
        f.write("eula=true\n")
    print("  ✅ EULA accepted")

def write_default_props():
    """Write default server.properties if it doesn't exist."""
    if not os.path.exists(PROPS_FILE):
        with open(PROPS_FILE, "w") as f:
            f.write(DEFAULT_PROPS)
        print("  ✅ Default server.properties created")

def get_ram():
    """Ask how much RAM to allocate."""
    print("\n  💾 How much RAM to allocate to the server?")
    print("  Recommended: 2G for 1-5 players, 4G for 6-10 players")
    print("  Options: 1G, 2G, 4G, 6G, 8G")
    ram = input("  RAM (default 2G): ").strip().upper()
    if ram not in ("1G", "2G", "4G", "6G", "8G"):
        ram = "2G"
    return ram

def start_server(ram="2G"):
    """Start the Minecraft server."""
    print(f"\n  🚀 Starting Minecraft server with {ram} RAM...")
    print("  Type 'stop' in the server console to shut down safely\n")
    print("  " + "─" * 50)

    cmd = ["java", f"-Xmx{ram}", f"-Xms{ram}", "-jar", "server.jar", "nogui"]
    try:
        process = subprocess.Popen(
            cmd,
            cwd=SERVER_DIR,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stdout
        )
        process.wait()
    except KeyboardInterrupt:
        print("\n  ⏹ Server stopped.")
    except Exception as e:
        print(f"\n  ❌ Could not start server: {e}")

def main():
    print("=" * 52)
    print("  ⛏️  Minecraft Java Server Launcher")
    print("=" * 52)

    # Check Java
    if not check_java():
        return

    # Create server directory
    os.makedirs(SERVER_DIR, exist_ok=True)

    # Download jar if needed
    if not os.path.exists(JAR_FILE):
        print(f"\n  No server.jar found in {SERVER_DIR}")
        choice = input("  Download latest Minecraft server? (y/n): ").strip().lower()
        if choice == "y":
            if not download_server():
                return
        else:
            print("  Please place server.jar manually and run again.")
            return

    # Accept EULA
    if not os.path.exists(EULA_FILE) or "eula=true" not in open(EULA_FILE).read():
        print("\n  📜 Minecraft EULA")
        print("  You must agree to Mojang's EULA to run a server.")
        print("  Read it at: https://aka.ms/MinecraftEULA")
        agree = input("  Do you agree to the EULA? (yes/no): ").strip().lower()
        if agree != "yes":
            print("  ❌ Cannot start server without agreeing to EULA.")
            return
        accept_eula()

    # Write default properties
    write_default_props()

    # Show current settings
    print(f"\n  📋 Server location: {SERVER_DIR}")
    print("  📋 To change settings, edit server_files/server.properties")

    # Get RAM and start
    ram = get_ram()
    start_server(ram)

if __name__ == "__main__":
    main()
