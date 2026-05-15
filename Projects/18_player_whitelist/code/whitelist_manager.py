#!/usr/bin/env python3
"""
Player Whitelist Manager - Project 18
Manage your Minecraft server whitelist without editing JSON manually.
Works with any JSON-format whitelist file.
"""

import os
import json
import datetime

WHITELIST_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "01_minecraft_java_server", "server_files", "whitelist.json"
)

# If the above path doesn't exist, use a local demo file
if not os.path.exists(os.path.dirname(WHITELIST_FILE)):
    WHITELIST_FILE = "whitelist_demo.json"

def load_whitelist():
    if not os.path.exists(WHITELIST_FILE):
        return []
    try:
        with open(WHITELIST_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_whitelist(players):
    with open(WHITELIST_FILE, "w") as f:
        json.dump(players, f, indent=2)

def list_players(players):
    if not players:
        print("\n  📋 Whitelist is empty.")
        return
    print(f"\n  📋 Whitelist ({len(players)} players):")
    print("  " + "─" * 40)
    for i, p in enumerate(sorted(players, key=lambda x: x.get("name","").lower()), 1):
        uuid = p.get("uuid", "no-uuid")
        name = p.get("name", "unknown")
        added = p.get("added", "unknown")
        print(f"  {i:>3}. {name:<20} {uuid[:8]}...  {added}")

def add_player(players, name, uuid=None):
    # Check not already in list
    for p in players:
        if p.get("name", "").lower() == name.lower():
            print(f"  ⚠️  {name} is already whitelisted.")
            return players

    if not uuid:
        uuid = f"demo-uuid-{name.lower()}-0000-0000-000000000000"
        print(f"  ℹ️  No UUID provided — using placeholder: {uuid}")
        print("  (For a real server, get the UUID from mcuuid.net)")

    players.append({
        "uuid":  uuid,
        "name":  name,
        "added": datetime.date.today().isoformat()
    })
    print(f"  ✅ Added {name} to whitelist")
    return players

def remove_player(players, name):
    before = len(players)
    players = [p for p in players if p.get("name", "").lower() != name.lower()]
    if len(players) < before:
        print(f"  ✅ Removed {name} from whitelist")
    else:
        print(f"  ❌ {name} not found in whitelist")
    return players

def search_players(players, query):
    results = [p for p in players if query.lower() in p.get("name","").lower()]
    if results:
        print(f"\n  🔍 Found {len(results)} result(s) for '{query}':")
        for p in results:
            print(f"  • {p['name']} ({p.get('uuid','?')[:8]}...)")
    else:
        print(f"  No players matching '{query}'")

def main():
    print("=" * 48)
    print("  📋 Player Whitelist Manager")
    print("=" * 48)
    print(f"\n  Whitelist file: {os.path.abspath(WHITELIST_FILE)}")

    players = load_whitelist()
    print(f"  Loaded {len(players)} player(s)\n")

    while True:
        print("  Options:")
        print("  [1] List all players")
        print("  [2] Add player")
        print("  [3] Remove player")
        print("  [4] Search")
        print("  [5] Export to text file")
        print("  [6] Quit")
        choice = input("\n  Choice: ").strip()

        if choice == "1":
            list_players(players)

        elif choice == "2":
            name = input("\n  Player name: ").strip()
            if not name:
                continue
            uuid = input("  UUID (optional, press Enter to skip): ").strip() or None
            players = add_player(players, name, uuid)
            save_whitelist(players)

        elif choice == "3":
            name = input("\n  Player name to remove: ").strip()
            if not name:
                continue
            confirm = input(f"  Remove {name}? (y/n): ").strip().lower()
            if confirm == "y":
                players = remove_player(players, name)
                save_whitelist(players)

        elif choice == "4":
            query = input("\n  Search term: ").strip()
            if query:
                search_players(players, query)

        elif choice == "5":
            fname = "whitelist_export.txt"
            with open(fname, "w") as f:
                f.write(f"Whitelist Export — {datetime.date.today()}\n")
                f.write("=" * 40 + "\n")
                for p in sorted(players, key=lambda x: x.get("name","").lower()):
                    f.write(f"{p.get('name','?')}\n")
            print(f"  ✅ Exported to {fname}")

        elif choice == "6":
            break

        print()

    print("  Whitelist manager closed. ✅")

if __name__ == "__main__":
    main()
