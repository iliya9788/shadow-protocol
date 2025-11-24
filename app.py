from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "shadow_protocol_secret"

# ----------------------------------------
# DATABASE - اگر بعداً خواستی استفاده می‌کنیم
# ----------------------------------------
def get_db():
    conn = sqlite3.connect("database/game.db")
    conn.row_factory = sqlite3.Row
    return conn

# ----------------------------------------
# ROUTES
# ----------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start")
def start():
    session["state"] = "intro"
    return redirect("/terminal")


# صفحهٔ ترمینال فقط خودِ UI را نشان می‌دهد
@app.route("/terminal")
def terminal():
    return render_template("terminal.html")


# API — پردازش دستورات ترمینال، بدون رفرش
@app.route("/api/command", methods=["POST"])
def api_command():
    data = request.get_json()
    cmd = (data.get("command") or "").strip().lower()

    # وضعیت بازی
    state = session.get("state", "intro")
    response = ""

    # ------------------------------
    # مرحله اول (دموی ساده)
    # ------------------------------
    if state == "intro":
        if cmd == "scan network":
            response = "Network scan complete. 3 nodes detected."
        elif cmd == "connect node 1":
            session["state"] = "node1"
            response = "Connected to Node 1."
        elif cmd == "help":
            response = "Commands: scan network, connect node 1, help, exit"
        elif cmd == "exit":
            session.clear()
            response = "Session ended."
        else:
            response = "Unknown command."

    # ------------------------------
    # مرحله دوم (Node 1)
    # ------------------------------
    elif state == "node1":
        if cmd == "status":
            response = "Node 1 Status: FIREWALL BYPASSED."
        elif cmd == "back":
            session["state"] = "intro"
            response = "Returning to main network..."
        else:
            response = "Node 1 > Unknown command."

    return jsonify({"response": response})


@app.route("/detected")
def detected():
    return render_template("detected.html")


@app.route("/ending/loyal")
def ending_loyal():
    return render_template("ending_loyal.html")


@app.route("/ending/rebel")
def ending_rebel():
    return render_template("ending_rebel.html")


if __name__ == "__main__":
    app.run(debug=True)
