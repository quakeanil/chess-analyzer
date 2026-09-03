"""
Dynamic Top Openings Generator for Chess Diagnostics
Calculates top winning and losing openings for White and Black.
"""
import json
import io
import os
import chess.pgn
from collections import defaultdict

def generate_top_openings(games, username="0kanil", output_path=None, min_games=5):
    stats_white = defaultdict(lambda: {'wins': 0, 'losses': 0, 'draws': 0, 'moves_samples': []})
    stats_black = defaultdict(lambda: {'wins': 0, 'losses': 0, 'draws': 0, 'moves_samples': []})
    u_lower = username.lower()

    for g in games:
        pgn_str = g.get('pgn')
        if not pgn_str:
            continue
        w = g.get('white', {}).get('username', '').lower()
        b = g.get('black', {}).get('username', '').lower()
        is_w = (w == u_lower)
        is_b = (b == u_lower)
        if not is_w and not is_b:
            continue
        
        my_data = g.get('white') if is_w else g.get('black')
        result = my_data.get('result')
        
        pgn_io = io.StringIO(pgn_str)
        try:
            game = chess.pgn.read_game(pgn_io)
        except Exception:
            continue
        if not game:
            continue
        
        eco = game.headers.get('ECO', 'A00')
        eco_url = game.headers.get('ECOUrl', '')
        if eco_url:
            op_name = eco_url.split('/')[-1].replace('-', ' ').title()
        else:
            op_name = game.headers.get('Opening', eco)
        
        key = f'[{eco}] {op_name}'
        target = stats_white if is_w else stats_black
        if result == 'win':
            target[key]['wins'] += 1
        elif result in ['checkmated', 'resigned', 'timeout', 'abandoned', 'lose']:
            target[key]['losses'] += 1
        else:
            target[key]['draws'] += 1
        
        # store first 10 moves
        board = game.board()
        moves_san = []
        for mv in list(game.mainline_moves())[:10]:
            moves_san.append(board.san(mv))
            board.push(mv)
        if len(target[key]['moves_samples']) < 3:
            target[key]['moves_samples'].append(moves_san)

    def get_top_tables(stats_dict, min_g=min_games):
        res = []
        for op, d in stats_dict.items():
            tot = d['wins'] + d['losses'] + d['draws']
            if tot >= min_g:
                w_pct = round(d['wins'] / tot * 100, 1)
                l_pct = round(d['losses'] / tot * 100, 1)
                res.append({
                    'op': op,
                    'total': tot,
                    'wins': d['wins'],
                    'losses': d['losses'],
                    'draws': d['draws'],
                    'win_rate': w_pct,
                    'loss_rate': l_pct,
                    'samples': d['moves_samples']
                })
        
        top_win = sorted(res, key=lambda x: (x['win_rate'], x['total']), reverse=True)[:10]
        top_loss = sorted(res, key=lambda x: (x['loss_rate'], x['total']), reverse=True)[:10]
        return top_win, top_loss

    w_win, w_loss = get_top_tables(stats_white, min_games)
    b_win, b_loss = get_top_tables(stats_black, min_games)

    result_data = {
        'white_winning': w_win,
        'white_losing': w_loss,
        'black_winning': b_win,
        'black_losing': b_loss
    }

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2)

    return result_data

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cache_path = os.path.join(base_dir, "data", "0kanil_games_cache.json")
    out_path = os.path.join(base_dir, "data", "top_openings.json")
    
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            cache_data = json.load(f)
        games_list = cache_data.get("games", [])
        data = generate_top_openings(games_list, username="0kanil", output_path=out_path)
        
        print('=== TOP 10 WINNING OPENINGS AS WHITE ===')
        for i, x in enumerate(data['white_winning'], 1):
            print(f"{i:2d}. {x['op'][:50]:<50} | Games: {x['total']:2d} | Win: {x['win_rate']:5.1f}% | Loss: {x['loss_rate']:5.1f}%")

        print('\n=== TOP 10 LOSING OPENINGS AS WHITE ===')
        for i, x in enumerate(data['white_losing'], 1):
            print(f"{i:2d}. {x['op'][:50]:<50} | Games: {x['total']:2d} | Loss: {x['loss_rate']:5.1f}% | Win: {x['win_rate']:5.1f}%")

        print('\n=== TOP 10 WINNING OPENINGS AS BLACK ===')
        for i, x in enumerate(data['black_winning'], 1):
            print(f"{i:2d}. {x['op'][:50]:<50} | Games: {x['total']:2d} | Win: {x['win_rate']:5.1f}% | Loss: {x['loss_rate']:5.1f}%")

        print('\n=== TOP 10 LOSING OPENINGS AS BLACK ===')
        for i, x in enumerate(data['black_losing'], 1):
            print(f"{i:2d}. {x['op'][:50]:<50} | Games: {x['total']:2d} | Loss: {x['loss_rate']:5.1f}% | Win: {x['win_rate']:5.1f}%")
