"""
Scandinavian Defense Master Curriculum & Knowledge Base
Contains detailed lesson lines, strategic golden rules, tactical traps, and move-by-move explanations.
"""

GOLDEN_RULES = [
    {
        "id": "bishop_outside",
        "title": "Rule #1: Bishop Outside the Pawn Chain",
        "rule": "Always develop your light-squared bishop (to f5 or g4) BEFORE playing ...e6! If you play e6 first, your c8 bishop becomes a 'bad French bishop' locked behind pawns for the entire game."
    },
    {
        "id": "c6_pocket",
        "title": "Rule #2: The c6 Escape Pocket for the Queen",
        "rule": "In the 3...Qa5 mainline, play 5...c6! early. It blunts White's knights from jumping to d5 or b5, controls the d5 square, and gives your Queen a safe retreat to c7 or d8 if attacked."
    },
    {
        "id": "punish_2e5",
        "title": "Rule #3: Never play 2...e6 or 2...d4 against 2.e5",
        "rule": "When White pushes 2.e5, strike with 2...Bf5! followed by 3...e6 and an immediate 4...c5! counter-attack. You get an improved Caro-Kann / French with an active bishop and great winning chances."
    },
    {
        "id": "central_breaks",
        "title": "Rule #4: Know Your Pawn Breaks (...c5 and ...e5)",
        "rule": "Black's main central strike against White's d4 pawn is ...c5! After castling, look for timing to play ...c5 to open the d-file for your rooks and Queen."
    },
    {
        "id": "queen_safety",
        "title": "Rule #5: Do Not Be Greedy With the Queen",
        "rule": "Never chase pawns on b2 or a2 with your Queen early on when White has discovered attack opportunities with Bd2 or Nd5. Prioritize piece development and king safety."
    }
]

LESSONS = {
    "scandi_qa5": {
        "id": "scandi_qa5",
        "name": "👑 Lesson 1: Mieses-Kotrc 3...Qa5 Classical Mainline",
        "subtitle": "The most tested, rock-solid Scandinavian setup played by elite Grandmasters.",
        "side": "black",
        "initial_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "white_first": True,
        "moves": [
            {
                "ply": 1,
                "bot_move": "e4",
                "bot_san": "1. e4",
                "mentor_intro": "White opens with the King's Pawn 1.e4, controlling d5 and f5. Let's hit the center immediately!",
                "expected_san": "d5",
                "expected_uci": "d7d5",
                "good_alternatives": [],
                "why_best": "1...d5! is the Scandinavian Defense! You immediately challenge White's central e4 pawn on move 1, forcing White to react.",
                "blunders": {
                    "e5": "1...e5 is the Open Game (1.e4 e5), not the Scandinavian.",
                    "c5": "1...c5 is the Sicilian Defense.",
                    "e6": "1...e6 is the French Defense."
                }
            },
            {
                "ply": 2,
                "bot_move": "exd5",
                "bot_san": "2. exd5",
                "mentor_intro": "White accepts the central challenge and captures 2.exd5. How should we recapture?",
                "expected_san": "Qxd5",
                "expected_uci": "d8d5",
                "good_alternatives": ["Nf6"],
                "why_best": "2...Qxd5! recaptures the pawn immediately. Although White will develop a knight with tempo on move 3, Black's Queen is surprisingly safe and active.",
                "blunders": {
                    "c6": "2...c6?! is the Blackburne-Kloosterboer Gambit. Playable, but 2...Qxd5 is the rock-solid mainline."
                }
            },
            {
                "ply": 3,
                "bot_move": "Nc3",
                "bot_san": "3. Nc3",
                "mentor_intro": "White plays 3.Nc3 developing the knight and attacking your Queen. Where is her best home in the Classical line?",
                "expected_san": "Qa5",
                "expected_uci": "d5a5",
                "good_alternatives": ["Qd6", "Qd8"],
                "why_best": "3...Qa5! is the classical Scandinavian square! The Queen pins the a5-e1 diagonal, stays out of White's minor pieces' way, and eyes the c7 square for a retreat.",
                "blunders": {
                    "Qe5+": "3...Qe5+?? is a beginner mistake. White blocks with 4.Be2 with tempo and your Queen is in great danger.",
                    "Qe6+": "3...Qe6+? blocks your own dark bishop and lets White develop with Be2/Nf3.",
                    "Qf5": "3...Qf5?! leaves the Queen vulnerable to Bd3."
                }
            },
            {
                "ply": 4,
                "bot_move": "d4",
                "bot_san": "4. d4",
                "mentor_intro": "White grabs full control of the center with 4.d4. We need to develop our kingside pieces!",
                "expected_san": "Nf6",
                "expected_uci": "g8f6",
                "good_alternatives": ["c6"],
                "why_best": "4...Nf6! develops your kingside knight to its most active square, stops White from pushing e5, and prepares kingside castling.",
                "blunders": {
                    "e5": "4...e5?! is premature; White can win a pawn or trade queens into an awkward endgame.",
                    "e6": "4...e6?! traps your c8 bishop before it can get out!"
                }
            },
            {
                "ply": 5,
                "bot_move": "Nf3",
                "bot_san": "5. Nf3",
                "mentor_intro": "White develops their knight with 5.Nf3. Now comes the most important structural move in the Scandinavian!",
                "expected_san": "c6",
                "expected_uci": "c7c6",
                "good_alternatives": ["Bf5", "Bg4"],
                "why_best": "5...c6!! THE GOLDEN MOVE! This pawn creates an emergency retreat on c7 for your Queen, prevents White from playing Nd5 or Nb5, and controls d5.",
                "blunders": {
                    "e6": "5...e6?! before c6 and before Bf5 locks your bishop in! Remember Rule #1.",
                    "Nc6": "5...Nc6?! blocks the c-pawn, which is needed on c6 to protect the Queen."
                }
            },
            {
                "ply": 6,
                "bot_move": "Bc4",
                "bot_san": "6. Bc4",
                "mentor_intro": "White develops 6.Bc4 targeting f7. It's time for Rule #1: Where does your light bishop belong?",
                "expected_san": "Bf5",
                "expected_uci": "c8f5",
                "good_alternatives": ["Bg4"],
                "why_best": "6...Bf5! Superb! You bring the bishop outside the pawn chain to an active diagonal where it controls e4 and exerts pressure toward White's queenside.",
                "blunders": {
                    "e6": "6...e6?! locks the c8 bishop behind the e6-d5 wall forever! Always play Bf5 first.",
                    "Be6": "6...Be6?! allows 7.Bxe6 fxe6 ruining Black's kingside pawn structure."
                }
            },
            {
                "ply": 7,
                "bot_move": "Bd2",
                "bot_san": "7. Bd2",
                "mentor_intro": "White plays 7.Bd2 setting up a discovery attack with the Nc3 knight. Now your bishop is safely outside, so protect your center!",
                "expected_san": "e6",
                "expected_uci": "e7e6",
                "good_alternatives": ["Qc7"],
                "why_best": "7...e6! Perfect timing. Now that your bishop is outside on f5, 7...e6 builds an unshakeable central fortress (c6-d5-e6) and opens the way for your dark-squared bishop.",
                "blunders": {
                    "Nc6": "7...Nc6?! walks into 8.d5! attacking the knight.",
                    "Qc7": "7...Qc7 is decent, but 7...e6 immediately solidifies the center."
                }
            },
            {
                "ply": 8,
                "bot_move": "Qe2",
                "bot_san": "8. Qe2",
                "mentor_intro": "White prepares queenside castling with 8.Qe2. Black has a fabulous development option with the dark bishop:",
                "expected_san": "Bb4",
                "expected_uci": "f8b4",
                "good_alternatives": ["Be7", "Nbd7"],
                "why_best": "8...Bb4! pins the c3 knight, neutralizes White's discovery ideas, and prepares rapid castling! Black has achieved a completely equal, rock-solid position.",
                "blunders": {}
            }
        ]
    },

    "scandi_qd6": {
        "id": "scandi_qd6",
        "name": "🛡️ Lesson 2: The 3...Qd6 Tiviakov / Carlsen Fortress",
        "subtitle": "Carlsen & Tiviakov's favorite system: controls e5, stops Bf4, and prepares rapid ...a6 and ...b5 expansion.",
        "side": "black",
        "initial_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "white_first": True,
        "moves": [
            {
                "ply": 1,
                "bot_move": "e4",
                "bot_san": "1. e4",
                "mentor_intro": "White plays 1.e4. Strike the center!",
                "expected_san": "d5",
                "expected_uci": "d7d5",
                "good_alternatives": [],
                "why_best": "1...d5! challenges White's pawn immediately.",
                "blunders": {}
            },
            {
                "ply": 2,
                "bot_move": "exd5",
                "bot_san": "2. exd5",
                "mentor_intro": "White takes 2.exd5. Recapture!",
                "expected_san": "Qxd5",
                "expected_uci": "d8d5",
                "good_alternatives": ["Nf6"],
                "why_best": "2...Qxd5! recaptures with the Queen.",
                "blunders": {}
            },
            {
                "ply": 3,
                "bot_move": "Nc3",
                "bot_san": "3. Nc3",
                "mentor_intro": "White attacks your Queen with 3.Nc3. Today we play the Modern Grandmaster retreat favored by Magnus Carlsen!",
                "expected_san": "Qd6",
                "expected_uci": "d5d6",
                "good_alternatives": ["Qa5"],
                "why_best": "3...Qd6! On d6, the Queen controls the e5 square, prevents White from playing an easy Bf4, and stays flexible.",
                "blunders": {
                    "Qe5+": "3...Qe5+?? loses tempo to 4.Be2."
                }
            },
            {
                "ply": 4,
                "bot_move": "d4",
                "bot_san": "4. d4",
                "mentor_intro": "White stakes central claims with 4.d4. Develop your knight!",
                "expected_san": "Nf6",
                "expected_uci": "g8f6",
                "good_alternatives": ["c6", "a6"],
                "why_best": "4...Nf6! controls e4 and prepares kingside development.",
                "blunders": {}
            },
            {
                "ply": 5,
                "bot_move": "Nf3",
                "bot_san": "5. Nf3",
                "mentor_intro": "White plays 5.Nf3. What is Black's trademark move in the 3...Qd6 line to stop White's knight from attacking the Queen?",
                "expected_san": "a6",
                "expected_uci": "a7a6",
                "good_alternatives": ["c6", "g6"],
                "why_best": "5...a6! Beautiful! It completely stops White from playing 6.Nb5 hitting your Queen, and prepares Black to expand on the queenside with ...b5.",
                "blunders": {
                    "Nc6": "5...Nc6 allows 6.Nb5! Qd8 7.Bf4 with heavy pressure on c7."
                }
            },
            {
                "ply": 6,
                "bot_move": "g3",
                "bot_san": "6. g3",
                "mentor_intro": "White fianchettoes with 6.g3 intending Bg2 and Bf4. How should Black pin down White's knight?",
                "expected_san": "Bg4",
                "expected_uci": "c8g4",
                "good_alternatives": ["c6", "Bf5"],
                "why_best": "6...Bg4! pins White's f3 knight to the queen and develops Black's bishop outside the pawn chain before playing ...e6.",
                "blunders": {
                    "e6": "6...e6?! traps your c8 bishop again! Always develop the bishop first."
                }
            },
            {
                "ply": 7,
                "bot_move": "Bg2",
                "bot_san": "7. Bg2",
                "mentor_intro": "White finishes the fianchetto with 7.Bg2. Bring out your queenside knight to pressure d4!",
                "expected_san": "Nc6",
                "expected_uci": "b8c6",
                "good_alternatives": ["c6", "e6"],
                "why_best": "7...Nc6! puts direct pressure on White's d4 pawn and prepares 8...O-O-O for a crushing d-file battery!",
                "blunders": {}
            }
        ]
    },

    "scandi_advance": {
        "id": "scandi_advance",
        "name": "⛔ Lesson 3: Refuting the 2.e5 Advance Error",
        "subtitle": "Fix your #1 historical bottleneck! White tries to clamp down the center; Black punishes them with 2...Bf5! and 4...c5!.",
        "side": "black",
        "initial_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "white_first": True,
        "moves": [
            {
                "ply": 1,
                "bot_move": "e4",
                "bot_san": "1. e4",
                "mentor_intro": "White starts 1.e4. Stake your claim in the center!",
                "expected_san": "d5",
                "expected_uci": "d7d5",
                "good_alternatives": [],
                "why_best": "1...d5! The Scandinavian strike.",
                "blunders": {}
            },
            {
                "ply": 2,
                "bot_move": "e5",
                "bot_san": "2. e5",
                "mentor_intro": "WHITE BLUNDERS / PLAYS INACCURATE 2.e5! This was your historical weakness. What is the GOLDEN MOVE here?",
                "expected_san": "Bf5",
                "expected_uci": "c8f5",
                "good_alternatives": [],
                "why_best": "2...Bf5!! CRITICAL MASTER MOVE! When White closes the center with e5, your bishop MUST escape outside the pawn chain before you play e6. If you play e6 first, you're locked in a bad French. With 2...Bf5!, Black has an improved Caro-Kann!",
                "blunders": {
                    "e6": "2...e6?? NO! This traps your bishop on c8 for the rest of the game! Always play 2...Bf5! first!",
                    "d4": "2...d4?! leaves you cramped and lets White attack with f4.",
                    "c5": "2...c5 is okay, but 2...Bf5! is much stronger."
                }
            },
            {
                "ply": 3,
                "bot_move": "d4",
                "bot_san": "3. d4",
                "mentor_intro": "White plays 3.d4 to reinforce e5. Now that your bishop is safe outside on f5, how do you lock your center?",
                "expected_san": "e6",
                "expected_uci": "e7e6",
                "good_alternatives": [],
                "why_best": "3...e6! Now it is completely safe to play e6 because your bishop is already developed outside on f5! Black's pawn structure is bulletproof.",
                "blunders": {
                    "Nc6": "3...Nc6 is playable, but 3...e6 solidifies the structure immediately."
                }
            },
            {
                "ply": 4,
                "bot_move": "Nf3",
                "bot_san": "4. Nf3",
                "mentor_intro": "White plays 4.Nf3. What is Black's primary pawn break against White's d4 pawn chain?",
                "expected_san": "c5",
                "expected_uci": "c7c5",
                "good_alternatives": ["Nc6"],
                "why_best": "4...c5! Boom! The thematic counter-strike. Black chips away at White's d4 center immediately. White's e5 pawn is overextended and will soon fall.",
                "blunders": {
                    "Be7": "4...Be7 is too passive. Strike with 4...c5! while White is uncastled."
                }
            },
            {
                "ply": 5,
                "bot_move": "c3",
                "bot_san": "5. c3",
                "mentor_intro": "White bolsters d4 with 5.c3. Bring out another attacker against d4!",
                "expected_san": "Nc6",
                "expected_uci": "b8c6",
                "good_alternatives": ["Qb6"],
                "why_best": "5...Nc6! adds a second attacker to d4 and controls the e5 square.",
                "blunders": {}
            },
            {
                "ply": 6,
                "bot_move": "Be2",
                "bot_san": "6. Be2",
                "mentor_intro": "White develops 6.Be2. Put double pressure on White's d4 pawn AND b2 pawn with the Queen!",
                "expected_san": "Qb6",
                "expected_uci": "d8b6",
                "good_alternatives": ["cxd4"],
                "why_best": "6...Qb6! Double threat! The Queen attacks d4 and targets the undefended b2 pawn. Black has a massive initiative and White is on the back foot.",
                "blunders": {}
            }
        ]
    },

    "scandi_modern": {
        "id": "scandi_modern",
        "name": "🗡️ Lesson 4: The Modern 2...Nf6 & Portuguese Gambit",
        "subtitle": "Sharp, dynamic attacking chess! Don't bring the Queen out early — swarm White with rapid piece development.",
        "side": "black",
        "initial_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "white_first": True,
        "moves": [
            {
                "ply": 1,
                "bot_move": "e4",
                "bot_san": "1. e4",
                "mentor_intro": "White opens 1.e4.",
                "expected_san": "d5",
                "expected_uci": "d7d5",
                "good_alternatives": [],
                "why_best": "1...d5! hits the center.",
                "blunders": {}
            },
            {
                "ply": 2,
                "bot_move": "exd5",
                "bot_san": "2. exd5",
                "mentor_intro": "White plays 2.exd5. Instead of Queen out, let's develop a knight to keep maximum tactical tension!",
                "expected_san": "Nf6",
                "expected_uci": "g8f6",
                "good_alternatives": ["Qxd5"],
                "why_best": "2...Nf6! The Modern Scandinavian. Black avoids an early Queen chase and threatens to recapture d5 with a piece, or play a venomous gambit.",
                "blunders": {}
            },
            {
                "ply": 3,
                "bot_move": "d4",
                "bot_san": "3. d4",
                "mentor_intro": "White plays 3.d4 maintaining control of d5. Now, play the sharp Portuguese Gambit to pin White down!",
                "expected_san": "Bg4",
                "expected_uci": "c8g4",
                "good_alternatives": ["Nxd5"],
                "why_best": "3...Bg4! The Portuguese Gambit! Black attacks the d1 Queen and develops with tempo, daring White to weaken their king with f3.",
                "blunders": {
                    "e6": "3...e6?! traps your c8 bishop before developing it."
                }
            },
            {
                "ply": 4,
                "bot_move": "f3",
                "bot_san": "4. f3",
                "mentor_intro": "White blocks the attack with 4.f3, weakening their light squares. Where should the bishop retreat?",
                "expected_san": "Bf5",
                "expected_uci": "g4f5",
                "good_alternatives": ["Bh5"],
                "why_best": "4...Bf5! maintains control of the c2 and b1 squares while leaving White with a weakened kingside diagonal (e1-h4).",
                "blunders": {}
            },
            {
                "ply": 5,
                "bot_move": "c4",
                "bot_san": "5. c4",
                "mentor_intro": "White tries to hold the extra d5 pawn with 5.c4. Blow open the center with the classic gambit strike!",
                "expected_san": "e6",
                "expected_uci": "e7e6",
                "good_alternatives": ["c6"],
                "why_best": "5...e6! Sacrificing a pawn to open lines for Black's Queen and dark bishop. Black will castle rapidly and White's king will be under lethal fire.",
                "blunders": {}
            },
            {
                "ply": 6,
                "bot_move": "dxe6",
                "bot_san": "6. dxe6",
                "mentor_intro": "White takes the bait with 6.dxe6. Bring your knight into the attack!",
                "expected_san": "Nc6",
                "expected_uci": "b8c6",
                "good_alternatives": ["Bxe6"],
                "why_best": "6...Nc6! Terrific piece activity! Black targets d4 and e5 while preparing 7...Qe7 and 8...O-O-O. Black has immense compensation.",
                "blunders": {}
            }
        ]
    },
    "scandi_qd8": {
        "id": "scandi_qd8",
        "name": "🛡️ Lesson 5: The Banker / Solid 3...Qd8 Retreat",
        "subtitle": "Ultra-solid, favorite of Super-GMs Carlsen and Shankland. Gives White zero tactical targets.",
        "side": "black",
        "initial_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "white_first": True,
        "moves": [
            {
                "ply": 1,
                "bot_move": "e4",
                "bot_san": "1. e4",
                "mentor_intro": "White plays 1.e4.",
                "expected_san": "d5",
                "expected_uci": "d7d5",
                "why_best": "1...d5! strikes the center."
            },
            {
                "ply": 2,
                "bot_move": "exd5",
                "bot_san": "2. exd5",
                "mentor_intro": "White captures 2.exd5. Recapture with the Queen.",
                "expected_san": "Qxd5",
                "expected_uci": "d8d5",
                "why_best": "2...Qxd5! brings the Queen to center."
            },
            {
                "ply": 3,
                "bot_move": "Nc3",
                "bot_san": "3. Nc3",
                "mentor_intro": "White attacks your Queen with 3.Nc3. Play the Banker retreat!",
                "expected_san": "Qd8",
                "expected_uci": "d5d8",
                "good_alternatives": ["Qa5", "Qd6"],
                "why_best": "3...Qd8! The Banker retreat! Your Queen returns to complete safety. White's Nc3 blocks their c-pawn, and Black has an unbreachable Caro-Kann-like pawn structure."
            },
            {
                "ply": 4,
                "bot_move": "d4",
                "bot_san": "4. d4",
                "mentor_intro": "White takes the center with 4.d4. Develop your kingside knight.",
                "expected_san": "Nf6",
                "expected_uci": "g8f6",
                "why_best": "4...Nf6 controls e4 and d5, preparing to pin White's knight."
            },
            {
                "ply": 5,
                "bot_move": "Nf3",
                "bot_san": "5. Nf3",
                "mentor_intro": "White plays 5.Nf3. Pin the knight before playing ...e6 (Rule #1)!",
                "expected_san": "Bg4",
                "expected_uci": "c8g4",
                "good_alternatives": ["Bf5", "c6"],
                "why_best": "5...Bg4! pins White's knight to the Queen and prepares a fortress with ...c6 and ...e6."
            },
            {
                "ply": 6,
                "bot_move": "h3",
                "bot_san": "6. h3",
                "mentor_intro": "White questions your bishop with 6.h3. Trade on f3 to double pawns or remove the defender of d4.",
                "expected_san": "Bxf3",
                "expected_uci": "g4f3",
                "why_best": "6...Bxf3! 7.Qxf3 c6! Black gets a rock-solid position with zero weaknesses."
            }
        ]
    },
    "scandi_icelandic": {
        "id": "scandi_icelandic",
        "name": "🗡️ Lesson 6: The Icelandic Gambit (3.c4 e6!)",
        "subtitle": "Sharp, venomous gambit sacrificing a pawn for crushing piece development and central pin tactics.",
        "side": "black",
        "initial_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "white_first": True,
        "moves": [
            {
                "ply": 1,
                "bot_move": "e4",
                "bot_san": "1. e4",
                "mentor_intro": "White opens 1.e4.",
                "expected_san": "d5",
                "expected_uci": "d7d5",
                "why_best": "1...d5!"
            },
            {
                "ply": 2,
                "bot_move": "exd5",
                "bot_san": "2. exd5",
                "mentor_intro": "White takes 2.exd5. Play the Modern 2...Nf6!",
                "expected_san": "Nf6",
                "expected_uci": "g8f6",
                "why_best": "2...Nf6 invites White to try to hold the pawn with c4."
            },
            {
                "ply": 3,
                "bot_move": "c4",
                "bot_san": "3. c4",
                "mentor_intro": "White greedily plays 3.c4 to keep the extra pawn. Launch the Icelandic Gambit!",
                "expected_san": "e6",
                "expected_uci": "e7e6",
                "why_best": "3...e6!! The Icelandic Gambit! Black offers a second pawn to blow open the e-file and diagonally activate both bishops."
            },
            {
                "ply": 4,
                "bot_move": "dxe6",
                "bot_san": "4. dxe6",
                "mentor_intro": "White accepts with 4.dxe6. Recapture with the bishop!",
                "expected_san": "Bxe6",
                "expected_uci": "c8e6",
                "why_best": "4...Bxe6! develops with tempo against White's c4 pawn."
            },
            {
                "ply": 5,
                "bot_move": "Nf3",
                "bot_san": "5. Nf3",
                "mentor_intro": "White plays 5.Nf3. Pin the knight or pin the king along the e-file with 5...Qe7!",
                "expected_san": "Qe7",
                "expected_uci": "d8e7",
                "good_alternatives": ["Bb4+", "Bc5"],
                "why_best": "5...Qe7! sets up a devastating discovered check (e.g. 6.Be2 Bxc4!). Black's attack is ferocious."
            }
        ]
    },
    "scandi_b4_gambit": {
        "id": "scandi_b4_gambit",
        "name": "💰 Lesson 7: Refuting the 4.b4?! Wing Gambit",
        "subtitle": "Punish club players who try to deflect your Queen with 4.b4?! and emerge a clean pawn ahead.",
        "side": "black",
        "initial_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "white_first": True,
        "moves": [
            {
                "ply": 1,
                "bot_move": "e4",
                "bot_san": "1. e4",
                "mentor_intro": "White plays 1.e4.",
                "expected_san": "d5",
                "expected_uci": "d7d5",
                "why_best": "1...d5!"
            },
            {
                "ply": 2,
                "bot_move": "exd5",
                "bot_san": "2. exd5",
                "mentor_intro": "White plays 2.exd5.",
                "expected_san": "Qxd5",
                "expected_uci": "d8d5",
                "why_best": "2...Qxd5!"
            },
            {
                "ply": 3,
                "bot_move": "Nc3",
                "bot_san": "3. Nc3",
                "mentor_intro": "White plays 3.Nc3.",
                "expected_san": "Qa5",
                "expected_uci": "d5a5",
                "why_best": "3...Qa5!"
            },
            {
                "ply": 4,
                "bot_move": "b4",
                "bot_san": "4. b4",
                "mentor_intro": "White plays 4.b4?!, the Wing Gambit. Take the free pawn!",
                "expected_san": "Qxb4",
                "expected_uci": "a5b4",
                "why_best": "4...Qxb4! Punishes White's bluff. Black wins a pawn and pins White's queenside."
            },
            {
                "ply": 5,
                "bot_move": "Rb1",
                "bot_san": "5. Rb1",
                "mentor_intro": "White attacks with 5.Rb1. Retreat the Queen to d6 safely!",
                "expected_san": "Qd6",
                "expected_uci": "b4d6",
                "good_alternatives": ["Qd8", "Qa5"],
                "why_best": "5...Qd6! Centralizes the Queen, keeps control of d4, and secures your pawn advantage."
            }
        ]
    },
    "scandi_tennison": {
        "id": "scandi_tennison",
        "name": "⚡ Lesson 8: Punishing the Tennison Gambit",
        "subtitle": "Defend against White's 2.Nf3 dxe4 3.Ng5 ICBM trick and convert your material advantage.",
        "side": "black",
        "initial_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "white_first": True,
        "moves": [
            {
                "ply": 1,
                "bot_move": "e4",
                "bot_san": "1. e4",
                "mentor_intro": "White opens 1.e4.",
                "expected_san": "d5",
                "expected_uci": "d7d5",
                "why_best": "1...d5!"
            },
            {
                "ply": 2,
                "bot_move": "Nf3",
                "bot_san": "2. Nf3",
                "mentor_intro": "White plays 2.Nf3?!, the Tennison Gambit instead of taking! Win the central e4 pawn!",
                "expected_san": "dxe4",
                "expected_uci": "d5e4",
                "why_best": "2...dxe4! wins White's central e-pawn immediately."
            },
            {
                "ply": 3,
                "bot_move": "Ng5",
                "bot_san": "3. Ng5",
                "mentor_intro": "White attacks e4 with 3.Ng5. Defend the pawn with 3...Nf6!",
                "expected_san": "Nf6",
                "expected_uci": "g8f6",
                "good_alternatives": ["Bf5"],
                "why_best": "3...Nf6! Natural piece development defending e4."
            },
            {
                "ply": 4,
                "bot_move": "Bc4",
                "bot_san": "4. Bc4",
                "mentor_intro": "White targets f7 with 4.Bc4. Blunt the bishop with 4...e6!",
                "expected_san": "e6",
                "expected_uci": "e7e6",
                "why_best": "4...e6! shuts down all of White's cheap tricks against f7. White is simply a pawn down with no compensation."
            }
        ]
    },
    "scandi_0kanil_leaks": {
        "id": "scandi_0kanil_leaks",
        "name": "📊 Lesson 9: 0kanil's Match Stats & Top 3 Leaks Fixer",
        "subtitle": "Based on 369 real Scandinavian matches on Chess.com (176W / 180L). Fixes your 64% loss rate against 2.e5!",
        "side": "black",
        "initial_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "white_first": True,
        "moves": [
            {
                "ply": 1,
                "bot_move": "e4",
                "bot_san": "1. e4",
                "mentor_intro": "Your opponents opened 1.e4 in 328+ games. Play your signature Scandinavian strike!",
                "expected_san": "d5",
                "expected_uci": "d7d5",
                "why_best": "1...d5! You have played this 369 times on Chess.com."
            },
            {
                "ply": 2,
                "bot_move": "e5",
                "bot_san": "2. e5",
                "mentor_intro": "White plays 2.e5 (played in 36 of your matches). In 31 games you played 2...d4?! and suffered a 64% loss rate! What is the GM refutation?",
                "expected_san": "Bf5",
                "expected_uci": "c8f5",
                "good_alternatives": ["c5"],
                "why_best": "2...Bf5!! The #1 fix for your Scandinavian record! Never push 2...d4 which locks your pieces. Activating your bishop outside the pawn chain gives Black a 65%+ win rate!"
            },
            {
                "ply": 3,
                "bot_move": "d4",
                "bot_san": "3. d4",
                "mentor_intro": "White builds the center with 3.d4. Now lock your pawn chain safely with Rule #1!",
                "expected_san": "e6",
                "expected_uci": "e7e6",
                "why_best": "3...e6! Now that your bishop is outside on f5, e6 secures the center and creates an improved French defense with zero bad pieces."
            },
            {
                "ply": 4,
                "bot_move": "Nf3",
                "bot_san": "4. Nf3",
                "mentor_intro": "White develops with 4.Nf3. Execute the central dynamite pawn break (Rule #4)!",
                "expected_san": "c5",
                "expected_uci": "c7c5",
                "why_best": "4...c5!! The signature Scandinavian strike! You hammer White's d4 pawn, prepare Nc6 and Qb6, and seize the initiative."
            },
            {
                "ply": 5,
                "bot_move": "c3",
                "bot_san": "5. c3",
                "mentor_intro": "White tries to hold the center with 5.c3. Bring your knight to attack d4!",
                "expected_san": "Nc6",
                "expected_uci": "b8c6",
                "why_best": "5...Nc6! Piles pressure on d4 and e5. Black's position is completely winning strategically."
            }
        ]
    },
    "center_game_paulsen": {
        "id": "center_game_paulsen",
        "name": "⚔️ Lesson 10: The Center Game (1.e4 e5 2.d4 exd4 3.Qxd4!)",
        "subtitle": "The Scandinavian in Reverse with an extra tempo! Master the lethal 4.Qe3 Paulsen Attack.",
        "side": "white",
        "initial_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "white_first": False,
        "moves": [
            {
                "ply": 1,
                "expected_san": "e4",
                "expected_uci": "e2e4",
                "why_best": "1.e4 controls the center and opens diagonals for your Queen and Bishop.",
                "bot_move": "e5",
                "bot_san": "1... e5",
                "mentor_intro": "You open 1.e4. Black responds classically with 1...e5."
            },
            {
                "ply": 2,
                "expected_san": "d4",
                "expected_uci": "d2d4",
                "why_best": "2.d4! Strike the center immediately! The Center Game challenges Black's e5 pawn on move 2.",
                "bot_move": "exd4",
                "bot_san": "2... exd4",
                "mentor_intro": "Black captures 2...exd4."
            },
            {
                "ply": 3,
                "expected_san": "Qxd4",
                "expected_uci": "d1d4",
                "why_best": "3.Qxd4! Recapture with the Queen! This is the Scandinavian Defense with reversed colors and White has an extra tempo.",
                "bot_move": "Nc6",
                "bot_san": "3... Nc6",
                "mentor_intro": "Black attacks your Queen with 3...Nc6. Where is the modern Grandmaster retreat?"
            },
            {
                "ply": 4,
                "expected_san": "Qe3",
                "expected_uci": "d4e3",
                "good_alternatives": ["Qa4"],
                "why_best": "4.Qe3! The Mieses-Chigorin / Paulsen Attack! It prevents Black from playing an easy ...d5, controls the third rank, and prepares rapid 0-0-0.",
                "bot_move": "Nf6",
                "bot_san": "4... Nf6",
                "mentor_intro": "Black develops 4...Nf6 attacking e4. Defend e4 and develop your knight!"
            },
            {
                "ply": 5,
                "expected_san": "Nc3",
                "expected_uci": "b1c3",
                "why_best": "5.Nc3! Solidifies e4 and controls d5.",
                "bot_move": "Bb4",
                "bot_san": "5... Bb4",
                "mentor_intro": "Black pins your knight with 5...Bb4. Break the pin and prepare to castle queenside!"
            },
            {
                "ply": 6,
                "expected_san": "Bd2",
                "expected_uci": "c1d2",
                "why_best": "6.Bd2! Neutralizes the pin and clears the back rank for 0-0-0.",
                "bot_move": "O-O",
                "bot_san": "6... O-O",
                "mentor_intro": "Black castles kingside 6...O-O. Complete your development with the queenside castle battery!"
            },
            {
                "ply": 7,
                "expected_san": "O-O-O",
                "expected_uci": "e1c1",
                "why_best": "7.O-O-O!! The dream setup! Your King is safe on the queenside, your rook commands the open d-file, and you are ready to roll your kingside pawns with Qg3, f4, and h4!"
            }
        ]
    }
}

def get_lesson(lesson_id):
    return LESSONS.get(lesson_id, LESSONS["scandi_qa5"])

def list_lessons():
    return [
        {"id": k, "name": v["name"], "subtitle": v["subtitle"]}
        for k, v in LESSONS.items()
    ]
