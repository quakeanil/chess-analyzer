import json
import io
import chess.pgn
from collections import defaultdict

with open('C:/Users/okanil/Documents/Projects/chess-analyzer/data/0kanil_games_cache.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

games = data.get('games', [])
stats_white = defaultdict(lambda: {'wins': 0, 'losses': 0, 'draws': 0, 'moves_samples': []})
stats_black = defaultdict(lambda: {'wins': 0, 'losses': 0, 'draws': 0, 'moves_samples': []})

for g in games:
    pgn_str = g.get('pgn')
    if not pgn_str: continue
    w = g.get('white', {}).get('username', '').lower()
    b = g.get('black', {}).get('username', '').lower()
    is_w = (w == '0kanil')
    is_b = (b == '0kanil')
    if not is_w and not is_b: continue
    
    my_data = g.get('white') if is_w else g.get('black')
    result = my_data.get('result')
    
    pgn_io = io.StringIO(pgn_str)
    try:
        game = chess.pgn.read_game(pgn_io)
    except: continue
    if not game: continue
    
    eco = game.headers.get('ECO', 'A00')
    eco_url = game.headers.get('ECOUrl', '')
    if eco_url:
        op_name = eco_url.split('/')[-1].replace('-', ' ').title()
    else:
        op_name = game.headers.get('Opening', eco)
    
    key = f'[{eco}] {op_name}'
    target = stats_white if is_w else stats_black
    if result == 'win': target[key]['wins'] += 1
    elif result in ['checkmated', 'resigned', 'timeout', 'abandoned', 'lose']: target[key]['losses'] += 1
    else: target[key]['draws'] += 1
    
    # store first 10 moves
    board = game.board()
    moves_san = []
    for mv in list(game.mainline_moves())[:10]:
        moves_san.append(board.san(mv))
        board.push(mv)
    if len(target[key]['moves_samples']) < 3:
        target[key]['moves_samples'].append(moves_san)

def get_top_tables(stats_dict, min_games=5):
    res = []
    for op, d in stats_dict.items():
        tot = d['wins'] + d['losses'] + d['draws']
        if tot >= min_games:
            w_pct = round(d['wins']/tot*100, 1)
            l_pct = round(d['losses']/tot*100, 1)
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

w_win, w_loss = get_top_tables(stats_white, min_games=5)
b_win, b_loss = get_top_tables(stats_black, min_games=5)

print('=== TOP 10 WINNING OPENINGS AS WHITE ===')
for i, x in enumerate(w_win, 1):
    print(f"{i:2d}. {x['op'][:50]:<50} | Games: {x['total']:2d} | Win: {x['win_rate']:5.1f}% | Loss: {x['loss_rate']:5.1f}%")

print('\n=== TOP 10 LOSING OPENINGS AS WHITE ===')
for i, x in enumerate(w_loss, 1):
    print(f"{i:2d}. {x['op'][:50]:<50} | Games: {x['total']:2d} | Loss: {x['loss_rate']:5.1f}% | Win: {x['win_rate']:5.1f}%")

print('\n=== TOP 10 WINNING OPENINGS AS BLACK ===')
for i, x in enumerate(b_win, 1):
    print(f"{i:2d}. {x['op'][:50]:<50} | Games: {x['total']:2d} | Win: {x['win_rate']:5.1f}% | Loss: {x['loss_rate']:5.1f}%")

print('\n=== TOP 10 LOSING OPENINGS AS BLACK ===')
for i, x in enumerate(b_loss, 1):
    print(f"{i:2d}. {x['op'][:50]:<50} | Games: {x['total']:2d} | Loss: {x['loss_rate']:5.1f}% | Win: {x['win_rate']:5.1f}%")

# Save structured json for dashboard integration
with open('C:/Users/okanil/Documents/Projects/chess-analyzer/data/top_openings.json', 'w', encoding='utf-8') as f:
    json.dump({
        'white_winning': w_win,
        'white_losing': w_loss,
        'black_winning': b_win,
        'black_losing': b_loss
    }, f, indent=2)
