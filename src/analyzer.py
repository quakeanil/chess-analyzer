"""
Chess Diagnostic & Opening Analysis Engine
"""
import io
import json
from collections import defaultdict, Counter
import chess
import chess.pgn

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
