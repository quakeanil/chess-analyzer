"""
Chess Diagnostic & Opening Analysis Engine with AI Coach Recommendations
"""
import io
import json
from collections import defaultdict, Counter
import chess
import chess.pgn

def generate_coach_advice(game_summary):
    """
    Analyzes a lost game and returns specific move-level recommendations:
    - critical_ply: which half-move went wrong
    - played_move: the inaccuracy/blunder played
    - better_move: what to play instead
    - never_rule: clear 'NEVER DO THAT' rule
    - explanation: why the better move works
    """
    moves = game_summary["moves_san"]
    color = game_summary["color"]
    opening = game_summary["opening"]
    
    # 1. Englund Gambit (White)
    if color == "White" and len(moves) >= 2 and moves[0] == "d4" and moves[1] == "e5":
        for i, m in enumerate(moves):
            if i % 2 == 0: # White's move
                move_num = (i // 2) + 1
                if move_num in [4, 5] and ("Qd2" in m or "Qc3" in m or "Bd2" not in m):
                    return {
                        "critical_ply": i + 1,
                        "move_num": move_num,
                        "played_move": f"{move_num}. {m}",
                        "better_move": f"{move_num}. Bd2! (followed by 6. Nc3!)",
                        "never_rule": "NEVER block an early Queen check with Qd2 or leave your b2 pawn unprotected!",
                        "explanation": "When Black plays 4...Qb4+, play 5.Bd2! Qxb2 6.Nc3! (or 6.Bc3 Bb4 7.Qd2!). White threatens 7.Rb1 or 7.Nd5 with a deadly double attack on c7 and Black's queen (+3.5 eval)."
                    }
                    
    # 2. Scandinavian 2.e5 (Black)
    if color == "Black" and len(moves) >= 3 and moves[0] == "e4" and moves[1] == "d5" and moves[2] == "e5":
        if len(moves) >= 4 and moves[3] != "Bf5":
            return {
                "critical_ply": 4,
                "move_num": 2,
                "played_move": f"2... {moves[3]}",
                "better_move": "2... Bf5!",
                "never_rule": "NEVER play 2...e6 before developing your light-squared bishop outside the pawn chain!",
                "explanation": "Playing 2...e6 traps your bishop on c8 for the rest of the game. Playing 2...Bf5! first gives you an active French Defense setup with no bad pieces."
            }

    # 3. vs London System (Black)
    if color == "Black" and len(moves) >= 3 and moves[0] == "d4" and moves[1] == "d5" and moves[2] == "Bf4":
        if len(moves) >= 4 and moves[3] not in ["c5", "c6"]:
            return {
                "critical_ply": 4,
                "move_num": 2,
                "played_move": f"2... {moves[3]}",
                "better_move": "2... c5! (followed by Nc6 & Qb6!)",
                "never_rule": "NEVER play passively against the London (1.d4 d5 2.Bf4) by just developing pieces to e6 or Bd6!",
                "explanation": "White's bishop left c1, leaving the b2 pawn unguarded. Strike immediately with 2...c5! 3.e3 Nc6 4.Nf3 Qb6! to seize the initiative."
            }

    # 4. White passive d4 + Nf3 + e3 without c4/Bf4
    if color == "White" and len(moves) >= 3 and moves[0] == "d4" and moves[1] == "d5":
        if len(moves) >= 5 and moves[2] == "Nf3" and moves[4] in ["e3", "Be2"]:
            return {
                "critical_ply": 5,
                "move_num": 3,
                "played_move": f"3. {moves[4]}",
                "better_move": "2. c4! (Queen's Gambit) or 2. Bf4! (London)",
                "never_rule": "NEVER play passive d4 setups (d4 + Nf3 + e3) without challenging Black's center or developing your dark-squared bishop first!",
                "explanation": "Playing e3 locks your dark-squared bishop on c1 and gives Black free equality with ...c5 and ...Bf5."
            }

    # 5. Early Queen development trap (Moves 2-5)
    for i, m in enumerate(moves[:10]):
        is_my_turn = (color == "White" and i % 2 == 0) or (color == "Black" and i % 2 == 1)
        if is_my_turn:
            move_num = (i // 2) + 1
            if m.startswith("Q") and move_num <= 4 and "Qxd5" not in m:
                return {
                    "critical_ply": i + 1,
                    "move_num": move_num,
                    "played_move": f"{move_num}. {m}",
                    "better_move": "Develop Knights (Nf3/Nc3/Nf6) or Bishops first",
                    "never_rule": "NEVER bring your Queen out on moves 2–4 to launch premature attacks!",
                    "explanation": "Opponent will develop their minor pieces with tempo by attacking your exposed Queen, gaining free development."
                }

    # 6. Default Fallback Diagnostic for short loss
    mid_ply = min(len(moves), 6)
    crit_move = moves[mid_ply - 1] if mid_ply > 0 else "N/A"
    return {
        "critical_ply": mid_ply,
        "move_num": (mid_ply + 1) // 2,
        "played_move": f"Move {(mid_ply + 1) // 2}: {crit_move}",
        "better_move": "Prioritize rapid minor piece development & early Castling (O-O)",
        "never_rule": "NEVER move the same piece twice or delay King safety in open tactical positions!",
        "explanation": "In fast 10-15 move games, the decisive factor is almost always king safety and piece coordination. Castle within the first 7 moves."
    }

def analyze_player_games(username, games_data):
    username = username.lower()
    
    stats_white = defaultdict(lambda: {"wins": 0, "losses": 0, "draws": 0, "games": []})
    stats_black = defaultdict(lambda: {"wins": 0, "losses": 0, "draws": 0, "games": []})
    
    loss_reasons = Counter()
    early_disasters = [] # Losses <= 15 moves
    all_losses = []
    
    first_moves_white = Counter()
    first_moves_black_vs_e4 = Counter()
    first_moves_black_vs_d4 = Counter()
    
    total_wins = 0
    total_losses = 0
    total_draws = 0
    
    for g in games_data:
        pgn_str = g.get("pgn")
        if not pgn_str:
            continue
            
        white_player = g.get("white", {}).get("username", "").lower()
        black_player = g.get("black", {}).get("username", "").lower()
        is_white = (white_player == username)
        is_black = (black_player == username)
        
        if not is_white and not is_black:
            continue
            
        my_data = g.get("white") if is_white else g.get("black")
        opp_data = g.get("black") if is_white else g.get("white")
        
        result = my_data.get("result")
        time_class = g.get("time_class", "unknown")
        game_url = g.get("url", "")
        
        # Parse PGN
        pgn_io = io.StringIO(pgn_str)
        try:
            game = chess.pgn.read_game(pgn_io)
        except Exception:
            continue
            
        if not game:
            continue
            
        eco = game.headers.get("ECO", "A00")
        eco_url = game.headers.get("ECOUrl", "")
        if eco_url:
            opening_name = eco_url.split("/")[-1].replace("-", " ").title()
        else:
            opening_name = game.headers.get("Opening", eco)
            
        # Replay moves and track FEN states
        board = game.board()
        moves_san = []
        fens = [board.fen()]
        
        for mv in game.mainline_moves():
            moves_san.append(board.san(mv))
            board.push(mv)
            fens.append(board.fen())
            
        move_count = (len(moves_san) + 1) // 2
        
        is_win = (result == "win")
        is_loss = (result in ["checkmated", "resigned", "timeout", "abandoned", "lose"])
        is_draw = not is_win and not is_loss
        
        if is_win:
            total_wins += 1
        elif is_loss:
            total_losses += 1
            loss_reasons[result] += 1
        else:
            total_draws += 1
            
        # Track first moves
        if len(moves_san) >= 1:
            first_move = moves_san[0]
            if is_white:
                first_moves_white[first_move] += 1
            elif is_black:
                if first_move == "e4" and len(moves_san) >= 2:
                    first_moves_black_vs_e4[moves_san[1]] += 1
                elif first_move == "d4" and len(moves_san) >= 2:
                    first_moves_black_vs_d4[moves_san[1]] += 1
                    
        op_key = f"[{eco}] {opening_name}" if opening_name else f"[{eco}]"
        target_stats = stats_white if is_white else stats_black
        
        if is_win:
            target_stats[op_key]["wins"] += 1
        elif is_loss:
            target_stats[op_key]["losses"] += 1
        else:
            target_stats[op_key]["draws"] += 1
            
        game_summary = {
            "url": game_url,
            "eco": eco,
            "opening": opening_name,
            "moves_count": move_count,
            "moves_san": moves_san,
            "fens": fens,
            "result": result,
            "color": "White" if is_white else "Black",
            "my_rating": my_data.get("rating"),
            "opp_name": opp_data.get("username"),
            "opp_rating": opp_data.get("rating"),
            "time_class": time_class
        }
        
        target_stats[op_key]["games"].append(game_summary)
        
        if is_loss:
            all_losses.append(game_summary)
            if move_count <= 15 and move_count >= 2:
                # Attach coach advice
                game_summary["coach_advice"] = generate_coach_advice(game_summary)
                early_disasters.append(game_summary)
                
    # Sort openings
    def format_openings(stats_dict):
        res = []
        for op, data in stats_dict.items():
            tot = data["wins"] + data["losses"] + data["draws"]
            if tot >= 5:
                win_pct = round((data["wins"] / tot) * 100, 1)
                loss_pct = round((data["losses"] / tot) * 100, 1)
                res.append({
                    "opening": op,
                    "games": tot,
                    "wins": data["wins"],
                    "losses": data["losses"],
                    "draws": data["draws"],
                    "win_rate": win_pct,
                    "loss_rate": loss_pct
                })
        res.sort(key=lambda x: (x["games"] >= 10, -x["loss_rate"], x["games"]), reverse=True)
        return res

    white_openings = format_openings(stats_white)
    black_openings = format_openings(stats_black)
    
    # Sort early disasters by shortest moves first
    early_disasters.sort(key=lambda x: x["moves_count"])

    return {
        "username": username,
        "total_games": len(games_data),
        "total_wins": total_wins,
        "total_losses": total_losses,
        "total_draws": total_draws,
        "win_rate": round((total_wins / max(1, total_wins + total_losses + total_draws)) * 100, 1),
        "loss_reasons": dict(loss_reasons),
        "early_disasters_count": len(early_disasters),
        "early_disasters": early_disasters[:40], # Top 40 for interactive player
        "white_openings": white_openings,
        "black_openings": black_openings,
        "first_moves_white": dict(first_moves_white.most_common(5)),
        "first_moves_black_vs_e4": dict(first_moves_black_vs_e4.most_common(5)),
        "first_moves_black_vs_d4": dict(first_moves_black_vs_d4.most_common(5))
    }
