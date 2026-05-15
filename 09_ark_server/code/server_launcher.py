#!/usr/bin/env python3
"""
ARK Survival Server Launcher - Project 09
Helps you set up and run a ARK Survival dedicated server.
"""

import os, sys, subprocess, platform

GAME         = "ARK Survival"
STEAM_APPID  = "376030"
DEFAULT_PORT = 7777
SERVER_DIR   = os.path.expanduser("~/09_ark_server_files")

def check_steamcmd():
    try:
        subprocess.run(["steamcmd", "+quit"], capture_output=True, timeout=10)
        return True
    except FileNotFoundError:
        return False

def install_server():
    if not check_steamcmd():
        print("  SteamCMD not found. Install: sudo apt install steamcmd")
        return False
    os.makedirs(SERVER_DIR, exist_ok=True)
    print(f"  Installing ARK Survival server via SteamCMD...")
    cmd = ["steamcmd", "+force_install_dir", SERVER_DIR,
           "+login", "anonymous", "+app_update", STEAM_APPID, "validate", "+quit"]
    result = subprocess.run(cmd)
    return result.returncode == 0

def main():
    print("=" * 48)
    print(f"  ARK Survival Server Launcher")
    print("=" * 48)
    print(f"  Install dir : {SERVER_DIR}")
    print(f"  Default port: {DEFAULT_PORT}")
    print(f"  Steam App ID: {STEAM_APPID}")

    if not os.path.exists(SERVER_DIR) or not os.listdir(SERVER_DIR):
        choice = input("\n  Install server? (y/n): ").strip().lower()
        if choice == "y":
            install_server()
    else:
        print(f"\n  Server files found at {SERVER_DIR}")
        print("  See README.md for the exact start command.")

if __name__ == "__main__":
    main()
