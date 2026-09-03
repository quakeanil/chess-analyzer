"""
Scandinavian Mentor Web Server
Flask-based live communication server connecting the user's interactive browser board with Antigravity AI Coach.
"""
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.mentor_engine import session

app = Flask(__name__, static_folder=".")
CORS(app)

@app.route("/")
@app.route("/mentor")
def serve_mentor_page():
    return send_from_directory(".", "mentor.html")

@app.route("/dashboard")
def serve_dashboard_page():
    return send_from_directory(".", "dashboard.html")

@app.route("/<path:path>")
def serve_static(path):
    if os.path.exists(path):
        return send_from_directory(".", path)
    return "Not Found", 404

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/api/state", methods=["GET"])
def get_state():
    return jsonify(session.get_state())

@app.route("/api/move", methods=["POST"])
def make_user_move():
    data = request.json or {}
    move_str = data.get("move", "")
    if not move_str:
        return jsonify({"error": "No move provided"}), 400
    state = session.play_user_move(move_str)
    return jsonify(state)

@app.route("/api/takeback", methods=["POST"])
def takeback_move():
    return jsonify(session.takeback())

@app.route("/api/mode", methods=["POST"])
def set_session_mode():
    data = request.json or {}
    mode = data.get("mode", "explore_white")
    session.reset_session(mode=mode)
    return jsonify(session.get_state())

@app.route("/api/play_white", methods=["POST"])
def play_white():
    data = request.json or {}
    move = data.get("move", "")
    if not move:
        return jsonify({"error": "No move provided"}), 400
    return jsonify(session.play_white_move(move))

@app.route("/api/blunder", methods=["POST"])
def set_blunder():
    data = request.json or {}
    puzzle_id = data.get("puzzle_id", "blunder_2e5_advance")
    return jsonify(session.set_blunder_puzzle(puzzle_id))

@app.route("/api/gm_game", methods=["POST"])
def set_gm():
    data = request.json or {}
    game_id = data.get("game_id", "carlsen_caruana_2014")
    return jsonify(session.set_gm_game(game_id))

@app.route("/api/hint", methods=["GET", "POST"])
def get_hint():
    return jsonify(session.get_hint())

@app.route("/api/threat", methods=["GET", "POST"])
def get_threat():
    return jsonify(session.get_threat())

@app.route("/api/analyze", methods=["GET", "POST"])
def run_analysis():
    session.update_analysis()
    return jsonify(session.get_state())

@app.route("/api/bot_play", methods=["GET", "POST"])
def bot_play():
    return jsonify(session.bot_play_move())

@app.route("/api/lesson", methods=["POST"])
def change_lesson():
    data = request.json or {}
    lesson_id = data.get("lesson_id", "scandi_qa5")
    session.reset_session(lesson_id=lesson_id, mode="lesson")
    return jsonify(session.get_state())

@app.route("/api/mentor_action", methods=["POST"])
def mentor_action():
    data = request.json or {}
    action = data.get("action", "")
    
    if action == "move":
        res = session.mentor_move(data.get("move", ""))
        return jsonify(res)
    elif action == "say":
        session.mentor_say(
            data.get("message", ""),
            tip=data.get("tip"),
            arrows=data.get("arrows")
        )
        return jsonify({"success": True, "state": session.get_state()})
    elif action == "arrow":
        f = data.get("from")
        t = data.get("to")
        color = data.get("color", "green")
        if f and t:
            session.arrows = [{"from": f, "to": t, "color": color}]
        return jsonify({"success": True, "state": session.get_state()})
    elif action == "reset":
        session.reset_lesson(session.lesson_id)
        return jsonify({"success": True, "state": session.get_state()})
    
    return jsonify({"error": f"Unknown action: {action}"}), 400

if __name__ == "__main__":
    port = 5050
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    print("=" * 60)
    print(f"🎓 SCANDINAVIAN MENTOR LIVE SERVER RUNNING ON PORT {port}")
    print(f"👉 Open in your browser: http://localhost:{port}/mentor")
    print("=" * 60)
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
