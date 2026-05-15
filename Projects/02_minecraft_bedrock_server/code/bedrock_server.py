#!/usr/bin/env python3
"""
Minecraft Bedrock Server Launcher - Project 02
Downloads and starts a Minecraft Bedrock Dedicated Server.
"""

import os
import sys
import platform
import subprocess
import urllib.request
import zipfile

SERVER_DIR = os.path.join(os.path.dirname(__file__), "..", "bedrock_server_files")

# Download URLs (check minecraft.net for latest)
DOWNLOAD_URLS = {
    "Linux":   "https://minecraft.azureedge.net/bin-linux/bedrock-server-1.21.0.03.zip",
    "Windows": "https://minecraft.azureedge.net/bin-win/bedrock-server-1.21.0.03.zip",
}

DEFAULT_PROPS = """server-name=My Bedrock Server
gamemode=survival
difficulty=normal
allow-cheats=false
max-players=10
online-mode=true
white-list=false
server-port=19132
server-portv6=19133
view-distance=32
tick-distance=4
player-idle-timeout=30
"""

def get_platform():
    system = platform.system()
    if system in DOWNLOAD_URLS:
        return system
    print(f"  ⚠️  {system} not directly supported for Bedrock Server.")
    print("  Use Linux (recommended) or Windows.")
    return None

def setup_server_dir():
    os.makedirs(SERVER_DIR, exist_ok=True)
    props_path = os.path.join(SERVER_DIR, "server.properties")
    if not os.path.exists(props_path):
        with open(props_path, "w") as f:
            f.write(DEFAULT_PROPS)
        print("  ✅ Default server.properties created")

def download_and_extract(system):
    url = DOWNLOAD_URLS[system]
    zip_path = os.path.join(SERVER_DIR, "bedrock_server.zip")
    print(f"  ⬇️  Downloading Bedrock server for {system}...")
    print(f"  URL: {url}")
    print("  (If this URL is outdated, download manually from minecraft.net)\n")

    try:
        def progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            pct = min(100, downloaded / total_size * 100) if total_size > 0 else 0
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            print(f"  [{bar}] {pct:.0f}%  ", end="\r")

        urllib.request.urlretrieve(url, zip_path, reporthook=progress)
        print(f"\n  ✅ Downloaded!")

        print("  📦 Extracting...")
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(SERVER_DIR)
        os.remove(zip_path)
        print("  ✅ Extracted!")
        return True
    except Exception as e:
        print(f"\n  ❌ Download failed: {e}")
        print("  Please download manually from:")
        print("  https://www.minecraft.net/en-us/download/server/bedrock")
        return False

def start_server(system):
    if system == "Linux":
        exe = os.path.join(SERVER_DIR, "bedrock_server")
        if os.path.exists(exe):
            os.chmod(exe, 0o755)
        cmd = ["./bedrock_server"]
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = "."
    else:
        cmd = ["bedrock_server.exe"]
        env = None

    print("\n  🚀 Starting Bedrock server...")
    print("  Players on Bedrock can connect via:")
    print("  • Same network: your local IP, port 19132")
    print("  • Internet: your public IP, port 19132 (UDP forwarded)")
    print("\n  Type 'stop' to shut down safely\n")
    print("  " + "─" * 50)

    try:
        process = subprocess.Popen(
            cmd, cwd=SERVER_DIR,
            stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stdout,
            env=env
        )
        process.wait()
    except KeyboardInterrupt:
        print("\n  ⏹ Server stopped.")
    except FileNotFoundError:
        print(f"\n  ❌ Server executable not found in {SERVER_DIR}")
        print("  Please download the server files manually.")

def main():
    print("=" * 52)
    print("  🪨 Minecraft Bedrock Server Launcher")
    print("=" * 52)

    system = get_platform()
    if not system:
        return

    print(f"  Platform: {system}")
    setup_server_dir()

    # Check if server binary exists
    exe_name = "bedrock_server" if system == "Linux" else "bedrock_server.exe"
    exe_path = os.path.join(SERVER_DIR, exe_name)

    if not os.path.exists(exe_path):
        print(f"\n  No Bedrock server found in {SERVER_DIR}")
        choice = input("  Download now? (y/n): ").strip().lower()
        if choice == "y":
            if not download_and_extract(system):
                return
        else:
            print("  Please manually place Bedrock server files in:")
            print(f"  {SERVER_DIR}")
            return

    print(f"\n  ✅ Server files found")
    print(f"  📋 Edit {SERVER_DIR}/server.properties to change settings\n")
    start_server(system)

if __name__ == "__main__":
    main()
