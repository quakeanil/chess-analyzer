"""
Scandinavian Grandmaster Games & "Guess the Move" Challenges
Featuring Magnus Carlsen, Sergei Tiviakov, and Viswanathan Anand.
"""

GM_GAMES = [
    {
        "id": "carlsen_caruana_2014",
        "title": "👑 Magnus Carlsen vs. Fabiano Caruana",
        "event": "Tromso Olympiad, 2014",
        "black_player": "Magnus Carlsen (2877)",
        "white_player": "Fabiano Caruana (2801)",
        "result": "0-1 (Carlsen Wins)",
        "opening": "Scandinavian: 3...Qd6 Classical",
        "story": "World Champion Magnus Carlsen chose the Scandinavian Defense against his world championship challenger Fabiano Caruana on the biggest international stage and scored a crushing win.",
        "fen_start": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "moves": [
            "e4", "d5", "exd5", "Qxd5", "Nc3", "Qd6", "d4", "Nf6", "Nf3", "c6",
            "Ne5", "Nbd7", "Bf4", "Nd5", "Nxd5", "Qxd5", "Be2", "Nxe5", "Bxe5", "Qxg2",
            "Bf3", "Qg6", "Qd2", "Bg4", "Bxg4", "Qxg4", "Qe2", "Qxe2+", "Kxe2", "f6",
            "Bf4", "g5", "Be3", "Kf7", "h4", "g4", "f3", "gxf3+", "Kxf3", "h5"
        ],
        "checkpoints": [
            {
                "ply": 6,
                "fen_before": "rnbqkbnr/ppp1pppp/3q4/8/3P4/2N2N2/PPP2PPP/R1BQKB1R b KQkq - 2 4",
                "last_white_move": "4. d4 Nf6 5. Nf3",
                "question": "Move 5: Caruana develops 5.Nf3. What is Black's Golden Move to blunt White's knights?",
                "best_move": "c6",
                "best_uci": "c7c6",
                "explanation": "5...c6! (Rule #2). Carlsen creates the c7 retreat square for his Queen, blunts White's knights from hopping to d5 or b5, and solidifies the center.",
                "gm_comment": "Magnus: '5...c6 is standard Scandinavian technique. White gets zero forward squares.'"
            },
            {
                "ply": 20,
                "fen_before": "r3kb1r/pp2pppp/2p5/3qB3/3P4/2N5/PPP1BP1P/R2QK2R b KQkq - 0 10",
                "last_white_move": "10. Bxe5",
                "question": "Move 10: Caruana trades knights on e5 leaving g2 undefended. What did Magnus play?",
                "best_move": "Qxg2",
                "best_uci": "d5g2",
                "explanation": "10...Qxg2!! Magnus snatches the g2 pawn, threatening the h1 rook and throwing White's kingside into disarray.",
                "gm_comment": "Magnus: 'When the pawn is poison-free, take it! White has no follow-up attack.'"
            },
            {
                "ply": 24,
                "fen_before": "r3kb1r/pp2pppp/2p3q1/4B3/3P4/2N2B2/PPPQ1P1P/R3K2R b KQkq - 2 12",
                "last_white_move": "12. Qd2",
                "question": "Move 12: Caruana plays 12.Qd2 preparing to castle queenside. How does Carlsen neutralize White's bishops?",
                "best_move": "Bg4",
                "best_uci": "c8g4",
                "explanation": "12...Bg4! Forces the trade of White's dangerous light-squared bishop, eliminating all tactical counterplay.",
                "gm_comment": "A classic Carlsen trade: strip the opponent of dynamic pieces and transition into a won endgame."
            }
        ]
    },
    {
        "id": "tiviakov_vanwely_2001",
        "title": "🛡️ Sergei Tiviakov vs. Loek van Wely",
        "event": "Wijk aan Zee Corus, 2001",
        "black_player": "Sergei Tiviakov (2680)",
        "white_player": "Loek van Wely (2700)",
        "result": "0-1 (Tiviakov Wins)",
        "opening": "Scandinavian: 3...Qd6 Tiviakov System",
        "story": "GM Sergei Tiviakov went an incredible 110 consecutive games undefeated at the highest level using the Scandinavian as Black. Here he showcases the ultimate central breakthrough.",
        "fen_start": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "moves": [
            "e4", "d5", "exd5", "Qxd5", "Nc3", "Qd6", "d4", "Nf6", "Nf3", "c6",
            "g3", "Bf5", "Bg2", "e6", "O-O", "Be7", "Bf4", "Qd8", "Qe2", "O-O",
            "Rfd1", "Nbd7", "Ne5", "Nxe5", "dxe5", "Nd5", "Nxd5", "cxd5", "c4", "d4"
        ],
        "checkpoints": [
            {
                "ply": 8,
                "fen_before": "rnbqkb1r/pp2pppp/2pq1n2/8/3P4/2N2NP1/PPP2PBP/R1BQK2R b KQkq - 1 6",
                "last_white_move": "6. g3",
                "question": "Move 6: Van Wely fianchettoes with 6.g3. Where does Black's light bishop belong?",
                "best_move": "Bf5",
                "best_uci": "c8f5",
                "explanation": "6...Bf5! (Rule #1). Activate the bishop to f5 BEFORE playing ...e6. The bishop exerts pressure down the c2 diagonal.",
                "gm_comment": "Tiviakov's trademark move: the bishop controls the key c2 outpost and frustrates White's plans."
            },
            {
                "ply": 28,
                "fen_before": "r2q1rk1/pp1b1ppp/4p3/3p4/2PP1B2/4P3/P3QPPP/R2R2K1 b - - 0 15",
                "last_white_move": "15. c4",
                "question": "Move 15: White strikes the center with 15.c4. Does Black take on c4 or push 15...d4!?",
                "best_move": "d4",
                "best_uci": "d5d4",
                "explanation": "15...d4! Creates a crushing passed pawn on d4 that splits White's pieces and secures a dominant winning endgame.",
                "gm_comment": "Tiviakov: 'A protected passed pawn on d4 is the dream in the Scandinavian!'"
            }
        ]
    }
]

def get_gm_game(game_id):
    for g in GM_GAMES:
        if g["id"] == game_id:
            return g
    return GM_GAMES[0]

def list_gm_games():
    return [
        {
            "id": g["id"],
            "title": g["title"],
            "event": g["event"],
            "result": g["result"],
            "opening": g["opening"]
        }
        for g in GM_GAMES
    ]
