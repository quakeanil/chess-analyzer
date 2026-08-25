"""
Stockfish 18 Engine Analyzer for Chess Games
Provides deep move-by-move evaluations, blunder detection, and best move recommendations.
"""
import os
import shutil
import glob
import chess
import chess.engine

def find_stockfish():
    """Locates the Stockfish binary on the system."""
    # 1. Check if stockfish is in PATH
    path = shutil.which("stockfish") or shutil.which("stockfish.exe")
    if path and os.path.exists(path):
        return path
        
    # 2. Check WinGet Packages directory
    winget_pattern = os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Packages\*Stockfish*/**/stockfish*.exe")
    matches = glob.glob(winget_pattern, recursive=True)
    if matches:
        return matches[0]
        
    # 3. Check Program Files
    prog_pattern = r"C:\Program Files\**\stockfish*.exe"
    matches = glob.glob(prog_pattern, recursive=True)
    if matches:
        return matches[0]
        
    # 4. Check local project directory
    local_bin = os.path.join(os.path.dirname(__file__), "..", "bin", "stockfish.exe")
    if os.path.exists(local_bin):
        return local_bin

    return None

def score_to_str(score_obj, is_white_perspective=True):
    """Converts a chess.engine Score object to a human-readable string like +1.5 or #2 (mate)."""
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
    """Returns numerical score in centipawns for blunder math."""
    if score_obj is None:
        return 0
    score = score_obj.white() if is_white_perspective else score_obj.black()
    if score.is_mate():
        return 10000 if score.mate() > 0 else -10000
    return score.score() or 0

def analyze_game_with_stockfish(game_summary, engine_path, depth=12):
    """
    Runs Stockfish analysis across all moves of a game.
    Attaches move-by-move evaluations, quality tags, and engine best moves.
    """
    if not engine_path or not os.path.exists(engine_path):
        return game_summary

    try:
        engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    except Exception as e:
        print(f"Failed to start Stockfish: {e}")
        return game_summary

    board = chess.Board()
    moves_san = game_summary.get("moves_san", [])
    my_color = game_summary.get("color", "White")
    is_my_turn_first = (my_color == "White")

    analysis_per_ply = []
    
    # Analyze start position
    start_info = engine.analyse(board, chess.engine.Limit(depth=depth))
    prev_score = start_info.get("score")
    
    for i, san_move in enumerate(moves_san):
        is_my_move = (i % 2 == 0 if is_my_turn_first else i % 2 == 1)
        move_num = (i // 2) + 1
        
        # Best move before playing
        best_move_obj = None
        pv_san_list = []
        try:
            info_before = engine.analyse(board, chess.engine.Limit(depth=depth))
            if "pv" in info_before and len(info_before["pv"]) > 0:
                best_move_obj = info_before["pv"][0]
                # Extract PV line in SAN
                temp_board = board.copy()
                for pv_m in info_before["pv"][:5]:
                    pv_san_list.append(temp_board.san(pv_m))
                    temp_board.push(pv_m)
        except Exception:
            pass

        best_move_san = board.san(best_move_obj) if best_move_obj else san_move
        eval_before_str = score_to_str(prev_score, is_white_perspective=True)
        eval_before_cp = score_to_cp(prev_score, is_white_perspective=(i % 2 == 0))

        # Push the actual played move
        try:
            actual_move_obj = board.parse_san(san_move)
            board.push(actual_move_obj)
        except Exception:
            break

        # Eval after move
        try:
            info_after = engine.analyse(board, chess.engine.Limit(depth=depth))
            cur_score = info_after.get("score")
            eval_after_str = score_to_str(cur_score, is_white_perspective=True)
            eval_after_cp = score_to_cp(cur_score, is_white_perspective=(i % 2 == 0))
            prev_score = cur_score
        except Exception:
            eval_after_str = eval_before_str
            eval_after_cp = eval_before_cp

        # Calculate eval loss for the player who just moved
        cp_diff = eval_before_cp - eval_after_cp
        
        # Classify move quality
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
            "best_san": best_move_san,
            "eval_str": eval_after_str,
            "eval_loss_cp": cp_diff,
            "quality": quality,
            "badge": badge,
            "pv_san": " ".join(pv_san_list)
        })

    try:
        engine.quit()
    except Exception:
        pass

    game_summary["stockfish_analysis"] = analysis_per_ply
    return game_summary
