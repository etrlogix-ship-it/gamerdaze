#!/usr/bin/env python3
"""
Auto Backup System - Project 17
Automatically backs up game server world files on a schedule.
Keeps the last N backups and deletes older ones.
"""

import os
import shutil
import time
import zipfile
import datetime
import threading
import json

CONFIG_FILE = "backup_config.json"

DEFAULT_CONFIG = {
    "source_dirs": [
        os.path.expanduser("~/minecraft_server_files/world"),
        os.path.expanduser("~/.config/unity3d/IronGate/Valheim/worlds"),
    ],
    "backup_dir":    os.path.expanduser("~/game_backups"),
    "max_backups":   10,
    "interval_mins": 60,
    "compress":      True,
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

def timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def human_size(path):
    total = 0
    if os.path.isfile(path):
        return os.path.getsize(path)
    for dirpath, _, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(dirpath, f))
            except:
                pass
    return total

def format_size(b):
    for unit in ["B", "KB", "MB", "GB"]:
        if b < 1024:
            return f"{b:.1f}{unit}"
        b /= 1024
    return f"{b:.1f}TB"

def backup_directory(source, backup_dir, compress=True):
    if not os.path.exists(source):
        print(f"  ⚠️  Source not found: {source}")
        return None

    os.makedirs(backup_dir, exist_ok=True)
    source_name = os.path.basename(source.rstrip("/"))
    ts = timestamp()

    if compress:
        dest = os.path.join(backup_dir, f"{source_name}_{ts}.zip")
        print(f"  📦 Compressing {source_name}...", end="", flush=True)
        with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
            if os.path.isfile(source):
                zf.write(source, os.path.basename(source))
            else:
                for root, _, files in os.walk(source):
                    for file in files:
                        filepath = os.path.join(root, file)
                        arcname  = os.path.relpath(filepath, os.path.dirname(source))
                        zf.write(filepath, arcname)
        size = format_size(os.path.getsize(dest))
        print(f" ✅ {size}")
    else:
        dest = os.path.join(backup_dir, f"{source_name}_{ts}")
        print(f"  📁 Copying {source_name}...", end="", flush=True)
        if os.path.isfile(source):
            shutil.copy2(source, dest)
        else:
            shutil.copytree(source, dest)
        size = format_size(human_size(dest))
        print(f" ✅ {size}")

    return dest

def rotate_backups(backup_dir, source_name, max_backups):
    """Delete oldest backups if over the limit."""
    pattern = source_name + "_"
    backups = sorted([
        f for f in os.listdir(backup_dir)
        if f.startswith(pattern)
    ])
    while len(backups) > max_backups:
        oldest = os.path.join(backup_dir, backups.pop(0))
        if os.path.isfile(oldest):
            os.remove(oldest)
        else:
            shutil.rmtree(oldest)
        print(f"  🗑️  Removed old backup: {os.path.basename(oldest)}")

def run_backup(cfg):
    print(f"\n  💾 Backup started at {datetime.datetime.now().strftime('%H:%M:%S')}")
    backed_up = 0
    for source in cfg["source_dirs"]:
        if os.path.exists(source):
            result = backup_directory(source, cfg["backup_dir"], cfg["compress"])
            if result:
                source_name = os.path.basename(source.rstrip("/"))
                rotate_backups(cfg["backup_dir"], source_name, cfg["max_backups"])
                backed_up += 1
        else:
            print(f"  ⏭️  Skipping (not found): {source}")
    print(f"  ✅ Backup complete — {backed_up} location(s) backed up")
    return backed_up

def list_backups(cfg):
    backup_dir = cfg["backup_dir"]
    if not os.path.exists(backup_dir):
        print("  No backups yet.")
        return
    files = sorted(os.listdir(backup_dir), reverse=True)
    if not files:
        print("  No backups found.")
        return
    print(f"\n  📋 Backups in {backup_dir}:")
    total_size = 0
    for f in files[:20]:
        path = os.path.join(backup_dir, f)
        size = human_size(path)
        total_size += size
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        print(f"  {f:<45} {format_size(size):>8}  {mtime.strftime('%Y-%m-%d %H:%M')}")
    print(f"\n  Total: {len(files)} backups, {format_size(total_size)}")

def auto_backup_loop(cfg, stop_event):
    """Run backups on a schedule until stop_event is set."""
    interval = cfg["interval_mins"] * 60
    while not stop_event.is_set():
        run_backup(cfg)
        print(f"  ⏰ Next backup in {cfg['interval_mins']} minutes. Press Ctrl+C to stop.")
        stop_event.wait(interval)

def main():
    print("=" * 52)
    print("  💾 Auto Backup System")
    print("=" * 52)

    cfg = load_config()
    print(f"\n  Backup directory: {cfg['backup_dir']}")
    print(f"  Sources: {len(cfg['source_dirs'])} configured")
    print(f"  Interval: every {cfg['interval_mins']} minutes")
    print(f"  Keep last: {cfg['max_backups']} backups")
    print(f"  Compress: {'Yes (zip)' if cfg['compress'] else 'No (copy)'}")

    while True:
        print("\n  Options:")
        print("  [1] Run backup now")
        print("  [2] Start auto-backup (runs every N minutes)")
        print("  [3] List existing backups")
        print("  [4] Edit config")
        print("  [5] Quit")
        choice = input("\n  Choice: ").strip()

        if choice == "1":
            run_backup(cfg)

        elif choice == "2":
            print(f"\n  🔄 Auto-backup started (every {cfg['interval_mins']} min)")
            print("  Press Ctrl+C to stop\n")
            stop_event = threading.Event()
            try:
                auto_backup_loop(cfg, stop_event)
            except KeyboardInterrupt:
                stop_event.set()
                print("\n  Auto-backup stopped.")

        elif choice == "3":
            list_backups(cfg)

        elif choice == "4":
            print("\n  Edit backup_config.json to change settings.")
            print(f"  File location: {os.path.abspath(CONFIG_FILE)}")

        elif choice == "5":
            break

    print("\n  Goodbye! Your worlds are safe. 💾")

if __name__ == "__main__":
    main()
