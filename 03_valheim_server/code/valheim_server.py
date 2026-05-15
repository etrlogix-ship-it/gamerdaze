#!/usr/bin/env python3
"""Valheim Server Launcher - Project 03"""

import os, subprocess, sys

INSTALL_DIR = os.path.expanduser("~/valheim_server")
WORLDS_DIR  = os.path.expanduser("~/.config/unity3d/IronGate/Valheim/worlds")

def install_via_steamcmd():
    print("  📥 Installing Valheim Dedicated Server via SteamCMD...")
    os.makedirs(INSTALL_DIR, exist_ok=True)
    cmd = [
        "steamcmd",
        "+force_install_dir", INSTALL_DIR,
        "+login", "anonymous",
        "+app_update", "896660", "validate",
        "+quit"
    ]
    try:
        subprocess.run(cmd, check=True)
        print("  ✅ Valheim server installed!")
        return True
    except FileNotFoundError:
        print("  ❌ SteamCMD not found.")
        print("  Install: sudo apt install steamcmd")
        print("  Or download: https://developer.valvesoftware.com/wiki/SteamCMD")
        return False
    except subprocess.CalledProcessError as e:
        print(f"  ❌ SteamCMD error: {e}")
        return False

def start_server(name, world, password, port=2456, public=True):
    exe = os.path.join(INSTALL_DIR, "valheim_server.x86_64")
    if not os.path.exists(exe):
        print(f"  ❌ Server not found at {exe}")
        return

    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = os.path.join(INSTALL_DIR, "linux64")
    env["SteamAppId"] = "892970"

    cmd = [
        exe,
        "-nographics", "-batchmode",
        "-name", name,
        "-port", str(port),
        "-world", world,
        "-password", password,
        "-public", "1" if public else "0"
    ]

    print(f"\n  🚀 Starting Valheim server: {name}")
    print(f"  World: {world} | Port: {port}-{port+2} UDP")
    print(f"  Public listing: {'Yes' if public else 'No'}")
    print("  Press Ctrl+C to stop\n")
    try:
        process = subprocess.Popen(cmd, env=env, cwd=INSTALL_DIR)
        process.wait()
    except KeyboardInterrupt:
        print("\n  ⏹ Server stopped.")

def main():
    print("=" * 48)
    print("  🪓 Valheim Server Launcher")
    print("=" * 48)

    exe = os.path.join(INSTALL_DIR, "valheim_server.x86_64")
    if not os.path.exists(exe):
        print(f"\n  Server not found at {INSTALL_DIR}")
        choice = input("  Install via SteamCMD? (y/n): ").strip().lower()
        if choice == "y":
            if not install_via_steamcmd():
                return
        else:
            return

    print("\n  Server Configuration:")
    name     = input("  Server name (default: My Viking Server): ").strip() or "My Viking Server"
    world    = input("  World name (default: MyWorld): ").strip() or "MyWorld"
    password = input("  Password (min 5 chars): ").strip()
    while len(password) < 5:
        print("  Password must be at least 5 characters!")
        password = input("  Password: ").strip()
    port_str = input("  Port (default 2456): ").strip()
    port     = int(port_str) if port_str.isdigit() else 2456
    public   = input("  List publicly? (y/n, default y): ").strip().lower() != "n"

    start_server(name, world, password, port, public)

if __name__ == "__main__":
    main()
