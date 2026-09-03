"""
Scandinavian Mentor CLI Bridge
Allows Antigravity (or the user from terminal) to inspect and control the visual board in real time.
"""
import sys
import json
import urllib.request
import urllib.error

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SERVER_URL = "http://127.0.0.1:5050"

def post_json(endpoint, payload):
    url = f"{SERVER_URL}{endpoint}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=3) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError:
        print("[!] Could not connect to mentor server at http://127.0.0.1:5050. Is mentor_server.py running?")
        return None

def get_json(endpoint):
    url = f"{SERVER_URL}{endpoint}"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=3) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError:
        print("[!] Could not connect to mentor server at http://127.0.0.1:5050. Is mentor_server.py running?")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python mentor_cli.py [state|move|say|arrow|lesson|reset]")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "state":
        res = get_json("/api/state")
        if res:
            print("=" * 60)
            print(f"Lesson: {res.get('lesson_name')} (Step {res.get('step_index')}/{res.get('total_steps')})")
            print(f"FEN: {res.get('fen')}")
            print(f"Moves: {' '.join(res.get('history', []))}")
            print(f"Turn: {res.get('turn')}")
            print(f"Coach Says: {res.get('coach_message')}")
            print(f"Expected Move: {res.get('expected_move')}")
            print("=" * 60)

    elif cmd == "move":
        if len(sys.argv) < 3:
            print("Usage: python mentor_cli.py move <san_or_uci>")
            sys.exit(1)
        move_str = sys.argv[2]
        res = post_json("/api/mentor_action", {"action": "move", "move": move_str})
        if res:
            print(f"[+] Moved {move_str} on the board!")

    elif cmd == "say":
        if len(sys.argv) < 3:
            print("Usage: python mentor_cli.py say \"<message>\" [\"<tip>\"]")
            sys.exit(1)
        msg = sys.argv[2]
        tip = sys.argv[3] if len(sys.argv) > 3 else None
        res = post_json("/api/mentor_action", {"action": "say", "message": msg, "tip": tip})
        if res:
            print("[+] Mentor dialogue updated on user's screen!")

    elif cmd == "arrow":
        if len(sys.argv) < 4:
            print("Usage: python mentor_cli.py arrow <from_sq> <to_sq> [color]")
            sys.exit(1)
        f_sq = sys.argv[2]
        t_sq = sys.argv[3]
        col = sys.argv[4] if len(sys.argv) > 4 else "green"
        res = post_json("/api/mentor_action", {"action": "arrow", "from": f_sq, "to": t_sq, "color": col})
        if res:
            print(f"[+] Drew {col} arrow from {f_sq} to {t_sq}!")

    elif cmd == "lesson":
        if len(sys.argv) < 3:
            print("Usage: python mentor_cli.py lesson <lesson_id>")
            sys.exit(1)
        lid = sys.argv[2]
        res = post_json("/api/lesson", {"lesson_id": lid})
        if res:
            print(f"[+] Switched to lesson: {lid}!")

    elif cmd == "reset":
        res = post_json("/api/mentor_action", {"action": "reset"})
        if res:
            print("[+] Lesson reset to start!")

if __name__ == "__main__":
    main()
