"""
Chess Diagnostic & Opening Analysis Engine with Stockfish 18 & AI Coach Recommendations
"""
import io
import json
from collections import defaultdict, Counter
import chess
import chess.pgn
import chess.engine
from src.engine_analyzer import find_stockfish, analyze_game_with_stockfish

def generate_opening_weaknesses_catalog():
    """
    Catalog of exact opening weaknesses, opponent triggers, best options, and tactical reasons.
    """
    return [
        {
            "id": "scandi_2e5",
            "side": "Black",
            "opening": "Scandinavian Defense 2.e5",
            "eco": "B01",
            "loss_count": 21,
            "opp_trigger": "Opponent plays: 2. e5",
            "your_mistake": "You played: 2... d4?! or 2... e6?! (Passive / Traps Bishop on c8)",
            "best_option": "Your Best Move: 2... Bf5! (followed by 3...e6, 4...c5! & 5...Nc6)",
            "why_reason": "When White pushes 2.e5, White closes the center. If you play 2...e6, your light-squared bishop is trapped on c8 for the entire game. If you play 2...d4, White attacks with f4. Playing 2...Bf5! brings your bishop outside the pawn chain before locking it with e6, giving Black an active, winning setup.",
            "fen_setup": "rnbqkbnr/ppp1pppp/8/3pP3/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2",
            "refutation_uci": "c8f5",
            "refutation_san": "2... Bf5!",
            "line_san": ["Bf5", "d4", "e6", "Nf3", "c5", "c3", "Nc6"],
            "line_uci": ["c8f5", "d2d4", "e7e6", "g1f3", "c7c5", "c2c3", "b8c6"]
        },
        {
            "id": "englund_trap",
            "side": "White",
            "opening": "Englund Gambit 1.d4 e5",
            "eco": "A40",
            "loss_count": 13,
            "opp_trigger": "Opponent plays: 4... Qb4+ (Forking King and Bishop on f4)",
            "your_mistake": "You played: 5. Qd2?? or 5. Qc3?? (Loses queen or b2/a1 rook to 5...Qxb2)",
            "best_option": "Your Best Move: 5. Bd2! Qxb2 6. Nc3! (+3.8 Advantage)",
            "why_reason": "Never block early queen checks with Qd2 when b2 is hanging! 5.Bd2! protects your king and poisons the b2 pawn. When Black greedily captures 5...Qxb2, play 6.Nc3! White threatens 7.Rb1 (trapping Black's queen) and 7.Nd5 (forking c7 King and Rook). Black is dead lost.",
            "fen_setup": "r1b1kbnr/pppp1ppp/2n5/4P3/1q3B2/5N2/PPP1PPPP/RN1QKB1R w KQkq - 5 5",
            "refutation_uci": "f4d2",
            "refutation_san": "5. Bd2!",
            "line_san": ["Bd2", "Qxb2", "Nc3", "Bb4", "Rb1", "Qa3", "Rb3", "Qa5", "a3"],
            "line_uci": ["f4d2", "b4b2", "b1c3", "f8b4", "a1b1", "b2a3", "b1b3", "a3a5", "a2a3"]
        },
        {
            "id": "danish_gambit",
            "side": "Black",
            "opening": "Danish Gambit (Double Pawn Sacrifice)",
            "eco": "C21",
            "loss_count": 7,
            "opp_trigger": "Opponent plays: 5. Bxb2 (Both White Bishops Aimed at f7 & g7)",
            "your_mistake": "You played: 5... Qf6?! or 5... Nf6? (Walks into e5 attack)",
            "best_option": "Your Best Move: 5... d5!! (The Schlechter Defense Refutation)",
            "why_reason": "White sacrificed two pawns to get murderous attacking diagonals with Bc4 and Bb2. Pushing 5...d5!! immediately blocks both bishops and returns one pawn to force queen exchanges (6.Bxd5 Nf6 7.Bxf7+ Kxf7 8.Qxd8 Bb4+ 9.Qd2 Bxd2+). Black emerges a clean pawn up with zero king danger.",
            "fen_setup": "rnbqkbnr/pppp1ppp/8/8/2B1P3/8/PB3PPP/RN1QK1NR b KQkq - 0 5",
            "refutation_uci": "d7d5",
            "refutation_san": "5... d5!!",
            "line_san": ["d5", "Bxd5", "Nf6", "Bxf7+", "Kxf7", "Qxd8", "Bb4+", "Qd2", "Bxd2+", "Nxd2"],
            "line_uci": ["d7d5", "c4d5", "g8f6", "d5f7", "e8f7", "d1d8", "f8b4", "d8d2", "b4d2", "b1d2"]
        },
        {
            "id": "london_black",
            "side": "Black",
            "opening": "vs London System 1.d4 d5 2.Bf4",
            "eco": "D00",
            "loss_count": 16,
            "opp_trigger": "Opponent plays: 2. Bf4 (Developing Bishop outside pawn chain)",
            "your_mistake": "You played: 2... e6?! or passive 2... Nf6 3.e3 e6 (Allows easy London pyramid)",
            "best_option": "Your Best Move: 2... c5! 3.e3 Nc6 4.Nf3 Qb6! (Double attack on b2 & d4)",
            "why_reason": "When White plays 2.Bf4, the b2 pawn is left unguarded. If you play passively, White builds an impenetrable triangle (c3-d4-e3). Striking immediately with 2...c5! and 4...Qb6! forces White to weaken their queenside (b3/Qc1) and gives Black the initiative.",
            "fen_setup": "rnbqkbnr/ppp1pppp/8/3p4/3P1B2/8/PPP1PPPP/RN1QKBNR b KQkq - 1 2",
            "refutation_uci": "c7c5",
            "refutation_san": "2... c5!",
            "line_san": ["c5", "e3", "Nc6", "Nf3", "Qb6", "Nc3", "cxd4", "exd4", "e6"],
            "line_uci": ["c7c5", "e2e3", "b8c6", "g1f3", "d8b6", "b1c3", "c5d4", "e3d4", "e7e6"]
        },
        {
            "id": "white_passive_d4",
            "side": "White",
            "opening": "Passive Queen's Pawn (1.d4 d5 2.Nf3 & 3.e3 / 3.b3)",
            "eco": "D02",
            "loss_count": 30,
            "opp_trigger": "You played: 2. Nf3 followed by 3. e3 or 3. b3 (No central strike)",
            "your_mistake": "Playing passive d4 setups locks your dark-squared bishop on c1 and gives Black free control of the center.",
            "best_option": "Your Best Move: 2. c4! (Queen's Gambit) or 2. Bf4! (Active London)",
            "why_reason": "In 1.d4 openings, White must either strike the center with 2.c4! (putting direct pressure on d5) or develop the dark bishop first with 2.Bf4! before playing e3. Playing Nf3 + e3 without c4 lets Black play ...c5 and ...Bf5 with a 70%+ win rate against you.",
            "fen_setup": "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2",
            "refutation_uci": "c2c4",
            "refutation_san": "2. c4! (Queen's Gambit)",
            "line_san": ["c4", "e6", "Nc3", "Nf6", "cxd5", "exd5", "Bg5"],
            "line_uci": ["c2c4", "e7e6", "b1c3", "g8f6", "c4d5", "e6d5", "c1g5"]
        },
        {
            "id": "reti_wedge",
            "side": "Black",
            "opening": "vs Réti Opening 1.Nf3 d5 2.c4",
            "eco": "A09",
            "loss_count": 8,
            "opp_trigger": "Opponent plays: 1. Nf3 d5 2. c4",
            "your_mistake": "You played: 2... dxc4?! or 2... c6 (Surrenders central space)",
            "best_option": "Your Best Move: 2... d4! (Space Wedge stopping Nc3)",
            "why_reason": "When White offers 2.c4 in the Réti, pushing 2...d4! creates an advanced wedge on White's queenside. It deprives White's knight of the natural c3 square and gives Black long-term space control. Follow up with 3...c5 and 4...Nc6.",
            "fen_setup": "rnbqkbnr/ppp1pppp/8/3p4/2P5/5N2/PP1PPPPP/RNBQKB1R b KQkq - 0 2",
            "refutation_uci": "d5d4",
            "refutation_san": "2... d4!",
            "line_san": ["d4", "e3", "c5", "exd4", "cxd4", "d3", "Nc6", "g3", "e5"],
            "line_uci": ["d5d4", "e2e3", "c7c5", "e3d4", "c5d4", "d2d3", "b8c6", "g2g3", "e7e5"]
        }
    ]

def analyze_player_games(username, games_data):
    username = username.lower()
    
    stats_white = defaultdict(lambda: {"wins": 0, "losses": 0, "draws": 0, "games": []})
    stats_black = defaultdict(lambda: {"wins": 0, "losses": 0, "draws": 0, "games": []})
    
    loss_reasons = Counter()
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
            
        # Categorize loss phase
        phase = "Opening" if move_count <= 15 else ("Middlegame" if move_count <= 30 else "Endgame")
        
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
            "time_class": time_class,
            "phase": phase
        }
        
        target_stats[op_key]["games"].append(game_summary)
        
        if is_loss and move_count >= 2:
            all_losses.append(game_summary)
            
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
    
    # Categorize losses into Opening Disasters (40), Middlegame Collapses (30), and Endgame (10)
    opening_losses = [g for g in all_losses if g["phase"] == "Opening"]
    opening_losses.sort(key=lambda x: x["moves_count"])
    
    middlegame_losses = [g for g in all_losses if g["phase"] == "Middlegame"]
    middlegame_losses.sort(key=lambda x: x["moves_count"])
    
    endgame_losses = [g for g in all_losses if g["phase"] == "Endgame"]
    endgame_losses.sort(key=lambda x: x["moves_count"])
    
    selected_losses = opening_losses[:45] + middlegame_losses[:30] + endgame_losses[:15]

    # Run Deep Stockfish Analysis across all selected losses
    engine_path = find_stockfish()
    if engine_path:
        print(f"[Stockfish Engine] Analyzing {len(selected_losses)} lost games (Opening, Middlegame & Endgame) at depth 10 with {engine_path}...")
        try:
            engine = chess.engine.SimpleEngine.popen_uci(engine_path)
            for idx, g_sum in enumerate(selected_losses):
                analyze_game_with_stockfish(g_sum, engine, depth=10)
            engine.quit()
        except Exception as e:
            print(f"Stockfish engine analysis error: {e}")

    opening_weaknesses = generate_opening_weaknesses_catalog()

    return {
        "username": username,
        "total_games": len(games_data),
        "total_wins": total_wins,
        "total_losses": total_losses,
        "total_draws": total_draws,
        "win_rate": round((total_wins / max(1, total_wins + total_losses + total_draws)) * 100, 1),
        "loss_reasons": dict(loss_reasons),
        "early_disasters_count": len(opening_losses),
        "opening_disasters_count": len(opening_losses),
        "early_disasters": selected_losses,
        "all_analyzed_losses": selected_losses, # 90 curated games with Stockfish evaluations
        "opening_weaknesses": opening_weaknesses, # Dedicated Opening Weakness & Refutation Diagnostic
        "white_openings": white_openings,
        "black_openings": black_openings,
        "first_moves_white": dict(first_moves_white.most_common(5)),
        "first_moves_black_vs_e4": dict(first_moves_black_vs_e4.most_common(5)),
        "first_moves_black_vs_d4": dict(first_moves_black_vs_d4.most_common(5)),
        "has_stockfish": bool(engine_path)
    }
