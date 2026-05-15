#!/usr/bin/env python3
"""
Server Performance Monitor - Project 16
Real-time dashboard showing CPU, RAM, disk, and network stats.
Install: pip install psutil
"""

import time
import os
import sys

try:
    import psutil
    PSUTIL = True
except ImportError:
    PSUTIL = False
    print("psutil not found. Install with: pip install psutil")
    print("Running in demo mode with random values.\n")
    import random

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def bar(value, width=30, fill="█", empty="░"):
    filled = int(value / 100 * width)
    return fill * filled + empty * (max(0, width - filled))

def colour(value, warn=70, crit=90):
    if value >= crit:  return "\033[91m"  # red
    if value >= warn:  return "\033[93m"  # yellow
    return "\033[92m"                      # green

RESET = "\033[0m"

def get_stats():
    if PSUTIL:
        cpu    = psutil.cpu_percent(interval=0.5)
        mem    = psutil.virtual_memory()
        disk   = psutil.disk_usage("/")
        net    = psutil.net_io_counters()
        temps  = {}
        try:
            t = psutil.sensors_temperatures()
            if t:
                for name, entries in t.items():
                    if entries:
                        temps[name] = entries[0].current
        except AttributeError:
            pass
        return {
            "cpu":        cpu,
            "ram_pct":    mem.percent,
            "ram_used":   mem.used  // (1024**3),
            "ram_total":  mem.total // (1024**3),
            "disk_pct":   disk.percent,
            "disk_used":  disk.used  // (1024**3),
            "disk_total": disk.total // (1024**3),
            "net_sent":   net.bytes_sent  // (1024**2),
            "net_recv":   net.bytes_recv  // (1024**2),
            "temps":      temps,
        }
    else:
        # Demo mode
        return {
            "cpu":        random.uniform(10, 80),
            "ram_pct":    random.uniform(30, 75),
            "ram_used":   random.randint(2, 6),
            "ram_total":  8,
            "disk_pct":   random.uniform(40, 70),
            "disk_used":  random.randint(100, 300),
            "disk_total": 500,
            "net_sent":   random.randint(500, 5000),
            "net_recv":   random.randint(1000, 10000),
            "temps":      {},
        }

def get_top_processes(n=5):
    if not PSUTIL:
        return [("java (Minecraft)", 45.2, 2048), ("python3", 2.1, 128),
                ("nginx", 0.8, 64), ("sshd", 0.1, 16), ("bash", 0.0, 8)]
    procs = []
    for p in psutil.process_iter(["name", "cpu_percent", "memory_info"]):
        try:
            procs.append((p.info["name"], p.info["cpu_percent"],
                          p.info["memory_info"].rss // (1024**2)))
        except:
            pass
    return sorted(procs, key=lambda x: x[1], reverse=True)[:n]

def draw_dashboard(stats, procs, tick):
    clear()
    width = 60
    spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"[tick % 10]

    print("╔" + "═" * width + "╗")
    print(f"║  📊 Server Monitor  {spinner}  {'LIVE' if PSUTIL else 'DEMO MODE':<34}║")
    print(f"║  {time.strftime('%Y-%m-%d  %H:%M:%S'):<{width-2}}║")
    print("╠" + "═" * width + "╣")

    # CPU
    c = colour(stats["cpu"])
    print(f"║  CPU    [{c}{bar(stats['cpu'], 28)}{RESET}] {stats['cpu']:5.1f}%     ║")

    # RAM
    c = colour(stats["ram_pct"])
    print(f"║  RAM    [{c}{bar(stats['ram_pct'], 28)}{RESET}] {stats['ram_pct']:5.1f}%     ║")
    print(f"║         {stats['ram_used']}GB used of {stats['ram_total']}GB{' ' * 38}║"[:width+3])

    # Disk
    c = colour(stats["disk_pct"])
    print(f"║  Disk   [{c}{bar(stats['disk_pct'], 28)}{RESET}] {stats['disk_pct']:5.1f}%     ║")
    print(f"║         {stats['disk_used']}GB used of {stats['disk_total']}GB{' ' * 38}║"[:width+3])

    # Network
    print(f"║  Net ↑  {stats['net_sent']:>6} MB sent   ↓  {stats['net_recv']:>6} MB recv   ║")

    # Temps
    if stats["temps"]:
        temp_str = "  ".join(f"{k}: {v:.0f}°C" for k, v in list(stats["temps"].items())[:3])
        print(f"║  Temp   {temp_str:<{width-9}}║")

    # Top processes
    print("╠" + "═" * width + "╣")
    print(f"║  {'Process':<28} {'CPU%':>6}  {'RAM MB':>7}          ║")
    print("║  " + "─" * (width-2) + "║")
    for name, cpu_p, mem_mb in procs:
        c = colour(cpu_p, 30, 60)
        print(f"║  {name[:28]:<28} {c}{cpu_p:>5.1f}%{RESET}  {mem_mb:>7}          ║"[:width+6])

    print("╚" + "═" * width + "╝")
    print("  Press Ctrl+C to exit")

def main():
    print("📊 Starting Server Monitor... (Ctrl+C to stop)")
    time.sleep(0.5)

    interval = 2  # seconds between updates
    tick = 0
    try:
        while True:
            stats = get_stats()
            procs = get_top_processes()
            draw_dashboard(stats, procs, tick)
            tick += 1
            time.sleep(interval)
    except KeyboardInterrupt:
        clear()
        print("  📊 Monitor stopped. Server is on its own now!")

if __name__ == "__main__":
    main()
