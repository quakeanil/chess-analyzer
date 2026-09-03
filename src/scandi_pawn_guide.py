"""
Scandinavian Defense Pawn Skeleton & Strategic Middlegame Plans Guide
Defines the pawn structures, breaks, outposts, and plans for Black.
"""

PAWN_PLANS = {
    "skeleton_overview": {
        "title": "The Scandinavian 'Caro-Pawn' Fortress (c6 + e6)",
        "fen": "r1b1kb1r/pp2pppp/2p2n2/q7/3P4/2N2N2/PPP2PPP/R1BQKB1R b KQkq - 2 5",
        "chain_black": ["c6", "e6"],
        "chain_white": ["d4"],
        "summary": "Black establishes a solid pawn wedge on c6 and e6 (similar to the Caro-Kann Defense), but with one massive advantage: Black's light-squared bishop is already active outside the pawn chain on f5 or g4!",
        "pros": [
            "Completely blunts White's knights from ever landing on d5 or b5.",
            "Creates the ultimate escape pocket for the Queen on c7 or d8.",
            "Leaves Black with zero structural weaknesses."
        ]
    },
    "breaks": [
        {
            "id": "c5_break",
            "name": "Break #1: The ...c5! Central Dynamite",
            "trigger": "When White has established pawns on d4 and c3/c4.",
            "action": "Push ...c5! to trade Black's flank pawn for White's central d4 pawn.",
            "result": "Opens the d-file for your Queen and Rooks, isolates or eliminates White's center, and gives Black equal or superior endgame chances."
        },
        {
            "id": "e5_break",
            "name": "Break #2: The ...e5! Counter-Strike",
            "trigger": "When White's king is still uncastled or White plays passively with d3/Nf3.",
            "action": "Strike with ...e5! to blow open the center.",
            "result": "Pins White's pieces against their King along the e-file and creates immediate tactical pressure."
        }
    ],
    "archetypes": [
        {
            "id": "queenside_castle",
            "name": "Archetype A: Queenside Castling (0-0-0) & Dynamic Attack",
            "popular_in": "Mieses 3...Qa5 & Modern 2...Nf6",
            "setup": "Queen on a5, Bishop on f5/g4, Knight on d7/c6, Castle Queenside (0-0-0).",
            "middlegame_plan": "Place both rooks on the open d-file and e-file. Launch a kingside pawn storm with ...h5 and ...g5 against White's castled King!"
        },
        {
            "id": "kingside_castle",
            "name": "Archetype B: Kingside Castling (0-0) & Positional Squeeze",
            "popular_in": "Carlsen/Tiviakov 3...Qd6 & Banker 3...Qd8",
            "setup": "Pawns on c6 & e6, Bishop on e7, Knights on f6 & d7, Castle Kingside (0-0).",
            "middlegame_plan": "Patiently blockade White's pieces. Build pressure against White's d4 pawn, then execute the ...c5 break to trade down into an advantageous minor-piece endgame."
        }
    ]
}

def get_pawn_guide():
    return PAWN_PLANS
