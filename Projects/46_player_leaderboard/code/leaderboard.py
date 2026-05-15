#!/usr/bin/env python3
"""Player Leaderboard - Project 46
Web-based leaderboard showing top players.
Install: pip install flask
"""
import os, json, time
from datetime import datetime

try:
    from flask import Flask, render_template_string, request, redirect, jsonify
    FLASK = True
except ImportError:
    FLASK = False

DATA_FILE = "leaderboard_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    # Demo data
    return {
        "players": [
            {"name": "DragonSlayer99", "kills": 1523, "deaths": 234, "playtime": 4820, "rank": "Legend"},
            {"name": "SteveBuilder",   "kills": 892,  "deaths": 445, "playtime": 7230, "rank": "Expert"},
            {"name": "NightCrawler",   "kills": 756,  "deaths": 189, "playtime": 2100, "rank": "Veteran"},
            {"name": "PixelPirate",    "kills": 634,  "deaths": 312, "playtime": 3400, "rank": "Veteran"},
            {"name": "CraftMaster",    "kills": 421,  "deaths": 567, "playtime": 8900, "rank": "Builder"},
            {"name": "TNT_Wizard",     "kills": 389,  "deaths": 892, "playtime": 1200, "rank": "Rookie"},
            {"name": "IronGolem42",    "kills": 298,  "deaths": 156, "playtime": 2800, "rank": "Expert"},
            {"name": "EndPortalHero",  "kills": 187,  "deaths": 234, "playtime": 5600, "rank": "Veteran"},
        ],
        "last_updated": datetime.now().isoformat()
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

HTML = """<!DOCTYPE html>
<html>
<head>
<title>🏆 Player Leaderboard</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f0f1a;color:#e0e0ff;font-family:'Segoe UI',sans-serif;padding:20px}
h1{text-align:center;color:#ffd700;font-size:2em;margin-bottom:5px;text-shadow:0 0 20px rgba(255,215,0,0.5)}
.subtitle{text-align:center;color:#888;margin-bottom:30px}
.table-wrap{max-width:900px;margin:0 auto;overflow-x:auto}
table{width:100%;border-collapse:collapse}
th{background:#1a1a2e;color:#ffd700;padding:12px 16px;text-align:left;font-size:0.85em;text-transform:uppercase;letter-spacing:1px}
td{padding:12px 16px;border-bottom:1px solid #1a1a2e}
tr:hover td{background:rgba(255,215,0,0.05)}
tr:nth-child(1) td{color:#ffd700;font-weight:bold}
tr:nth-child(2) td{color:#c0c0c0}
tr:nth-child(3) td{color:#cd7f32}
.rank-badge{padding:3px 8px;border-radius:12px;font-size:0.8em;background:#1a1a2e}
.medal{font-size:1.3em}
.kd{color:{% if player.kills/max(player.deaths,1) > 2 %}#4caf50{% elif player.kills/max(player.deaths,1) > 1 %}#ff9800{% else %}#f44336{% endif %}}
.updated{text-align:center;color:#555;font-size:0.8em;margin-top:20px}
</style>
</head>
<body>
<h1>🏆 Player Leaderboard</h1>
<p class="subtitle">Updated {{ data.last_updated[:10] }}</p>
<div class="table-wrap">
<table>
<tr>
  <th>#</th><th>Player</th><th>Rank</th><th>Kills</th>
  <th>Deaths</th><th>K/D</th><th>Playtime (hrs)</th>
</tr>
{% for p in players %}
<tr>
  <td>
    {% if loop.index == 1 %}<span class="medal">🥇</span>
    {% elif loop.index == 2 %}<span class="medal">🥈</span>
    {% elif loop.index == 3 %}<span class="medal">🥉</span>
    {% else %}{{ loop.index }}{% endif %}
  </td>
  <td><strong>{{ p.name }}</strong></td>
  <td><span class="rank-badge">{{ p.rank }}</span></td>
  <td>{{ p.kills }}</td>
  <td>{{ p.deaths }}</td>
  <td>{{ "%.2f"|format(p.kills / [p.deaths,1]|max) }}</td>
  <td>{{ (p.playtime // 60) }}h {{ p.playtime % 60 }}m</td>
</tr>
{% endfor %}
</table>
</div>
<p class="updated">Auto-refreshes every 30s</p>
<script>setTimeout(()=>location.reload(), 30000)</script>
</body></html>"""

if FLASK:
    app = Flask(__name__)

    @app.route("/")
    def index():
        data = load_data()
        players = sorted(data["players"], key=lambda x: x["kills"], reverse=True)
        return render_template_string(HTML, data=data, players=players)

    @app.route("/api/players")
    def api_players():
        return jsonify(load_data())

    @app.route("/add", methods=["POST"])
    def add_player():
        data = load_data()
        player = request.json
        data["players"].append(player)
        data["last_updated"] = datetime.now().isoformat()
        save_data(data)
        return jsonify({"ok": True})

    if __name__ == "__main__":
        print("🏆 Player Leaderboard running at http://localhost:5001")
        app.run(port=5001, debug=False)
else:
    # Terminal fallback
    data = load_data()
    players = sorted(data["players"], key=lambda x: x["kills"], reverse=True)
    print("\n🏆 Player Leaderboard\n")
    print(f"  {'#':<4} {'Name':<20} {'Kills':>6} {'Deaths':>7} {'K/D':>6} {'Hrs':>5}")
    print("  " + "-"*52)
    for i, p in enumerate(players, 1):
        kd = p["kills"] / max(p["deaths"], 1)
        hrs = p["playtime"] // 60
        print(f"  {i:<4} {p['name']:<20} {p['kills']:>6} {p['deaths']:>7} {kd:>6.2f} {hrs:>5}")
    print("\nInstall flask for web version: pip install flask")
