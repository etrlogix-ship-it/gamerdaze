#!/usr/bin/env python3
"""
Auto-Restart Watchdog - Project 19
Monitors your game server process and restarts it if it crashes.
"""

import os
import subprocess
import time
import datetime
import sys
import json

CONFIG = {
    "server_command": ["java", "-Xmx2G", "-Xms1G", "-jar", "server.jar", "nogui"],
    "server_dir":     os.path.expanduser("~/minecraft_server_files"),
    "restart_delay":  10,    # seconds to wait before restarting
    "max_restarts":   5,     # max restarts per hour before giving up
    "log_file":       "watchdog.log",
    "crash_keywords": ["FATAL", "OutOfMemoryError", "JVM crash"],
}

restart_times = []

def log(msg):
    ts  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(CONFIG["log_file"], "a") as f:
        f.write(line + "\n")

def too_many_restarts():
    now = time.time()
    # Keep only restarts in the last hour
    recent = [t for t in restart_times if now - t < 3600]
    restart_times.clear()
    restart_times.extend(recent)
    return len(restart_times) >= CONFIG["max_restarts"]

def start_server():
    log(f"🚀 Starting server: {' '.join(CONFIG['server_command'])}")
    work_dir = CONFIG["server_dir"]

    if not os.path.exists(work_dir):
        log(f"❌ Server directory not found: {work_dir}")
        log("  Edit CONFIG['server_dir'] in watchdog.py")
        return None

    try:
        proc = subprocess.Popen(
            CONFIG["server_command"],
            cwd=work_dir,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        log(f"✅ Server started (PID {proc.pid})")
        return proc
    except FileNotFoundError as e:
        log(f"❌ Could not start server: {e}")
        log("  Check that the server command is correct in CONFIG")
        return None

def monitor_output(proc):
    """Read server output and watch for crash keywords."""
    try:
        for line in proc.stdout:
            line = line.rstrip()
            if line:
                print(f"  [SERVER] {line}")
                # Check for crash indicators
                for keyword in CONFIG["crash_keywords"]:
                    if keyword in line:
                        log(f"⚠️  Crash keyword detected: '{keyword}'")
    except:
        pass

def run_watchdog():
    log("🐕 Watchdog started")
    log(f"   Max restarts per hour: {CONFIG['max_restarts']}")
    log(f"   Restart delay: {CONFIG['restart_delay']}s")

    import threading

    while True:
        proc = start_server()
        if proc is None:
            log("❌ Could not start server. Check configuration.")
            break

        restart_times.append(time.time())

        # Monitor output in background thread
        output_thread = threading.Thread(target=monitor_output, args=(proc,), daemon=True)
        output_thread.start()

        # Wait for server to exit
        proc.wait()
        exit_code = proc.returncode
        log(f"⚠️  Server exited with code {exit_code}")

        if exit_code == 0:
            log("✅ Server shut down cleanly. Watchdog stopping.")
            break

        # Check if too many restarts
        if too_many_restarts():
            log(f"🛑 Too many restarts ({CONFIG['max_restarts']}/hour). Giving up!")
            log("   Check server logs for the underlying issue.")
            break

        log(f"⏳ Restarting in {CONFIG['restart_delay']} seconds...")
        log(f"   Restarts this hour: {len(restart_times)}/{CONFIG['max_restarts']}")
        time.sleep(CONFIG["restart_delay"])

    log("🐕 Watchdog stopped.")

def demo_mode():
    """Simulate a server crash and restart."""
    print("\n  🎭 DEMO MODE — simulating server crash and restart\n")

    class FakeProc:
        def __init__(self, lifetime):
            self.pid = 99999
            self.returncode = None
            self._lifetime = lifetime
            self._start = time.time()

        def wait(self):
            while time.time() - self._start < self._lifetime:
                time.sleep(0.5)
            self.returncode = -1
            return -1

        @property
        def stdout(self):
            return iter([
                "Server starting...\n",
                "Done! For help, type 'help'\n",
                "Player joined: Steve\n",
            ])

        def poll(self):
            return self.returncode

    for attempt in range(1, 4):
        log(f"🚀 Starting demo server (attempt {attempt}/3)")
        log(f"✅ Server started (PID 99999)")
        fake = FakeProc(lifetime=3)

        import threading
        output_thread = threading.Thread(target=monitor_output, args=(fake,), daemon=True)
        output_thread.start()

        fake.wait()
        log(f"⚠️  Server crashed! Exit code: -1")
        if attempt < 3:
            log(f"⏳ Restarting in 2 seconds...")
            time.sleep(2)

    log("🎭 Demo complete — in real use, this would keep restarting!")

def main():
    print("=" * 52)
    print("  🐕 Auto-Restart Watchdog")
    print("=" * 52)
    print("\n  This script monitors your server and restarts it")
    print("  automatically if it crashes.\n")

    print("  [1] Start watchdog (real server)")
    print("  [2] Demo mode (simulated crash/restart)")
    print("  [3] Show config")
    print("  [4] Quit")
    choice = input("\n  Choice: ").strip()

    if choice == "1":
        print("\n  Press Ctrl+C to stop the watchdog (server will also stop)\n")
        try:
            run_watchdog()
        except KeyboardInterrupt:
            log("  🛑 Watchdog stopped by user.")

    elif choice == "2":
        try:
            demo_mode()
        except KeyboardInterrupt:
            print("\n  Demo stopped.")

    elif choice == "3":
        print("\n  Current config:")
        for k, v in CONFIG.items():
            print(f"  {k}: {v}")
        print("\n  Edit CONFIG dict in watchdog.py to change settings.")

    print("\n  Watchdog closed. 🐕")

if __name__ == "__main__":
    main()
