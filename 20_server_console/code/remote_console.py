#!/usr/bin/env python3
"""Remote Server Console - Project 20
Control your Minecraft server from a web browser.
Install: pip install flask
"""
from flask import Flask, request, jsonify, render_template_string
import subprocess, threading, collections, time, os

app = Flask(__name__)
server_proc = None
output_buffer = collections.deque(maxlen=200)
SERVER_DIR = os.path.expanduser("~/minecraft_server_files")

HTML = """<!DOCTYPE html>
<html>
<head>
<title>Server Console</title>
<style>
body{background:#1a1a1a;color:#00ff00;font-family:monospace;margin:20px}
#output{background:#000;padding:15px;height:400px;overflow-y:auto;border:1px solid #333;margin-bottom:10px;white-space:pre-wrap}
input{width:70%;padding:8px;background:#222;color:#0f0;border:1px solid #444;font-family:monospace}
button{padding:8px 16px;background:#333;color:#0f0;border:1px solid #555;cursor:pointer;margin-left:5px}
button:hover{background:#555}
.status{color:#ff0;margin-bottom:10px}
</style>
</head>
<body>
<h2>🎮 Game Server Console</h2>
<div class="status" id="status">Connecting...</div>
<div id="output"></div>
<input id="cmd" placeholder="Type a command and press Enter..." onkeydown="if(event.key==='Enter')send()">
<button onclick="send()">Send</button>
<button onclick="clearOutput()">Clear</button>
<script>
let lastLen = 0;
function send(){
  const cmd = document.getElementById("cmd").value;
  if(!cmd) return;
  fetch("/send", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({cmd})});
  document.getElementById("cmd").value = "";
}
function clearOutput(){ document.getElementById("output").innerHTML = ""; lastLen = 0; }
async function poll(){
  const r = await fetch("/output?since="+lastLen);
  const d = await r.json();
  if(d.lines.length){
    const out = document.getElementById("output");
    d.lines.forEach(l => out.innerHTML += l + "\n");
    lastLen += d.lines.length;
    out.scrollTop = out.scrollHeight;
  }
  document.getElementById("status").textContent = d.running ? "✅ Server Running" : "🔴 Server Stopped";
  setTimeout(poll, 1000);
}
poll();
</script>
</body></html>"""

@app.route("/")
def index(): return HTML

@app.route("/send", methods=["POST"])
def send_cmd():
    global server_proc
    cmd = request.json.get("cmd","").strip()
    if cmd and server_proc and server_proc.stdin:
        try:
            server_proc.stdin.write(cmd + "\n")
            server_proc.stdin.flush()
            output_buffer.append(f"> {cmd}")
        except:
            output_buffer.append("[Error sending command]")
    return jsonify({"ok": True})

@app.route("/output")
def get_output():
    since = int(request.args.get("since", 0))
    lines = list(output_buffer)
    new_lines = lines[since:] if since < len(lines) else []
    running = server_proc is not None and server_proc.poll() is None
    return jsonify({"lines": new_lines, "running": running})

def read_output():
    global server_proc
    if server_proc and server_proc.stdout:
        for line in server_proc.stdout:
            output_buffer.append(line.rstrip())

def demo_mode():
    """Simulate a running server for demo."""
    demo_lines = [
        "Starting Minecraft server version 1.21",
        "Loading properties",
        "Default game type: SURVIVAL",
        "Done! For help, type \"help\"",
        "Player joined: Steve",
        "Player joined: Alex",
        "[Steve]: Hello!",
    ]
    for line in demo_lines:
        output_buffer.append(line)
        time.sleep(0.3)
    while True:
        time.sleep(10)
        output_buffer.append(f"[Server] {int(time.time())} — server tick")

if __name__ == "__main__":
    import sys
    print("=" * 48)
    print("  🖥️  Remote Server Console")
    print("=" * 48)
    print("\n  Open http://localhost:5000 in your browser")
    print("  Press Ctrl+C to stop\n")

    if "--demo" in sys.argv or not os.path.exists(SERVER_DIR):
        print("  Running in DEMO mode (no real server)")
        threading.Thread(target=demo_mode, daemon=True).start()
    else:
        cmd = ["java", "-Xmx2G", "-jar", "server.jar", "nogui"]
        server_proc = subprocess.Popen(cmd, cwd=SERVER_DIR,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, bufsize=1)
        threading.Thread(target=read_output, daemon=True).start()

    app.run(host="0.0.0.0", port=5000, debug=False)
