"""
Stockfish 18 Engine Analyzer for Chess Games
Provides deep move-by-move evaluations, blunder detection, UCI coordinates for arrows, and best move recommendations.
"""
import os
import shutil
import glob
import chess
import chess.engine

def find_stockfish():
    """Locates the Stockfish binary on the system."""
    path = shutil.which("stockfish") or shutil.which("stockfish.exe")
    if path and os.path.exists(path):
        return path
        
    winget_pattern = os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Packages\*Stockfish*/**/stockfish*.exe")
    matches = glob.glob(winget_pattern, recursive=True)
    if matches:
        return matches[0]
        
    prog_pattern = r"C:\Program Files\**\stockfish*.exe"
    matches = glob.glob(prog_pattern, recursive=True)
    if matches:
        return matches[0]
        
    local_bin = os.path.join(os.path.dirname(__file__), "..", "bin", "stockfish.exe")
    if os.path.exists(local_bin):
        return local_bin

    return None

def score_to_str(score_obj, is_white_perspective=True):
    if score_obj is None:
        return "0.0"
    
    score = score_obj.white() if is_white_perspective else score_obj.black()
    
    if score.is_mate():
        mate_moves = score.mate()
        if mate_moves > 0:
            return f"+M{mate_moves}"
        else:
            return f"-M{abs(mate_moves)}"
            
    cp = score.score()
    if cp is None:
        return "0.0"
        
    val = cp / 100.0
    return f"{val:+.1f}"

def score_to_cp(score_obj, is_white_perspective=True):
    if score_obj is None:
        return 0
    score = score_obj.white() if is_white_perspective else score_obj.black()
    if score.is_mate():
        return 10000 if score.mate() > 0 else -10000
    return score.score() or 0

def analyze_game_with_stockfish(game_summary, engine_or_path, depth=10):
    if not engine_or_path:
        return game_summary

    close_when_done = False
    if isinstance(engine_or_path, chess.engine.SimpleEngine):
        engine = engine_or_path
    elif isinstance(engine_or_path, str) and os.path.exists(engine_or_path):
        try:
            engine = chess.engine.SimpleEngine.popen_uci(engine_or_path)
            close_when_done = True
        except Exception as e:
            print(f"Failed to start Stockfish: {e}")
            return game_summary
    else:
        return game_summary

    board = chess.Board()
    moves_san = game_summary.get("moves_san", [])
    my_color = game_summary.get("color", "White")
    is_my_turn_first = (my_color == "White")

    analysis_per_ply = []
    
    try:
        cur_info = engine.analyse(board, chess.engine.Limit(depth=depth))
    except Exception:
        cur_info = {}
    cur_score = cur_info.get("score")
    
    for i, san_move in enumerate(moves_san):
        is_my_move = (i % 2 == 0 if is_my_turn_first else i % 2 == 1)
        move_num = (i // 2) + 1
        
        best_move_obj = None
        pv_san_list = []
        if "pv" in cur_info and len(cur_info["pv"]) > 0:
            best_move_obj = cur_info["pv"][0]
            temp_board = board.copy()
            for pv_m in cur_info["pv"][:5]:
                pv_san_list.append(temp_board.san(pv_m))
                temp_board.push(pv_m)

        best_move_san = board.san(best_move_obj) if best_move_obj else san_move
        best_uci = best_move_obj.uci() if best_move_obj else None
        
        eval_before_str = score_to_str(cur_score, is_white_perspective=True)
        eval_before_cp = score_to_cp(cur_score, is_white_perspective=(i % 2 == 0))

        try:
            actual_move_obj = board.parse_san(san_move)
            played_uci = actual_move_obj.uci()
            board.push(actual_move_obj)
        except Exception:
            break

        try:
            cur_info = engine.analyse(board, chess.engine.Limit(depth=depth))
            cur_score = cur_info.get("score")
            eval_after_str = score_to_str(cur_score, is_white_perspective=True)
            eval_after_cp = score_to_cp(cur_score, is_white_perspective=(i % 2 == 0))
        except Exception:
            eval_after_str = eval_before_str
            eval_after_cp = eval_before_cp

        cp_diff = eval_before_cp - eval_after_cp
        
        if cp_diff <= 15:
            quality = "Best Move"
            badge = "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
        elif cp_diff <= 50:
            quality = "Good"
            badge = "bg-sky-500/20 text-sky-400 border-sky-500/30"
        elif cp_diff <= 150:
            quality = "Inaccuracy"
            badge = "bg-amber-500/20 text-amber-400 border-amber-500/30"
        elif cp_diff <= 300:
            quality = "Mistake"
            badge = "bg-orange-500/20 text-orange-400 border-orange-500/30"
        else:
            quality = "Blunder"
            badge = "bg-rose-500/20 text-rose-400 border-rose-500/30"

        analysis_per_ply.append({
            "ply": i + 1,
            "move_num": move_num,
            "is_my_move": is_my_move,
            "played_san": san_move,
            "played_uci": played_uci,
            "best_san": best_move_san,
            "best_uci": best_uci,
            "eval_str": eval_after_str,
            "eval_loss_cp": cp_diff,
            "quality": quality,
            "badge": badge,
            "pv_san": " ".join(pv_san_list)
        })

    if close_when_done:
        try:
            engine.quit()
        except Exception:
            pass

    game_summary["stockfish_analysis"] = analysis_per_ply
    return game_summary
