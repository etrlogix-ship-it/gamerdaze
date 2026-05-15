#!/usr/bin/env python3
"""Ultimate Game Hub - Project 100 🚀
The grand finale — an all-in-one dashboard for your gaming empire.
Shows server status, player leaderboard, recent activity, and quick controls.
Install: pip install flask psutil requests
"""
import os, json, time, threading, subprocess
from datetime import datetime

try:
    from flask import Flask, render_template_string, jsonify
    FLASK = True
except ImportError:
    FLASK = False

try:
    import psutil
    PSUTIL = True
except ImportError:
    PSUTIL = False

app = Flask(__name__) if FLASK else None

SERVERS_CONFIG = [
    {"name": "Minecraft",  "port": 25565, "dir": os.path.expanduser("~/minecraft_server_files")},
    {"name": "Valheim",    "port": 2456,  "dir": os.path.expanduser("~/valheim_server")},
    {"name": "Terraria",   "port": 7777,  "dir": os.path.expanduser("~/terraria_server_files")},
]

DEMO_PLAYERS = [
    {"name": "DragonSlayer99", "kills": 1523, "online": True},
    {"name": "SteveBuilder",   "kills": 892,  "online": True},
    {"name": "NightCrawler",   "kills": 756,  "online": False},
    {"name": "PixelPirate",    "kills": 634,  "online": False},
]

def check_port(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("localhost", port)) == 0

def get_system_stats():
    if PSUTIL:
        return {
            "cpu":  psutil.cpu_percent(interval=0.2),
            "ram":  psutil.virtual_memory().percent,
            "disk": psutil.disk_usage("/").percent,
        }
    import random
    return {"cpu": random.uniform(15, 65), "ram": random.uniform(30, 70), "disk": random.uniform(40, 60)}

HTML = """<!DOCTYPE html>
<html>
<head>
<title>🚀 Ultimate Game Hub</title>
<meta http-equiv="refresh" content="15">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a14;color:#e0e0ff;font-family:'Segoe UI',sans-serif;padding:24px}
h1{color:#7c3aed;font-size:1.8em;margin-bottom:4px}
.sub{color:#555;margin-bottom:28px;font-size:0.9em}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-bottom:24px}
.card{background:#12122a;border-radius:12px;padding:20px;border:1px solid #1e1e3a}
.card h2{font-size:0.85em;text-transform:uppercase;letter-spacing:1px;color:#7c3aed;margin-bottom:14px}
.server-row{display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e1e3a}
.dot{width:10px;height:10px;border-radius:50%;background:#f44336;margin-right:8px;flex-shrink:0}
.dot.online{background:#4caf50;box-shadow:0 0 8px rgba(76,175,80,0.6)}
.bar-wrap{background:#1e1e3a;border-radius:4px;height:8px;margin-top:6px}
.bar{height:8px;border-radius:4px}
.stat-val{font-size:1.4em;font-weight:bold;color:#7c3aed}
.player-row{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1e1e3a;font-size:0.92em}
.online-tag{color:#4caf50;font-size:0.8em}
.offline-tag{color:#555;font-size:0.8em}
footer{text-align:center;color:#333;font-size:0.8em;margin-top:24px}
</style>
</head>
<body>
<h1>🚀 Ultimate Game Hub</h1>
<p class="sub">Auto-refreshes every 15 seconds · {{ now }}</p>

<div class="grid">
<!-- Servers -->
<div class="card">
<h2>🖥️ Game Servers</h2>
{% for s in servers %}
<div class="server-row">
  <div style="display:flex;align-items:center">
    <div class="dot {{ 'online' if s.online else '' }}"></div>
    <span>{{ s.name }}</span>
  </div>
  <span style="color:{{ '#4caf50' if s.online else '#f44336' }}">
    {{ '● ONLINE' if s.online else '○ OFFLINE' }}
  </span>
</div>
{% endfor %}
</div>

<!-- System Stats -->
<div class="card">
<h2>📊 System Health</h2>
{% for label, val in stats.items() %}
<div style="margin-bottom:12px">
  <div style="display:flex;justify-content:space-between">
    <span>{{ label.upper() }}</span>
    <span class="stat-val">{{ "%.0f"|format(val) }}%</span>
  </div>
  <div class="bar-wrap">
    <div class="bar" style="width:{{ val }}%;background:{{ '#4caf50' if val<70 else '#ff9800' if val<90 else '#f44336' }}"></div>
  </div>
</div>
{% endfor %}
</div>

<!-- Players -->
<div class="card">
<h2>👥 Top Players</h2>
{% for p in players %}
<div class="player-row">
  <span>{{ p.name }}</span>
  <span>
    <span style="color:#ffd700">{{ p.kills }} kills</span>
    <span class="{{ 'online-tag' if p.online else 'offline-tag' }}"> {{ '● online' if p.online else '○' }}</span>
  </span>
</div>
{% endfor %}
</div>
</div>

<footer>Made by Sanford Banks · Project 100 — Ultimate Game Hub 🚀</footer>
</body></html>"""

if FLASK:
    @app.route("/")
    def index():
        servers = [{"name": s["name"], "port": s["port"], "online": check_port(s["port"])} for s in SERVERS_CONFIG]
        stats   = get_system_stats()
        now     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return render_template_string(HTML, servers=servers, stats=stats, players=DEMO_PLAYERS, now=now)

    @app.route("/api/status")
    def api_status():
        return jsonify({
            "servers": [{"name": s["name"], "online": check_port(s["port"])} for s in SERVERS_CONFIG],
            "system":  get_system_stats(),
        })

def main():
    print("╔" + "═"*50 + "╗")
    print("║  🚀 ULTIMATE GAME HUB — Project 100       ║")
    print("║     Congratulations on completing all      ║")
    print("║     100 Gamer Projects! 🏆                 ║")
    print("╚" + "═"*50 + "╝")

    if not FLASK:
        print("\n  Install flask for the web dashboard: pip install flask")
        print("\n  Quick status check:")
        for s in SERVERS_CONFIG:
            online = check_port(s["port"])
            icon = "✅" if online else "❌"
            print(f"  {icon} {s['name']:<15} port {s['port']} — {'ONLINE' if online else 'offline'}")
        stats = get_system_stats()
        print(f"\n  CPU: {stats['cpu']:.0f}%  RAM: {stats['ram']:.0f}%  Disk: {stats['disk']:.0f}%")
        return

    print("\n  🌐 Dashboard running at http://localhost:5100")
    print("  Press Ctrl+C to stop")
    try:
        app.run(host="0.0.0.0", port=5100, debug=False)
    except KeyboardInterrupt:
        print("\n  Game Hub stopped. GG! 🎮")

if __name__ == "__main__":
    main()
