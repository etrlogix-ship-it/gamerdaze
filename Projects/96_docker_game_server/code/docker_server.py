#!/usr/bin/env python3
"""Dockerised Game Server - Project 96
Run a Minecraft server inside Docker.
Requirements: Docker installed (docker.com/get-started)
"""
import subprocess, os, sys

IMAGE     = "itzg/minecraft-server"
CONTAINER = "minecraft-docker"
PORT      = 25565
DATA_DIR  = os.path.expanduser("~/minecraft-docker-data")

def docker_available():
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def pull_image():
    print(f"  ⬇️  Pulling {IMAGE}...")
    subprocess.run(["docker", "pull", IMAGE], check=True)

def start_server(memory="2G", version="LATEST", gamemode="survival"):
    os.makedirs(DATA_DIR, exist_ok=True)
    cmd = [
        "docker", "run", "-d",
        "--name", CONTAINER,
        "-p", f"{PORT}:{PORT}",
        "-v", f"{DATA_DIR}:/data",
        "-e", "EULA=TRUE",
        "-e", f"MEMORY={memory}",
        "-e", f"VERSION={version}",
        "-e", f"GAMEMODE={gamemode}",
        "-e", "ONLINE_MODE=FALSE",
        "--restart", "unless-stopped",
        IMAGE
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  ✅ Container started: {result.stdout.strip()[:12]}...")
        print(f"  📂 World data: {DATA_DIR}")
        print(f"  🌐 Connect at: localhost:{PORT}")
        print(f"  📊 Logs: docker logs -f {CONTAINER}")
    else:
        print(f"  ❌ Error: {result.stderr}")

def stop_server():
    subprocess.run(["docker", "stop", CONTAINER])
    print(f"  ⏹ Container stopped")

def remove_server():
    subprocess.run(["docker", "rm", CONTAINER])
    print(f"  🗑️  Container removed (data kept in {DATA_DIR})")

def server_status():
    result = subprocess.run(["docker", "ps", "--filter", f"name={CONTAINER}", "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"],
                             capture_output=True, text=True)
    if CONTAINER in result.stdout:
        print(f"\n  ✅ Server is RUNNING")
        print(result.stdout)
    else:
        print(f"\n  🔴 Server is STOPPED")

def show_logs():
    print("  Press Ctrl+C to stop viewing logs\n")
    try:
        subprocess.run(["docker", "logs", "-f", "--tail", "50", CONTAINER])
    except KeyboardInterrupt:
        pass

def main():
    print("=" * 52)
    print("  🐳 Dockerised Minecraft Server")
    print("=" * 52)

    if not docker_available():
        print("\n  ❌ Docker not found!")
        print("  Install Docker from: https://docker.com/get-started")
        print("\n  Why Docker?")
        print("  • Server runs in an isolated container")
        print("  • Easy to update, backup, and move")
        print("  • Doesn\'t mess up your system")
        print("  • One command to start/stop/remove")
        return

    print("  ✅ Docker found!")

    while True:
        print("\n  Options:")
        print("  [1] Start Minecraft server")
        print("  [2] Stop server")
        print("  [3] Remove container (keeps world data)")
        print("  [4] Server status")
        print("  [5] View logs")
        print("  [6] Quit")
        choice = input("\n  Choice: ").strip()

        if choice == "1":
            version  = input("  Minecraft version (LATEST/1.20.4/etc): ").strip() or "LATEST"
            memory   = input("  Memory (1G/2G/4G, default 2G): ").strip() or "2G"
            gamemode = input("  Gamemode (survival/creative, default survival): ").strip() or "survival"
            pull_image()
            start_server(memory, version, gamemode)
        elif choice == "2": stop_server()
        elif choice == "3": remove_server()
        elif choice == "4": server_status()
        elif choice == "5": show_logs()
        elif choice == "6": break

if __name__ == "__main__":
    main()
