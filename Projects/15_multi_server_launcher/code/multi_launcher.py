#!/usr/bin/env python3
"""
Multi-Server Launcher - Project 15
Launch, monitor, and stop multiple game servers from one menu.
"""

import os
import subprocess
import time
import sys

# ── Configure your servers here ──────────────────────────────────
SERVERS = [
    {
        "name":    "Minecraft Java",
        "dir":     os.path.expanduser("~/minecraft_server_files"),
        "command": ["java", "-Xmx2G", "-Xms1G", "-jar", "server.jar", "nogui"],
        "port":    25565,
    },
    {
        "name":    "Valheim",
        "dir":     os.path.expanduser("~/valheim_server"),
        "command": ["./valheim_server.x86_64", "-nographics", "-batchmode",
                    "-name", "My Server", "-port", "2456",
                    "-world", "MyWorld", "-password", "secret"],
        "port":    2456,
    },
    {
        "name":    "Terraria (TShock)",
        "dir":     os.path.expanduser("~/terraria_server_files"),
        "command": ["mono", "TShock.Server.exe", "-port", "7777"],
        "port":    7777,
    },
    # Add more servers here!
]
# ─────────────────────────────────────────────────────────────────

running_processes = {}  # name -> (process, start_time)

def get_status(name):
    if name in running_processes:
        proc, start = running_processes[name]
        if proc.poll() is None:
            uptime = int(time.time() - start)
            h, m, s = uptime // 3600, (uptime % 3600) // 60, uptime % 60
            return f"🟢 RUNNING  uptime: {h:02d}:{m:02d}:{s:02d}"
        else:
            del running_processes[name]
    return "🔴 STOPPED"

def print_menu():
    os.system("clear" if os.name == "posix" else "cls")
    print("╔" + "═" * 54 + "╗")
    print("║  🚀 Multi-Server Launcher                          ║")
    print("╠" + "═" * 54 + "╣")
    print(f"  {'#':<4} {'Server':<22} {'Port':<8} Status")
    print("  " + "─" * 52)
    for i, server in enumerate(SERVERS, 1):
        status = get_status(server["name"])
        print(f"  [{i}]  {server['name']:<22} {server['port']:<8} {status}")
    print()
    print("  [S] Stop a server   [A] Stop all   [Q] Quit")
    print("╚" + "═" * 54 + "╝")

def start_server(server):
    name = server["name"]
    if name in running_processes and running_processes[name][0].poll() is None:
        print(f"\n  ⚠️  {name} is already running!")
        input("  Press Enter to continue...")
        return

    work_dir = server["dir"]
    if not os.path.exists(work_dir):
        print(f"\n  ❌ Directory not found: {work_dir}")
        print("  Make sure the server is installed first.")
        input("  Press Enter to continue...")
        return

    print(f"\n  🚀 Starting {name}...")
    try:
        log_file = open(f"{name.replace(' ','_').lower()}_server.log", "a")
        proc = subprocess.Popen(
            server["command"],
            cwd=work_dir,
            stdout=log_file,
            stderr=log_file,
            stdin=subprocess.DEVNULL
        )
        running_processes[name] = (proc, time.time())
        print(f"  ✅ {name} started! (PID {proc.pid})")
        print(f"  📝 Logs: {name.replace(' ','_').lower()}_server.log")
        time.sleep(1)
    except FileNotFoundError as e:
        print(f"  ❌ Could not start: {e}")
        print("  Is the server installed? Check README for this game.")
        input("  Press Enter to continue...")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        input("  Press Enter to continue...")

def stop_server(name):
    if name in running_processes:
        proc, _ = running_processes[name]
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
            del running_processes[name]
            print(f"  ✅ {name} stopped.")
        else:
            del running_processes[name]
    else:
        print(f"  {name} is not running.")

def stop_all():
    print("\n  Stopping all servers...")
    for name in list(running_processes.keys()):
        stop_server(name)
    print("  All servers stopped.")
    time.sleep(1)

def main():
    print("\n  🎮 Multi-Server Launcher starting...")
    print("  Servers will run in background. Check log files for output.\n")
    time.sleep(1)

    try:
        while True:
            print_menu()
            choice = input("\n  Choice: ").strip().lower()

            if choice == "q":
                if running_processes:
                    confirm = input("\n  Servers still running! Stop all and quit? (y/n): ").strip().lower()
                    if confirm == "y":
                        stop_all()
                break

            elif choice == "a":
                stop_all()

            elif choice == "s":
                names = [s["name"] for s in SERVERS]
                print("\n  Running servers:")
                running = [n for n in names if n in running_processes
                           and running_processes[n][0].poll() is None]
                if not running:
                    print("  No servers running.")
                else:
                    for i, n in enumerate(running, 1):
                        print(f"  [{i}] {n}")
                    pick = input("  Which to stop? (number): ").strip()
                    if pick.isdigit() and 1 <= int(pick) <= len(running):
                        stop_server(running[int(pick)-1])
                        time.sleep(0.5)

            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(SERVERS):
                    start_server(SERVERS[idx])
                else:
                    print("  Invalid number.")
                    time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n\n  Shutting down...")
        stop_all()

    print("\n  👋 Multi-launcher closed.")

if __name__ == "__main__":
    main()
