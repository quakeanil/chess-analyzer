"""
Scandinavian Mentor Engine with:
1. Explore White Mode (Top 10 moves for White with win rates & strength status)
2. Master Lessons Mode (8 Scandinavian Grandmaster curriculum lines)
3. Blunder Quiz Mode (Replay 0kanil's real Chess.com lost games)
4. Pawn Skeleton & Plans Blueprint (Visual pawn structure, breaks, and outposts)
5. Guess the Move with Grandmasters (Carlsen, Tiviakov masterclasses)
"""
import os
import json
import chess
import chess.engine
from src.scandi_curriculum import LESSONS, GOLDEN_RULES, get_lesson, list_lessons
from src.scandi_blunders import OKANIL_SCANDI_BLUNDERS, get_blunder_puzzle, list_blunder_puzzles
from src.scandi_gm_games import GM_GAMES, get_gm_game, list_gm_games
from src.scandi_pawn_guide import PAWN_PLANS, get_pawn_guide
from src.engine_analyzer import find_stockfish, score_to_str, score_to_cp

DESCRIPTIVE_MOVE_NAMES = {
    # Black moves
    "d5": "Scandinavian Central Strike (1...d5!)",
    "Qxd5": "Mieses-Kotrc: Recapture with Queen",
    "Nf6": "Modern Line: Delay Queen, develop knight",
    "Qa5": "Classical Square: Pin diagonal, eye c7 escape",
    "Qd6": "Carlsen / Tiviakov: Control e5, stop Bf4",
    "Qd8": "Banker Retreat: Deceptively solid, zero targets",
    "Bf5": "Active Bishop outside pawn chain (Rule #1)",
    "Bg4": "Portuguese Attack: Pin knight to Queen",
    "c6": "Golden Move: Create c7 Queen pocket (Rule #2)",
    "e6": "Solidify Center: Lock pawn chain after Bf5",
    "c5": "Central Strike: Break White's d4 center (Rule #4)",
    "Nxd5": "Recapture central d5 pawn with Knight",
    "Nc6": "Develop Queenside Knight, attack d4",
    "a6": "Carlsen Prophylaxis: Stop Nb5/Bb5",
    "Bb4": "Pin White's c3 Knight to King",
    "Be7": "Solid Kingside Development",
    "O-O": "Castle Kingside into safety",
    "O-O-O": "Queenside Castling Battery on d-file",
    "Qxg2": "Carlsen Pawn Snatch: Grabs g2 with tempo!",
    # White moves
    "e4": "King's Pawn Opening",
    "exd5": "Mainline Central Capture",
    "e5": "Advance Error (Overextends pawn, weakens d5)",
    "Nc3": "Natural Development, attacks Queen/d5",
    "d4": "Establishes classical pawn center",
    "Nf3": "Controls e5/d4, classical development",
    "c4": "Tries to cling to extra d5 pawn (Gambit invite)",
    "b4": "Wing Gambit: Tries to deflect Black's Queen",
    "d3": "Passive pawn defense",
    "Bd3": "Develops bishop, defends pawn",
    "Bc4": "Italian-style diagonal pressure on f7",
    "Be2": "Quiet classical development",
    "Bd2": "Discovered attack battery on Black Queen",
    "Qe2": "Pinning along e-file",
    "Qf3": "Aggressive Queen sortie targeting b7/f7"
}

def get_strength_status(rank, cp_diff):
    if rank == 1 or cp_diff <= 15:
        return "👑 Best Move"
    elif cp_diff <= 35:
        return "⚔️ Sharp / Strong"
    elif cp_diff <= 75:
        return "🛡️ Playable"
    elif cp_diff <= 140:
        return "⚠️ Inaccuracy"
    else:
        return "❌ Mistake"

def analyze_with_stockfish(board, depth=12, multipv=10, time_limit=0.35):
    engine_path = find_stockfish()
    if not engine_path or not os.path.exists(engine_path) or board.is_game_over():
        return [], "0.0"

    try:
        eng = chess.engine.SimpleEngine.popen_uci(engine_path)
        info = eng.analyse(board, chess.engine.Limit(time=time_limit, depth=depth), multipv=multipv)
        eng.quit()

        results = []
        overall_eval = "0.0"
        best_cp = None

        for i, entry in enumerate(info, 1):
            if "pv" not in entry or len(entry["pv"]) == 0:
                continue
            mv = entry["pv"][0]
            san = board.san(mv)
            uci = mv.uci()
            cp = score_to_cp(entry["score"], is_white_perspective=True)
            eval_str = score_to_str(entry["score"], is_white_perspective=True)

            if i == 1:
                overall_eval = eval_str
                best_cp = cp

            cp_diff = abs(cp - (best_cp if best_cp is not None else cp))
            strength = get_strength_status(i, cp_diff)

            prob_white = 1.0 / (1.0 + 10.0 ** (-cp / 400.0))
            w_pct = max(5, min(90, round(prob_white * 80 + 10)))
            d_pct = 30
            b_pct = max(5, 100 - w_pct - d_pct)

            pv_san_list = []
            temp_b = board.copy()
            for pv_m in entry["pv"][:5]:
                pv_san_list.append(temp_b.san(pv_m))
                temp_b.push(pv_m)

            name = DESCRIPTIVE_MOVE_NAMES.get(san, "Candidate Move")

            results.append({
                "rank": i,
                "san": san,
                "uci": uci,
                "from": uci[:2],
                "to": uci[2:4],
                "eval": eval_str,
                "strength": strength,
                "w": w_pct,
                "d": d_pct,
                "b": b_pct,
                "name": name,
                "pv": " ".join(pv_san_list)
            })

        return results, overall_eval
    except Exception as e:
        print(f"[Stockfish 18 Analysis Error]: {e}")
        return [], "0.0"

class ScandinavianMentorSession:
    def __init__(self):
        self.board = chess.Board()
        self.lesson_id = "scandi_qa5"
        self.mode = "explore_white"  # "explore_white", "lesson", "blunder_drill", "gm_game", "pawn_guide"
        self.step_index = 0
        self.history = []
        self.arrows = []
        self.highlights = []
        self.coach_message = ""
        self.coach_tip = ""
        self.last_quality = "Ready"
        self.top_moves = []
        self.white_top_moves = []
        self.engine_eval = "0.0"

        # Features 2, 4, 5 state
        self.blunder_puzzle_id = "blunder_2e5_advance"
        self.blunder_score = {"solved": 0, "total": 0, "streak": 0}
        self.gm_game_id = "carlsen_caruana_2014"
        self.gm_checkpoint_idx = 0
        self.gm_score = 0

        self.reset_session()

    def reset_lesson(self, lesson_id=None):
        return self.reset_session(lesson_id=lesson_id, mode="lesson")

    def reset_session(self, lesson_id=None, mode=None):
        if lesson_id:
            self.lesson_id = lesson_id
        if mode:
            self.mode = mode

        self.step_index = 0
        self.history = []
        self.arrows = []
        self.highlights = []

        if self.mode == "explore_white":
            self.board = chess.Board()
            mv_obj = self.board.parse_san("e4")
            self.board.push(mv_obj)
            self.history.append("e4")
            self.coach_message = "🔍 <b>Interactive Study Sandbox:</b> You are studying as Black. White opened with <b>1.e4</b>.<br>Play <b>1...d5</b> to start the Scandinavian Defense!"
            self.coach_tip = "Play 1...d5 on the board (or click Best Move)!"
            self.arrows = [{"from": "d7", "to": "d5", "color": "green"}]
            self.last_quality = "Sandbox Ready"
            self.update_analysis()

        elif self.mode == "explore_center":
            self.board = chess.Board()
            self.coach_message = "⚔️ <b>Center Game Study Sandbox:</b> You are studying as <b>White</b> (1.e4 e5 2.d4 exd4 3.Qxd4!).<br>Play <b>1.e4</b> to seize the center!"
            self.coach_tip = "Play 1.e4 on the board (or click Best Move)!"
            self.arrows = [{"from": "e2", "to": "e4", "color": "green"}]
            self.last_quality = "Center Game Ready"
            self.update_analysis()

        elif self.mode == "lesson":
            lesson = get_lesson(self.lesson_id)
            self.board = chess.Board(lesson.get("initial_fen", chess.STARTING_FEN))
            if lesson.get("white_first") and len(lesson["moves"]) > 0:
                first_step = lesson["moves"][0]
                first_move = first_step["bot_move"]
                mv_obj = self.board.parse_san(first_move)
                self.board.push(mv_obj)
                self.history.append(first_move)
                self.coach_message = f"🎓 <b>{lesson['name']}</b><br>{first_step.get('mentor_intro', 'White played 1.e4.')}"
                self.coach_tip = first_step.get("why_best", "What is Black's signature Scandinavian move?")
                self.arrows = [{"from": "d7", "to": "d5", "color": "green"}]
            else:
                self.coach_message = f"🎓 <b>{lesson['name']}</b><br>{lesson['subtitle']}"
                if len(lesson.get("moves", [])) > 0:
                    exp = lesson["moves"][0].get("expected_san", "e4")
                    exp_uci = lesson["moves"][0].get("expected_uci", "e2e4")
                    self.coach_tip = f"Play <b>{exp}</b> on the board to start!"
                    self.arrows = [{"from": exp_uci[:2], "to": exp_uci[2:4], "color": "green"}]
                else:
                    self.coach_tip = "Make your opening move on the board."
            self.update_analysis()

        elif self.mode == "blunder_drill":
            puzzle = get_blunder_puzzle(self.blunder_puzzle_id)
            self.board = chess.Board(puzzle["fen"])
            self.history = list(puzzle.get("history_lead", []))
            self.coach_message = f"⚡ <b>Personal Blunder Quiz: {puzzle['title']}</b><br>Opponent: {puzzle['opp_name']} ({puzzle['time_class']})<br><br>In your match, you played <span class='text-rose-400 font-bold'>{puzzle['okanil_san']}</span> ({puzzle['why_bad']}).<br><br>👉 <b>What should Black play instead?</b>"
            self.coach_tip = "Make Black's winning/saving move on the board!"
            self.last_quality = "Puzzle Active"
            self.arrows = []
            self.update_analysis()

        elif self.mode == "gm_game":
            game = get_gm_game(self.gm_game_id)
            self.gm_checkpoint_idx = 0
            chk = game["checkpoints"][0]
            self.board = chess.Board(chk["fen_before"])
            self.coach_message = f"👑 <b>Guess the Move: {game['title']}</b><br>Event: {game['event']} | Result: {game['result']}<br><br>{chk['question']}"
            self.coach_tip = f"Play the Grandmaster move as {game['black_player']}!"
            self.last_quality = "GM Challenge"
            self.arrows = []
            self.update_analysis()

        elif self.mode == "pawn_guide":
            guide = get_pawn_guide()
            skel = guide["skeleton_overview"]
            self.board = chess.Board(skel["fen"])
            self.history = ["1. e4", "d5", "2. exd5", "Qxd5", "3. Nc3", "Qa5", "4. d4", "Nf6", "5. Nf3", "c6"]
            self.coach_message = f"🗺️ <b>{skel['title']}</b><br>{skel['summary']}<br><br><b>Key Benefits:</b><br>• " + "<br>• ".join(skel['pros'])
            self.coach_tip = "Notice Black's c6 + e6 pawn chain and active bishop on c8/g4!"
            self.last_quality = "Pawn Blueprint"
            self.arrows = [{"from": "c7", "to": "c6", "color": "green"}, {"from": "e7", "to": "e6", "color": "green"}]
            self.highlights = ["c6", "e6", "d4", "c5", "f5"]
            self.update_analysis()

    def update_analysis(self):
        if self.board.is_game_over():
            self.top_moves = []
            self.white_top_moves = []
            self.engine_eval = "0.0"
            return

        multipv = 10 if (self.mode in ["explore_white", "explore_center"]) else 5
        moves, self.engine_eval = analyze_with_stockfish(self.board, multipv=multipv)
        if self.board.turn == chess.WHITE:
            self.white_top_moves = moves
            self.top_moves = []
        else:
            self.top_moves = moves
            self.white_top_moves = []

    def bot_play_move(self):
        if self.board.is_game_over():
            return self.get_state()
        self._reply_with_engine()
        self.update_analysis()
        if self.board.turn == chess.WHITE and self.white_top_moves:
            best_w = self.white_top_moves[0]
            self.arrows = [{"from": best_w["from"], "to": best_w["to"], "color": "green"}]
            self.coach_tip = f"Recommended White move: <b>{best_w['san']}</b>!"
        elif self.board.turn == chess.BLACK and self.top_moves:
            best_b = self.top_moves[0]
            self.arrows = [{"from": best_b["from"], "to": best_b["to"], "color": "green"}]
            self.coach_tip = f"Recommended Black move: <b>{best_b['san']}</b>!"
        return self.get_state()

    def set_blunder_puzzle(self, puzzle_id):
        self.blunder_puzzle_id = puzzle_id
        self.reset_session(mode="blunder_drill")
        return self.get_state()

    def set_gm_game(self, game_id):
        self.gm_game_id = game_id
        self.reset_session(mode="gm_game")
        return self.get_state()

    def play_white_move(self, move_str):
        try:
            try:
                move_obj = self.board.parse_san(move_str)
            except Exception:
                move_obj = self.board.parse_uci(move_str)
        except Exception as e:
            return {"error": f"Invalid move: {move_str}"}

        san = self.board.san(move_obj)
        self.board.push(move_obj)
        self.history.append(san)
        self.arrows = []
        self.highlights = []

        self.update_analysis()
        best_reply_text = ""
        if self.top_moves:
            best_black = self.top_moves[0]
            self.arrows = [{"from": best_black["from"], "to": best_black["to"], "color": "green"}]
            best_reply_text = f"<br><br>♟️ <b>Best Move for Black:</b> Play <b>{best_black['san']}</b> ({best_black['eval']}) — {best_black['name']}."
            self.coach_tip = f"Recommended reply: <b>{best_black['san']}</b>!"

        name = DESCRIPTIVE_MOVE_NAMES.get(san, "White move")
        self.coach_message = f"🏳️ <b>White played: {san}</b> ({name}).{best_reply_text}"
        self.last_quality = f"White: {san}"
        return self.get_state()

    def play_user_move(self, move_str):
        try:
            try:
                move_obj = self.board.parse_san(move_str)
            except Exception:
                move_obj = self.board.parse_uci(move_str)
        except Exception as e:
            return {"error": f"Invalid move: {move_str}"}

        san = self.board.san(move_obj)
        uci = move_obj.uci()

        # Handle White Move in Explore Mode
        if self.board.turn == chess.WHITE and self.mode == "explore_white":
            return self.play_white_move(san)

        # 1. BLUNDER QUIZ MODE
        if self.mode == "blunder_drill":
            puzzle = get_blunder_puzzle(self.blunder_puzzle_id)
            is_correct = (san == puzzle["expected_san"] or uci == puzzle["expected_uci"])
            self.blunder_score["total"] += 1
            if is_correct:
                self.blunder_score["solved"] += 1
                self.blunder_score["streak"] += 1
                self.last_quality = f"Solved! Streak: {self.blunder_score['streak']} 🔥"
                self.board.push(move_obj)
                self.history.append(san)
                self.arrows = [{"from": puzzle["expected_uci"][:2], "to": puzzle["expected_uci"][2:4], "color": "green"}]
                self.coach_message = f"🎉 <b>BRILLIANT! You found the refutation: {san}!</b><br>{puzzle['why_best']}<br><br><span class='text-emerald-400 font-mono'>Expected Line: {puzzle['pv']}</span>"
                self.coach_tip = "Streak increased! Try the next blunder puzzle."
            else:
                self.blunder_score["streak"] = 0
                self.last_quality = "Try Again ❌"
                self.arrows = [{"from": puzzle["expected_uci"][:2], "to": puzzle["expected_uci"][2:4], "color": "green"}]
                self.coach_message = f"❌ <b>Not quite. You played {san}.</b><br>{puzzle['why_bad']}<br><br>👉 Stockfish recommends: <b>{puzzle['expected_san']}</b> ({puzzle['best_eval']})!"
                self.coach_tip = f"The correct move was {puzzle['expected_san']}!"
            self.update_analysis()
            return self.get_state()

        # 2. GUESS THE GM MOVE MODE
        if self.mode == "gm_game":
            game = get_gm_game(self.gm_game_id)
            chk = game["checkpoints"][self.gm_checkpoint_idx]
            is_gm_move = (san == chk["best_move"] or uci == chk["best_uci"])
            if is_gm_move:
                self.gm_score += 100
                self.last_quality = "Grandmaster Match! ⭐ +100"
                self.board.push(move_obj)
                self.history.append(san)
                self.arrows = [{"from": chk["best_uci"][:2], "to": chk["best_uci"][2:4], "color": "green"}]
                self.coach_message = f"⭐ <b>AMAZING! You played exactly like {game['black_player']}: {san}!</b><br>{chk['explanation']}<br><br><i>{chk['gm_comment']}</i>"
                self.coach_tip = f"Score: {self.gm_score} pts! Moving to next checkpoint."
                if self.gm_checkpoint_idx + 1 < len(game["checkpoints"]):
                    self.gm_checkpoint_idx += 1
            else:
                self.last_quality = "Different Idea"
                self.arrows = [{"from": chk["best_uci"][:2], "to": chk["best_uci"][2:4], "color": "green"}]
                self.coach_message = f"You played <b>{san}</b>. {game['black_player']} chose <b>{chk['best_move']}</b>.<br>{chk['explanation']}"
                self.coach_tip = f"GM preferred {chk['best_move']}!"
            self.update_analysis()
            return self.get_state()

        # 3. STUDY SANDBOX MODE (SCANDINAVIAN - BLACK)
        if self.mode == "explore_white":
            self.board.push(move_obj)
            self.history.append(san)
            self.coach_message = f"♟️ You played <b>{san}</b>. Now choose from <b>White's Top 10 Moves</b> below to study White's responses!"
            self.coach_tip = "Pick any of White's moves in the Top 10 table to test that line!"
            self.last_quality = "Your Move"
            self.update_analysis()
            return self.get_state()

        # 3B. STUDY SANDBOX MODE (CENTER GAME - WHITE)
        if self.mode == "explore_center":
            self.board.push(move_obj)
            self.history.append(san)
            self.update_analysis()
            if self.board.turn == chess.BLACK:
                self.coach_message = f"🏳️ <b>You played {san}:</b> Now choose from <b>Black's Top 10 Moves</b> below to study Black's defense, or click 🤖 Bot Move!"
                self.coach_tip = "Select Black's move from the table, drag on board, or click Bot Move!"
                self.last_quality = f"White: {san}"
            else:
                best_w = self.white_top_moves[0] if self.white_top_moves else None
                if best_w:
                    self.arrows = [{"from": best_w["from"], "to": best_w["to"], "color": "green"}]
                    self.coach_message = f"♟️ <b>Black played {san}</b>.<br><br>👑 <b>Best Move for White:</b> Play <b>{best_w['san']}</b> ({best_w['eval']}) — {best_w['name']}."
                    self.coach_tip = f"Stockfish recommends: <b>{best_w['san']}</b>!"
                else:
                    self.coach_message = f"♟️ <b>Black played {san}</b>."
                    self.coach_tip = "Your turn as White!"
                self.last_quality = f"Black: {san}"
            return self.get_state()

        # 4. LESSON MODE
        self.board.push(move_obj)
        self.history.append(san)
        self.arrows = []
        self.highlights = []

        lesson = get_lesson(self.lesson_id)
        current_moves = lesson.get("moves", [])

        if self.step_index < len(current_moves):
            step = current_moves[self.step_index]
            expected_san = step.get("expected_san")
            expected_uci = step.get("expected_uci")
            alternatives = step.get("good_alternatives", [])
            blunders = step.get("blunders", {})

            is_best = (san == expected_san or uci == expected_uci)
            is_alt = (san in alternatives)

            if is_best or is_alt:
                self.last_quality = "Best Move" if is_best else "Good Alternative"
                why = step.get("why_best", "Excellent move!")
                self.step_index += 1

                is_white_lesson = (lesson.get("side") == "white")
                if is_white_lesson:
                    bot_mv_san = step.get("bot_move")
                    if bot_mv_san:
                        try:
                            bot_mv_obj = self.board.parse_san(bot_mv_san)
                            self.board.push(bot_mv_obj)
                            self.history.append(bot_mv_san)
                        except Exception:
                            self._reply_with_engine()

                    if self.step_index < len(current_moves):
                        next_step = current_moves[self.step_index]
                        intro = step.get("mentor_intro", f"Black plays {bot_mv_san}.")
                        self.coach_message = f"⭐ <b>{self.last_quality}: {san}!</b><br>{why}<br><br>🤖 <b>Opponent:</b> {intro}"
                        self.coach_tip = next_step.get("why_best", "Find White's best reply.")
                    else:
                        self.coach_message = f"🎉 <b>Lesson Complete!</b><br>{why}<br><br>You have mastered the Center Game setup!"
                        self.coach_tip = "Try another lesson or test your moves in Sandbox!"
                else:
                    if self.step_index < len(current_moves):
                        next_step = current_moves[self.step_index]
                        bot_mv_san = next_step.get("bot_move")
                        try:
                            bot_mv_obj = self.board.parse_san(bot_mv_san)
                            self.board.push(bot_mv_obj)
                            self.history.append(bot_mv_san)
                            intro = next_step.get("mentor_intro", f"White plays {bot_mv_san}.")
                            self.coach_message = f"⭐ <b>{self.last_quality}: {san}!</b><br>{why}<br><br>🤖 <b>Opponent:</b> {intro}"
                            self.coach_tip = next_step.get("why_best", "Find Black's best reply.")
                        except Exception:
                            self._reply_with_engine()
                    else:
                        self.coach_message = f"🎉 <b>Lesson Complete!</b><br>{why}<br><br>You have mastered this Scandinavian line!"
                        self.coach_tip = "Try another lesson or test White's Top 10 in Sandbox!"
            else:
                self.last_quality = "Deviation"
                blunder_reason = blunders.get(san)
                if not blunder_reason:
                    if san.startswith("e6") and not any(m in self.history for m in ["Bf5", "Bg4"]):
                        blunder_reason = "⚠️ <b>Rule #1:</b> You locked in your c8-Bishop with ...e6! Bring the bishop out first."
                    else:
                        blunder_reason = f"You played <b>{san}</b> (The lesson recommended <b>{expected_san}</b>)."
                self.coach_message = f"⚠️ <b>{self.last_quality}: {san}</b><br>{blunder_reason}"
                self.coach_tip = "Opponent responds with Stockfish:"
                self._reply_with_engine()
        else:
            self.last_quality = "Free Play"
            self.coach_message = f"You played <b>{san}</b>."
            self._reply_with_engine()

        self.update_analysis()
        if self.mode == "lesson":
            if self.step_index < len(current_moves):
                exp_uci = current_moves[self.step_index].get("expected_uci")
                if exp_uci:
                    self.arrows = [{"from": exp_uci[:2], "to": exp_uci[2:4], "color": "green"}]
        elif not self.board.is_game_over():
            active_m = self.top_moves if self.board.turn == chess.BLACK else self.white_top_moves
            if active_m:
                best_m = active_m[0]
                self.arrows = [{"from": best_m["from"], "to": best_m["to"], "color": "green"}]

        return self.get_state()

    def _reply_with_engine(self):
        engine_path = find_stockfish()
        if not engine_path or not os.path.exists(engine_path) or self.board.is_game_over():
            return
        try:
            eng = chess.engine.SimpleEngine.popen_uci(engine_path)
            res = eng.play(self.board, chess.engine.Limit(time=0.25))
            eng.quit()
            if res.move:
                bot_san = self.board.san(res.move)
                self.board.push(res.move)
                self.history.append(bot_san)
                self.coach_message += f"<br>🤖 Opponent replies: <b>{bot_san}</b>"
        except Exception as e:
            print(f"Engine reply error: {e}")

    def get_hint(self):
        self.update_analysis()
        active_moves = self.top_moves if self.board.turn == chess.BLACK else self.white_top_moves
        if not active_moves:
            return {"error": "No legal moves available."}

        best = active_moves[0]
        self.arrows = [{"from": best["from"], "to": best["to"], "color": "green"}]
        self.highlights = [best["from"], best["to"]]

        side_name = "Black" if self.board.turn == chess.BLACK else "White"
        explanation = f"💡 <b>Best Move for {side_name}: {best['san']}</b> (Stockfish 18: <b>{best['eval']}</b>)<br>{best['name']}.<br><span class='text-slate-400'>Expected Line: {best['pv']}</span>"
        self.coach_tip = f"Play <b>{best['san']}</b> on the board!"

        return {
            "best_san": best["san"],
            "best_uci": best["uci"],
            "from": best["from"],
            "to": best["to"],
            "eval": best["eval"],
            "explanation": explanation,
            "arrows": self.arrows
        }

    def get_threat(self):
        if self.board.is_game_over():
            return {"error": "Game is over."}
        if self.board.is_check():
            return {
                "threat_san": "Check!",
                "explanation": "You are in check — dealing with check is the immediate priority!",
                "arrows": []
            }

        fields = self.board.fen().split(' ')
        fields[1] = 'w' if fields[1] == 'b' else 'b'
        fields[3] = '-'
        flipped_fen = ' '.join(fields)

        try:
            flipped_board = chess.Board(flipped_fen)
        except Exception:
            return {"error": "Cannot probe threat in this position."}

        opp_moves, _ = analyze_with_stockfish(flipped_board, depth=12, multipv=1, time_limit=0.25)
        if not opp_moves:
            return {"error": "No opponent threats found."}

        threat = opp_moves[0]
        self.arrows = [{"from": threat["from"], "to": threat["to"], "color": "violet"}]
        opp_color = "White" if self.board.turn == chess.BLACK else "Black"
        explanation = f"⚠️ <b>Opponent Threat:</b> If you pass, {opp_color} will play <b>{threat['san']}</b> ({threat['name']}).<br><span class='text-slate-400'>Threat Line: {threat['pv']}</span>"
        self.coach_tip = f"Watch out for {opp_color}'s <b>{threat['san']}</b> idea!"

        return {
            "threat_san": threat["san"],
            "threat_uci": threat["uci"],
            "from": threat["from"],
            "to": threat["to"],
            "eval": threat["eval"],
            "explanation": explanation,
            "arrows": self.arrows
        }

    def takeback(self):
        if len(self.history) >= 1:
            self.board.pop()
            self.history.pop()
            if self.mode == "lesson" and len(self.history) >= 1 and self.board.turn == chess.WHITE:
                self.board.pop()
                self.history.pop()
                if self.step_index > 0:
                    self.step_index -= 1
            self.coach_message = f"↩️ <b>Takeback:</b> Back to move {len(self.history)}."
            self.coach_tip = "Make your move or select from candidate moves!"
        self.update_analysis()
        active = self.top_moves if self.board.turn == chess.BLACK else self.white_top_moves
        if active:
            best = active[0]
            self.arrows = [{"from": best["from"], "to": best["to"], "color": "green"}]
        return self.get_state()

    def get_state(self):
        lesson = get_lesson(self.lesson_id)
        current_step = None
        moves = lesson.get("moves", [])
        if self.step_index < len(moves):
            current_step = moves[self.step_index]

        return {
            "fen": self.board.fen(),
            "turn": "white" if self.board.turn == chess.WHITE else "black",
            "history": self.history,
            "mode": self.mode,
            "lesson_id": self.lesson_id,
            "lesson_name": lesson.get("name", "Scandinavian Lesson"),
            "lesson_subtitle": lesson.get("subtitle", ""),
            "step_index": self.step_index,
            "total_steps": len(moves),
            "coach_message": self.coach_message,
            "coach_tip": self.coach_tip,
            "last_quality": self.last_quality,
            "expected_move": current_step.get("expected_san") if (current_step and self.mode == "lesson") else (self.top_moves[0]["san"] if self.top_moves else None),
            "arrows": self.arrows,
            "highlights": self.highlights,
            "orientation": "white" if (self.mode == "explore_center" or (self.mode == "lesson" and lesson.get("side") == "white")) else "black",
            "golden_rules": GOLDEN_RULES,
            "lessons_list": list_lessons(),
            "top_moves": self.top_moves,
            "white_top_moves": self.white_top_moves,
            "engine_eval": self.engine_eval,
            "blunder_puzzles": list_blunder_puzzles(),
            "active_blunder_id": self.blunder_puzzle_id,
            "blunder_score": self.blunder_score,
            "gm_games": list_gm_games(),
            "active_gm_id": self.gm_game_id,
            "gm_score": self.gm_score,
            "pawn_guide": get_pawn_guide()
        }

session = ScandinavianMentorSession()
