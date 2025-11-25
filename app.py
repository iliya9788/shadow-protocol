from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "shadow_protocol_secret"

# -------------------------------------------------
# DATABASE (اختیاری – بعداً می‌تونیم استفاده کنیم)
# -------------------------------------------------
def get_db():
    conn = sqlite3.connect("database/game.db")
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------------------------------
# ROUTES اصلی
# -------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start")
def start():
    # شروع بازی از حالت اولیه
    session["state"] = "intro"
    return redirect("/terminal")


@app.route("/terminal")
def terminal():
    return render_template("terminal.html")


@app.route("/detected")
def detected():
    return render_template("detected.html")


@app.route("/ending/loyal")
def ending_loyal():
    return render_template("ending_loyal.html")


@app.route("/ending/rebel")
def ending_rebel():
    return render_template("ending_rebel.html")


# -------------------------------------------------
# API COMMAND SYSTEM (هستهٔ بازی)
# -------------------------------------------------
@app.route("/api/command", methods=["POST"])
def api_command():
    data = request.get_json()
    cmd = (data.get("command") or "").strip().lower()
    state = session.get("state", "intro")

    # ----------------------------
    # STAGE 1 — INTRO / BREACH POINT
    # ----------------------------
    if state == "intro":

        if cmd == "scan network":
            response = (
                "DIVISION-71 // SHADOW PROTOCOL ONLINE\n"
                "SECURE LINK ESTABLISHED.\n"
                "AGENT: You are now inside a hostile perimeter.\n\n"
                "Running network scan...\n"
                "Network scan complete.\n"
                "3 nodes detected:\n"
                " - node_04 (encrypted)   [HIGH VALUE]\n"
                " - node_12 (inactive)\n"
                " - node_09 (unstable)\n\n"
                "HINT: High-value targets are usually encrypted.\n"
                "Try: connect node_04 --auth"
            )
            return jsonify({"response": response})

        elif cmd == "connect node_04 --auth":
            session["state"] = "stage1_auth"
            response = (
                "Attempting secure tunnel to node_04...\n"
                "ENCRYPTION LAYER: ACTIVE\n"
                "AUTH CHANNEL OPENED.\n\n"
                "Last operative left a fragmented key in the system logs:\n"
                "AUTH KEY FRAGMENT: alpha-71\n"
                "(Format: <word>-<number>)\n\n"
                "Enter passcode to continue."
            )
            return jsonify({"response": response})

        elif cmd == "help":
            response = (
                "/// SHADOW PROTOCOL – HELP ///\n"
                "- Your link is unstable. You must move quickly.\n"
                "- Start by mapping the target:\n"
                "  scan network\n"
                "- Then try to authenticate with the critical node:\n"
                "  connect node_04 --auth\n"
            )
            return jsonify({"response": response})

        else:
            return jsonify({"response": "SYSTEM: Unknown command in entry state. Try: scan network"})

    # ----------------------------
    # STAGE 1 — PASSCODE
    # ----------------------------
    elif state == "stage1_auth":

        if cmd == "alpha-71":
            session["state"] = "node1"
            response = (
                "PASSCODE ACCEPTED.\n"
                "Node_04 decrypted successfully.\n\n"
                "You slip past the outer perimeter.\n"
                "Behind the silence, an adaptive FIREWALL NODE awakens.\n\n"
                "Entering FIREWALL NODE...\n"
                "HINT: Before moving, analyze the defenses.\n"
                "Try: scan firewalls"
            )
            return jsonify({"response": response})

        elif cmd == "help":
            return jsonify({"response": "PASSCODE HINT: alpha-71 (you saw it in the fragmented key)."})

        else:
            return jsonify({"response": "ACCESS DENIED. Passcode incorrect. The fragment was: alpha-71"})

    # ----------------------------
    # STAGE 2 — FIREWALL NODE
    # ----------------------------
    elif state == "node1":

        if cmd == "scan firewalls":
            response = (
                "FIREWALL ANALYSIS ONLINE…\n\n"
                "3 FIREWALL NODES DETECTED:\n"
                " - node_7a (slow)     [HEAVY LOGGING – HIGH VISIBILITY]\n"
                " - node_9b (active)   [AGGRESSIVE TRACE ENGINE]\n"
                " - node_5c (mirror)   [ROUTES TRAFFIC AS REFLECTION]\n\n"
                "In stealth operations, mirrored routes are often the safest.\n"
                "HINT: Choose the node that reflects rather than attacks.\n"
                "Try: bypass node_5c   (or risk the others…)"
            )
            return jsonify({"response": response})

        elif cmd == "bypass node_5c":
            session["state"] = "stage3"
            response = (
                "Bypassing node_5c...\n"
                "MIRROR CHANNEL ENGAGED.\n"
                "Your packets are reflected as harmless noise.\n\n"
                "FIREWALL NODE CLEARED.\n"
                "STAGE 2 COMPLETE.\n\n"
                "Deep inside the network, an echo stirs.\n"
                "Operative X — the one marked as 'missing in action' — left something here.\n"
                "A broken transmission, encoded and buried.\n\n"
                "HINT: Echoes must be decoded.\n"
                "Try: decode"
            )
            return jsonify({"response": response})

        elif cmd in ["bypass node_7a", "bypass node_9b"]:
            session["state"] = "trace_warning"
            response = (
                "⚠ SECURITY ALERT ⚠\n"
                "You chose a noisy or aggressive firewall.\n"
                "TRACE ENGINE ACTIVATED.\n\n"
                "A hostile system has locked onto your signal.\n"
                "You have 5 seconds to sever the link.\n"
                "COMMAND REQUIRED: disconnect"
            )
            return jsonify({"response": response, "trace": True})

        elif cmd == "help":
            response = (
                "FIREWALL HELP:\n"
                "- Scan first: scan firewalls\n"
                "- Think like a ghost: heavy logging and active engines are dangerous.\n"
                "- Mirror nodes echo traffic instead of attacking it.\n"
                "Hint: node_5c."
            )
            return jsonify({"response": response})

        else:
            return jsonify({"response": "Unknown command in FIREWALL NODE. Try: scan firewalls"})

    # ----------------------------
    # TRACE WARNING
    # ----------------------------
    elif state == "trace_warning":

        if cmd == "disconnect":
            session["state"] = "node1"
            response = (
                "LINK SEVERED.\n"
                "TRACE VECTOR LOST.\n\n"
                "You barely slip back into the shadows.\n"
                "You are once again at the FIREWALL NODE.\n"
                "Try a different route this time.\n"
                "Hint: scan firewalls"
            )
            return jsonify({"response": response})

        else:
            session["state"] = "detected"
            response = (
                "TRACE COMPLETE.\n"
                "YOUR POSITION IS COMPROMISED.\n"
                "The system flags you as a hostile entity.\n"
                "Connection forcibly terminated."
            )
            return jsonify({"response": response, "redirect": "/detected"})

    # ----------------------------
    # STAGE 3 — ECHO CHAMBER
    # ----------------------------
    elif state == "stage3":

        if cmd == "decode":
            response = (
                "ECHO CHANNEL OPENED…\n"
                "Recovered fragment from OPERATIVE X (Status: PRESUMED DEAD):\n\n"
                "\"They told us Division-71 protected people.\n"
                " If you're reading this, you already feel the cracks.\n"
                " I encoded the truth inside this payload. Only those who can decode it\n"
                " are worthy of knowing what really sits in THE CORE.\"\n\n"
                "ENCRYPTED PAYLOAD (BASE64):\n"
                "VEhFIFRSVVRIIElTIElOIFRIRSBDT1JF\n\n"
                "HINT:\n"
                "- This is Base64.\n"
                "- Decode it using your brain, your tools… or pure insight.\n"
                "- Then reply with:\n"
                "  decode <decoded text>\n"
                "Example:\n"
                "  decode the truth is ..."
            )
            return jsonify({"response": response})

        elif cmd.startswith("decode "):
            text = cmd.replace("decode ", "").strip()

            if text == "the truth is in the core":
                session["state"] = "core"
                response = (
                    "DECRYPTION COMPLETE.\n"
                    "MESSAGE VERIFIED AS AUTHENTIC.\n\n"
                    "OPERATIVE X WAS RIGHT.\n"
                    "The truth doesn’t sit on the edges of the network — it lives in the CORE.\n\n"
                    "You follow the coordinates embedded between the bits.\n"
                    "Firewalls dim. Silence turns heavy.\n"
                    "You are standing at the heart of Division-71’s data vault.\n\n"
                    "ENTERING THE CORE…\n"
                    "Type: list files"
                )
                return jsonify({"response": response})
            else:
                return jsonify({"response": "Decryption failed. That is not what the echo said. (Hint: decode the Base64.)"})

        elif cmd == "help":
            response = (
                "ECHO CHAMBER HELP:\n"
                "- Use: decode\n"
                "- Read the Base64 payload carefully.\n"
                "- Decode it (manually or with a tool) and send it back as:\n"
                "  decode the truth is in the core"
            )
            return jsonify({"response": response})

        else:
            return jsonify({"response": "Unknown command in ECHO CHAMBER. Try: decode"})

    # ----------------------------
    # STAGE 4 — THE CORE
    # ----------------------------
    elif state == "core":

        if cmd == "list files":
            response = (
                "[CORE FILESYSTEM MOUNTED]\n\n"
                " - protocol_shadow.sys   (master control routine)\n"
                " - division71_logs.sec   (classified incident logs)\n"
                " - truth.dat             (sealed dossier)\n\n"
                "One of these files doesn’t align with the rest.\n"
                "HINT: You came here because of 'the truth'.\n"
                "Try: open truth.dat"
            )
            return jsonify({"response": response})

        elif cmd == "open truth.dat":
            response = (
                "Opening: truth.dat …\n"
                "Decompressing historical event stream…\n\n"
                ">> DIVISION-71 // INTERNAL MEMO // REDACTED <<\n"
                "- Data streams were altered.\n"
                "- Polls, records, even identities rewritten.\n"
                "- All in the name of \"stability\".\n\n"
                "OPERATIVE X (last note):\n"
                "\"If you’ve reached this file, you see it now.\n"
                " The world you know was curated.\n"
                " You can burn this evidence and keep the lie alive…\n"
                " or you can expose everything and let the system collapse.\"\n\n"
                "You must decide:\n"
                " - destroy evidence\n"
                " - reveal truth"
            )
            return jsonify({"response": response})

        elif cmd == "destroy evidence":
            session["state"] = "ending_loyal"
            response = (
                "You trigger a silent wipe.\n"
                "truth.dat dissolves into white noise.\n"
                "Logs are rewritten. Shadows re-align into place.\n\n"
                "DIVISION-71 marks the operation as a success.\n"
                "No one will ever know what was erased here.\n"
                "But you will.\n\n"
                "Redirecting to final report..."
            )
            return jsonify({"response": response, "redirect": "/ending/loyal"})

        elif cmd == "reveal truth":
            session["state"] = "ending_rebel"
            response = (
                "You reroute truth.dat to every public node you can reach.\n"
                "Firewalls scream. Warning lights flood the CORE.\n\n"
                "Within seconds, Division-71 cannot contain the leak.\n"
                "Reality starts to realign itself around raw, unfiltered truth.\n\n"
                "You won’t be a hero in their reports.\n"
                "You’ll be a traitor in their system.\n"
                "But maybe, finally, the world will see what was done to it.\n\n"
                "Redirecting to fallout sequence..."
            )
            return jsonify({"response": response, "redirect": "/ending/rebel"})

        elif cmd == "help":
            response = (
                "CORE HELP:\n"
                "- Scan files: list files\n"
                "- Open the dossier that matters: open truth.dat\n"
                "- Choose:\n"
                "  destroy evidence   (stay loyal to Division-71)\n"
                "  reveal truth       (side with the victims)"
            )
            return jsonify({"response": response})

        else:
            return jsonify({"response": "Unknown command in CORE. Try: list files or open truth.dat"})

    # ----------------------------
    # FALLBACK STATE
    # ----------------------------
    else:
        session["state"] = "intro"
        return jsonify({"response": "SYSTEM RESET.\nLink re-initialized.\nType: scan network"})


# -------------------------------------------------
# RUN SERVER
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
