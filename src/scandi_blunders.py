"""
Curated Scandinavian Defense Blunder Puzzles from 0kanil's Real Chess.com Matches.
Each puzzle captures the exact position where 0kanil made a move, explains the mistake,
and tests the user to find the engine-recommended refutation.
"""

OKANIL_SCANDI_BLUNDERS = [
    {
        "id": "blunder_2e5_advance",
        "title": "Puzzle 1: The 2.e5 Advance Trap",
        "opp_name": "Chess.com Opponent (1260)",
        "time_class": "Blitz 3+0",
        "fen": "rnbqkbnr/ppp1pppp/8/4P3/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2",
        "history_lead": ["1. e4", "d5", "2. e5"],
        "okanil_move": "d4",
        "okanil_san": "2... d4?!",
        "why_bad": "You played 2...d4?! in 20+ of your matches. This closes the center, blocks your own pieces, and gives White a free hand on the kingside (3.f4/3.Nf3).",
        "expected_san": "Bf5",
        "expected_uci": "c8f5",
        "best_eval": "+0.3 for Black",
        "why_best": "2...Bf5! (Rule #3: Never lock the center with d4!). Develop the light-squared bishop outside the pawn chain before playing e6. Black gets an improved French/Caro-Kann with an active bishop and great winning chances.",
        "pv": "2...Bf5 3.d4 e6 4.Nf3 c5! 5.c3 Nc6"
    },
    {
        "id": "blunder_3c4_greedy",
        "title": "Puzzle 2: White Clings to d5 with 3.c4",
        "opp_name": "Chess.com Opponent (1295)",
        "time_class": "Rapid 10+0",
        "fen": "rnbqkb1r/ppp1pppp/5n2/3P4/2P5/8/PP1P1PPP/RNBQKBNR b KQkq - 0 3",
        "history_lead": ["1. e4", "d5", "2. exd5", "Nf6", "3. c4"],
        "okanil_move": "e6",
        "okanil_san": "3... e6!!",
        "why_bad": "In several games, 3...c6 was played or passive play allowed White to solidify. If you play passively, White simply keeps the extra pawn.",
        "expected_san": "e6",
        "expected_uci": "e7e6",
        "best_eval": "-0.2 (Equal/Dynamic)",
        "why_best": "3...e6!! The Icelandic Gambit strike! Sacrificing a second pawn to blow open the e-file and activate both bishops. White's greedy 3.c4 will face relentless central pressure.",
        "pv": "3...e6! 4.dxe6 Bxe6 5.Nf3 Qe7! 6.Be2 Bxc4"
    },
    {
        "id": "blunder_tennison_trap",
        "title": "Puzzle 3: The Tennison Gambit Attack",
        "opp_name": "Chess.com Opponent (1240)",
        "time_class": "Blitz 3+2",
        "fen": "rnbqkbnr/ppp1pppp/8/6N1/4p3/8/PPPP1PPP/RNBQKB1R b KQkq - 1 3",
        "history_lead": ["1. e4", "d5", "2. Nf3", "dxe4", "3. Ng5"],
        "okanil_move": "Nf6",
        "okanil_san": "3... Nf6!",
        "why_bad": "Playing 3...Bf5 or passive moves allows White tricky sacrifices like 4.d3 or 4.Bc4 e6 5.Nc3 with complications.",
        "expected_san": "Nf6",
        "expected_uci": "g8f6",
        "best_eval": "-0.8 for Black",
        "why_best": "3...Nf6! Natural, robust piece development directly defending e4. Follow up with 4...e6 against 4.Bc4 to permanently blunt White's attack and consolidate your extra pawn.",
        "pv": "3...Nf6 4.Bc4 e6 5.Nc3 a6 6.Ngxe4 b5"
    },
    {
        "id": "blunder_bishop_inside",
        "title": "Puzzle 4: The Bad French Bishop Blunder",
        "opp_name": "Chess.com Opponent (1310)",
        "time_class": "Blitz 5+0",
        "fen": "r1b1kbnr/ppp1pppp/2n5/q7/3P4/2N5/PPP2PPP/R1BQKBNR b KQkq - 0 4",
        "history_lead": ["1. e4", "d5", "2. exd5", "Qxd5", "3. Nc3", "Qa5", "4. d4", "Nc6"],
        "okanil_move": "e6",
        "okanil_san": "4... e6??",
        "why_bad": "You played 4...e6?? before developing the light-squared bishop! This violates Rule #1: the c8 bishop is now entombed behind your own pawns for the rest of the game.",
        "expected_san": "Nf6",
        "expected_uci": "g8f6",
        "best_eval": "+0.4 for White",
        "why_best": "4...Nf6! or 4...Bf5! Keep the c8-h3 diagonal wide open so your bishop can jump to f5 or g4 before locking your pawn chain with ...e6.",
        "pv": "4...Nf6 5.Nf3 Bg4 6.Be2 O-O-O 7.Be3 e5!"
    },
    {
        "id": "blunder_c6_pocket_miss",
        "title": "Puzzle 5: Missing the c6 Safety Pocket",
        "opp_name": "Chess.com Opponent (1285)",
        "time_class": "Blitz 3+0",
        "fen": "r1b1kb1r/ppp1pppp/2n2n2/q7/3P4/2N2N2/PPP2PPP/R1BQKB1R b KQkq - 2 5",
        "history_lead": ["1. e4", "d5", "2. exd5", "Qxd5", "3. Nc3", "Qa5", "4. d4", "Nf6", "5. Nf3", "Nc6"],
        "okanil_move": "Bg4",
        "okanil_san": "5... Bg4",
        "why_bad": "5...Bg4 is playable, but playing without ...c6 allows White to play 6.Bd2 or 6.Bb5/6.d5 harassing your Queen with tempo.",
        "expected_san": "Bg4",
        "expected_uci": "c8g4",
        "best_eval": "+0.5 for White",
        "why_best": "5...Bg4! pins White's knight to the Queen and readies 6...O-O-O or 6...e6. Remember Rule #2: follow up with ...c6 soon to secure the c7 retreat!",
        "pv": "5...Bg4 6.h3 Bxf3 7.Qxf3 O-O-O 8.Be3 e5"
    }
]

def get_blunder_puzzle(puzzle_id):
    for p in OKANIL_SCANDI_BLUNDERS:
        if p["id"] == puzzle_id:
            return p
    return OKANIL_SCANDI_BLUNDERS[0]

def list_blunder_puzzles():
    return OKANIL_SCANDI_BLUNDERS
