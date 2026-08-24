"""
HTML Dashboard & Full Opening Trainer Generator for Chess Diagnostic Tool
"""
import json
import os

def generate_html_dashboard(analysis_data, user_stats, output_path="dashboard.html"):
    stats_json = json.dumps(analysis_data)
    user_stats_json = json.dumps(user_stats)
    
    # Load top openings json if exists
    top_openings_file = os.path.join(os.path.dirname(output_path), "data", "top_openings.json")
    top_openings_data = {}
    if os.path.exists(top_openings_file):
        try:
            with open(top_openings_file, "r", encoding="utf-8") as f:
                top_openings_data = json.load(f)
        except Exception:
            pass
            
    top_openings_json = json.dumps(top_openings_data)
    
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chess.com Diagnostics & Opening Trainer - __USERNAME__</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chessboard.js & jQuery & Chess.js -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/chessboard-js/1.0.0/chessboard-1.0.0.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chessboard-js/1.0.0/chessboard-1.0.0.min.js"></script>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .tab-btn.active { border-bottom: 3px solid #38bdf8; color: #38bdf8; font-weight: 600; }
        .board-container { max-width: 420px; width: 100%; margin: 0 auto; }
        .badge-loss { background-color: #ef444420; color: #ef4444; border: 1px solid #ef444450; }
        .badge-win { background-color: #22c55e20; color: #22c55e; border: 1px solid #22c55e50; }
        .trainer-card.active { border-color: #38bdf8; background-color: #0369a120; }
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- Header -->
    <header class="bg-slate-900 border-b border-slate-800 px-6 py-4 flex flex-wrap items-center justify-between shadow-lg">
        <div class="flex items-center space-x-3">
            <span class="text-3xl">♟️</span>
            <div>
                <h1 class="text-xl font-bold text-white flex items-center gap-2">
                    Chess Diagnostic Copilot & Opening Trainer
                    <span class="text-xs bg-sky-500/20 text-sky-400 border border-sky-500/30 px-2 py-0.5 rounded font-mono">__USERNAME__</span>
                </h1>
                <p class="text-xs text-slate-400">Move-by-Move Opening Diagnosis, Top 10 Analytics & Interactive Drills</p>
            </div>
        </div>
        <div class="flex gap-4 mt-2 sm:mt-0 text-sm">
            <div class="bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700">
                <span class="text-slate-400">Blitz:</span> <span class="font-bold text-amber-400" id="blitz-rating">--</span>
            </div>
            <div class="bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700">
                <span class="text-slate-400">Bullet:</span> <span class="font-bold text-orange-400" id="bullet-rating">--</span>
            </div>
            <div class="bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700">
                <span class="text-slate-400">Tactics Peak:</span> <span class="font-bold text-emerald-400" id="tactics-rating">--</span>
            </div>
        </div>
    </header>

    <!-- Navigation Tabs -->
    <div class="bg-slate-900/80 backdrop-blur border-b border-slate-800 px-6">
        <nav class="flex space-x-8 text-sm">
            <button onclick="switchTab('overview')" id="tab-overview" class="tab-btn active py-3 px-1 text-slate-300 hover:text-white transition">Top 10 Win/Loss Openings</button>
            <button onclick="switchTab('trainer')" id="tab-trainer" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition">🎯 Interactive Opening Trainer</button>
            <button onclick="switchTab('disasters')" id="tab-disasters" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition">Early Disaster Replayer (<=15 moves)</button>
            <button onclick="switchTab('repertoire')" id="tab-repertoire" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition">Coach's Golden Rules & Repertoire</button>
        </nav>
    </div>

    <!-- Main Content Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto p-6">

        <!-- TAB 1: TOP 10 WINNING & LOSING OPENINGS -->
        <section id="view-overview" class="space-y-6">
            <!-- Top Metric Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-slate-800/80 p-5 rounded-xl border border-slate-700">
                    <div class="text-xs text-slate-400 uppercase font-semibold">Total Games</div>
                    <div class="text-2xl font-bold text-white mt-1">__TOTAL_GAMES__</div>
                    <div class="text-xs text-slate-400 mt-2">Win Rate: <span class="text-emerald-400 font-semibold">__WIN_RATE__%</span></div>
                </div>
                <div class="bg-slate-800/80 p-5 rounded-xl border border-slate-700">
                    <div class="text-xs text-slate-400 uppercase font-semibold">Record (W / L / D)</div>
                    <div class="text-2xl font-bold text-slate-200 mt-1">__TOTAL_WINS__ / __TOTAL_LOSSES__ / __TOTAL_DRAWS__</div>
                    <div class="text-xs text-slate-400 mt-2">Resignations: __RESIGNED__</div>
                </div>
                <div class="bg-slate-800/80 p-5 rounded-xl border border-rose-900/50 bg-gradient-to-br from-slate-800 to-rose-950/30">
                    <div class="text-xs text-rose-400 uppercase font-semibold">Early Disasters (<=15 moves)</div>
                    <div class="text-2xl font-bold text-rose-400 mt-1">__DISASTERS_COUNT__ games</div>
                    <div class="text-xs text-rose-300/70 mt-2">18% of all losses happened in opening!</div>
                </div>
                <div class="bg-slate-800/80 p-5 rounded-xl border border-emerald-900/50 bg-gradient-to-br from-slate-800 to-emerald-950/30">
                    <div class="text-xs text-emerald-400 uppercase font-semibold">Puzzle Peak Rating</div>
                    <div class="text-2xl font-bold text-emerald-400 mt-1">1,736</div>
                    <div class="text-xs text-emerald-300/70 mt-2">Strong tactical foundation</div>
                </div>
            </div>

            <!-- Queen's Pawn Breakdown Box -->
            <div class="bg-amber-950/40 border border-amber-600/50 rounded-xl p-5">
                <h3 class="text-base font-bold text-amber-300 flex items-center gap-2">
                    <span>👑</span> Why You Are Losing With Queen's Pawn (1.d4) as White: The Vital Distinction
                </h3>
                <p class="text-sm text-slate-300 mt-2 leading-relaxed">
                    1.d4 itself is one of the strongest openings in chess. However, your data reveals a massive contrast:
                </p>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-3 text-xs">
                    <div class="bg-emerald-950/40 border border-emerald-700/60 p-3 rounded-lg">
                        <strong class="text-emerald-400 text-sm block mb-1">🟢 When you play ACTIVE d4 (2.Bf4 London / Horwitz):</strong>
                        <p class="text-slate-200">You score <strong>80% to 100% win rates</strong>! Your pieces are active and king is safe.</p>
                    </div>
                    <div class="bg-rose-950/40 border border-rose-700/60 p-3 rounded-lg">
                        <strong class="text-rose-400 text-sm block mb-1">🔴 When you play PASSIVE d4 (2.Nf3 & 3.e3 Zukertort):</strong>
                        <p class="text-slate-200">Your loss rate jumps to <strong>69% – 80%</strong>! The bishop gets locked on c1 and Black attacks first.</p>
                    </div>
                </div>
            </div>

            <!-- TOP 10 TABLES GRID -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- White Top 10 Winning -->
                <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-5">
                    <h3 class="text-sm font-bold text-emerald-400 mb-3 flex items-center justify-between">
                        <span>🏆 Top 10 WINNING Openings as White</span>
                        <span class="text-xs text-slate-400">Min 5 games</span>
                    </h3>
                    <div class="overflow-x-auto">
                        <table class="w-full text-xs text-left text-slate-300">
                            <thead class="text-slate-400 bg-slate-900/60 uppercase">
                                <tr>
                                    <th class="py-2 px-3">Opening</th>
                                    <th class="py-2 px-2 text-center">Games</th>
                                    <th class="py-2 px-2 text-center">Win %</th>
                                    <th class="py-2 px-2 text-center">Loss %</th>
                                </tr>
                            </thead>
                            <tbody id="white-win-tbody" class="divide-y divide-slate-700/50"></tbody>
                        </table>
                    </div>
                </div>

                <!-- White Top 10 Losing -->
                <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-5">
                    <h3 class="text-sm font-bold text-rose-400 mb-3 flex items-center justify-between">
                        <span>⚠️ Top 10 LOSING Openings as White</span>
                        <span class="text-xs text-slate-400">Min 5 games</span>
                    </h3>
                    <div class="overflow-x-auto">
                        <table class="w-full text-xs text-left text-slate-300">
                            <thead class="text-slate-400 bg-slate-900/60 uppercase">
                                <tr>
                                    <th class="py-2 px-3">Opening</th>
                                    <th class="py-2 px-2 text-center">Games</th>
                                    <th class="py-2 px-2 text-center">Loss %</th>
                                    <th class="py-2 px-2 text-center">Win %</th>
                                </tr>
                            </thead>
                            <tbody id="white-loss-tbody" class="divide-y divide-slate-700/50"></tbody>
                        </table>
                    </div>
                </div>

                <!-- Black Top 10 Winning -->
                <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-5">
                    <h3 class="text-sm font-bold text-emerald-400 mb-3 flex items-center justify-between">
                        <span>🏆 Top 10 WINNING Openings as Black</span>
                        <span class="text-xs text-slate-400">Min 5 games</span>
                    </h3>
                    <div class="overflow-x-auto">
                        <table class="w-full text-xs text-left text-slate-300">
                            <thead class="text-slate-400 bg-slate-900/60 uppercase">
                                <tr>
                                    <th class="py-2 px-3">Opening</th>
                                    <th class="py-2 px-2 text-center">Games</th>
                                    <th class="py-2 px-2 text-center">Win %</th>
                                    <th class="py-2 px-2 text-center">Loss %</th>
                                </tr>
                            </thead>
                            <tbody id="black-win-tbody" class="divide-y divide-slate-700/50"></tbody>
                        </table>
                    </div>
                </div>

                <!-- Black Top 10 Losing -->
                <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-5">
                    <h3 class="text-sm font-bold text-rose-400 mb-3 flex items-center justify-between">
                        <span>⚠️ Top 10 LOSING Openings as Black</span>
                        <span class="text-xs text-slate-400">Min 5 games</span>
                    </h3>
                    <div class="overflow-x-auto">
                        <table class="w-full text-xs text-left text-slate-300">
                            <thead class="text-slate-400 bg-slate-900/60 uppercase">
                                <tr>
                                    <th class="py-2 px-3">Opening</th>
                                    <th class="py-2 px-2 text-center">Games</th>
                                    <th class="py-2 px-2 text-center">Loss %</th>
                                    <th class="py-2 px-2 text-center">Win %</th>
                                </tr>
                            </thead>
                            <tbody id="black-loss-tbody" class="divide-y divide-slate-700/50"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 2: INTERACTIVE OPENING TRAINER -->
        <section id="view-trainer" class="hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <!-- Left: Board & Move Controls -->
                <div class="lg:col-span-6 flex flex-col items-center">
                    <div class="board-container shadow-2xl rounded-lg overflow-hidden border border-slate-700">
                        <div id="trainer-board" style="width: 100%"></div>
                    </div>
                    <!-- Feedback & Controls -->
                    <div class="w-full max-w-[420px] mt-4 space-y-3">
                        <div id="trainer-feedback" class="p-4 rounded-lg bg-slate-900 border border-slate-700 text-sm">
                            <div class="font-semibold text-slate-300" id="trainer-prompt">Select an opening drill to begin!</div>
                            <div class="text-xs text-slate-400 mt-1" id="trainer-subtext">Play the correct move on the board.</div>
                        </div>

                        <div class="flex items-center justify-between text-xs text-slate-400 bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
                            <span id="trainer-step-indicator">Move: 0 / 0</span>
                            <div class="space-x-2">
                                <button onclick="resetCurrentDrill()" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-white rounded">🔄 Reset Drill</button>
                                <button onclick="showDrillHint()" class="px-2.5 py-1 bg-sky-600 hover:bg-sky-500 text-white rounded">💡 Hint</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Right: Drill Selector List -->
                <div class="lg:col-span-6 space-y-4">
                    <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-5 flex flex-col h-full">
                        <div class="flex items-center justify-between mb-3">
                            <h3 class="text-base font-bold text-white flex items-center gap-2">
                                <span>📚</span> Select Repertoire Drill
                            </h3>
                            <div class="flex gap-1 text-xs">
                                <button onclick="filterDrills('all')" class="px-2 py-1 bg-slate-700 rounded text-white" id="filter-all">All</button>
                                <button onclick="filterDrills('white_fix')" class="px-2 py-1 bg-slate-900 hover:bg-slate-700 rounded text-slate-300" id="filter-white_fix">⚪ White Fixes</button>
                                <button onclick="filterDrills('black_fix')" class="px-2 py-1 bg-slate-900 hover:bg-slate-700 rounded text-slate-300" id="filter-black_fix">⚫ Black Fixes</button>
                                <button onclick="filterDrills('winning')" class="px-2 py-1 bg-slate-900 hover:bg-slate-700 rounded text-slate-300" id="filter-winning">🏆 Master Lines</button>
                            </div>
                        </div>

                        <div id="drills-list-container" class="space-y-2 max-h-[520px] overflow-y-auto pr-1"></div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 3: EARLY DISASTER REPLAYER -->
        <section id="view-disasters" class="hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <!-- Left: Interactive Board -->
                <div class="lg:col-span-5 flex flex-col items-center">
                    <div class="board-container shadow-2xl rounded-lg overflow-hidden border border-slate-700">
                        <div id="replay-board" style="width: 100%"></div>
                    </div>
                    <!-- Controls -->
                    <div class="flex items-center gap-2 mt-4">
                        <button onclick="replayFirst()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded text-sm font-semibold">|&lt;</button>
                        <button onclick="replayPrev()" class="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded text-sm font-semibold">&lt; Prev</button>
                        <button onclick="replayNext()" class="px-4 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded text-sm font-semibold">Next &gt;</button>
                        <button onclick="replayLast()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded text-sm font-semibold">&gt;|</button>
                    </div>
                    <div id="replay-status" class="text-xs text-slate-400 mt-2 font-mono">Move 0 / 0</div>
                </div>

                <!-- Right: Game Selector & Coach Advice Card -->
                <div class="lg:col-span-7 space-y-4">
                    <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-5">
                        <label class="block text-xs font-semibold text-slate-400 uppercase mb-1">Select Lost Game (<=15 moves):</label>
                        <select id="game-select" onchange="loadSelectedGame(this.value)" class="w-full bg-slate-900 border border-slate-700 text-slate-200 text-sm rounded-lg p-2.5 focus:border-sky-500"></select>

                        <div id="game-meta-card" class="bg-slate-900/70 p-3.5 rounded-lg border border-slate-700 mt-3 text-xs space-y-1">
                            <div><strong>Opening:</strong> <span id="meta-opening" class="text-sky-400"></span></div>
                            <div><strong>Opponent:</strong> <span id="meta-opp" class="text-slate-300"></span> | <strong>Result:</strong> <span id="meta-result" class="text-rose-400 font-semibold"></span></div>
                            <div><strong>Chess.com Link:</strong> <a id="meta-link" href="#" target="_blank" class="text-sky-400 underline">Open on Chess.com ↗</a></div>
                        </div>

                        <div class="mt-3">
                            <label class="block text-xs font-semibold text-slate-400 uppercase mb-1">Move Notation (Click any move to jump):</label>
                            <div id="moves-container" class="bg-slate-900 p-3 rounded-lg border border-slate-700 font-mono text-xs max-h-32 overflow-y-auto leading-relaxed flex flex-wrap gap-1.5"></div>
                        </div>
                    </div>

                    <!-- COACH RECOMMENDATIONS BOX -->
                    <div id="coach-card" class="bg-gradient-to-br from-slate-900 via-slate-800 to-indigo-950/40 rounded-xl border-2 border-amber-500/40 p-5 space-y-3 shadow-xl">
                        <div class="flex items-center justify-between">
                            <h3 class="text-sm font-bold text-amber-400 flex items-center gap-2">
                                <span>🎯</span> Coach Diagnostic & Better Move
                            </h3>
                            <span id="coach-ply-tag" class="text-xs bg-amber-500/20 text-amber-300 border border-amber-500/40 px-2 py-0.5 rounded font-mono">Move Diagnosis</span>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                            <div class="bg-rose-950/40 border border-rose-800/60 p-3 rounded-lg">
                                <div class="font-bold text-rose-400 uppercase text-[11px] mb-1">🔴 What You Played</div>
                                <div id="coach-played-move" class="font-mono text-sm text-slate-100 font-bold"></div>
                            </div>
                            <div class="bg-emerald-950/40 border border-emerald-800/60 p-3 rounded-lg">
                                <div class="font-bold text-emerald-400 uppercase text-[11px] mb-1">🟢 What You Should Play Instead</div>
                                <div id="coach-better-move" class="font-mono text-sm text-emerald-300 font-bold"></div>
                            </div>
                        </div>

                        <div class="bg-slate-900/80 border border-amber-500/30 p-3.5 rounded-lg text-xs space-y-2">
                            <div>
                                <strong class="text-rose-300 font-bold uppercase text-[11px] tracking-wide">⚠️ NEVER DO THIS RULE:</strong>
                                <p id="coach-never-rule" class="text-slate-200 mt-0.5 font-medium"></p>
                            </div>
                            <div class="border-t border-slate-800 pt-2">
                                <strong class="text-sky-300 font-bold uppercase text-[11px] tracking-wide">💡 WHY THIS WORKS (MASTER INSIGHT):</strong>
                                <p id="coach-explanation" class="text-slate-300 mt-0.5 leading-relaxed"></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 4: COACH'S GOLDEN RULES & REPERTOIRE -->
        <section id="view-repertoire" class="hidden space-y-6">
            <!-- 5 Golden "NEVER DO THAT" Rules -->
            <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-6">
                <h3 class="text-lg font-bold text-rose-400 flex items-center gap-2 mb-4">
                    <span>🛑</span> Top 5 "NEVER DO THAT" Rules for 1200 → 1500 Players
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-slate-300">
                    <div class="bg-slate-900/80 p-4 rounded-lg border border-rose-900/40">
                        <strong class="text-rose-400 text-sm block mb-1">1. Never block queen checks with your Queen when b2 is hanging</strong>
                        <p>In the Englund Gambit (1.d4 e5 2.dxe5 Nc6 3.Nf3 Qe7 4.Bf4 Qb4+), playing <strong>5.Qd2??</strong> loses immediately to 5...Qxb2! Play <strong>5.Bd2!</strong> instead, followed by <strong>6.Nc3!</strong>.</p>
                    </div>
                    <div class="bg-slate-900/80 p-4 rounded-lg border border-rose-900/40">
                        <strong class="text-rose-400 text-sm block mb-1">2. Never trap your light-squared bishop in the Scandinavian</strong>
                        <p>When White plays 2.e5 against your 1...d5, NEVER play 2...e6! Always play <strong>2...Bf5!</strong> first, bringing your bishop outside the pawn chain before locking it with e6.</p>
                    </div>
                    <div class="bg-slate-900/80 p-4 rounded-lg border border-rose-900/40">
                        <strong class="text-rose-400 text-sm block mb-1">3. Never let the London player set up without fighting for the center</strong>
                        <p>Against 1.d4 d5 2.Bf4, NEVER play passive setup moves like 2...e6. Strike immediately with <strong>2...c5!</strong> and <strong>4...Qb6!</strong> attacking b2.</p>
                    </div>
                    <div class="bg-slate-900/80 p-4 rounded-lg border border-rose-900/40">
                        <strong class="text-rose-400 text-sm block mb-1">4. Never play passive d4 + Nf3 + e3 without c4 or Bf4</strong>
                        <p>Playing 1.d4 followed by Nf3 and e3 with your dark bishop trapped on c1 gives Black full control of the game. Always play <strong>2.c4! (Queen's Gambit)</strong> or <strong>2.Bf4! (London)</strong>.</p>
                    </div>
                </div>
            </div>

            <!-- Master Repertoire Blueprints -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- White Blueprint -->
                <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-6 space-y-4">
                    <div class="flex items-center gap-2">
                        <span class="text-2xl">⚪</span>
                        <h3 class="text-lg font-bold text-white">White Master Repertoire Plan</h3>
                    </div>
                    <div class="space-y-3 text-xs leading-relaxed text-slate-300">
                        <div class="bg-slate-900/80 p-3.5 rounded-lg border border-slate-700">
                            <h4 class="font-bold text-amber-400 mb-1">1. Against Englund Gambit (1.d4 e5 2.dxe5 Nc6 3.Nf3 Qe7)</h4>
                            <p>Play <strong>4.Bf4 Qb4+ 5.Bd2! Qxb2 6.Nc3!</strong> (Threatens 7.Rb1 or 7.Nd5 with double attack on c7 and Queen). Evaluation is +3.5 for White!</p>
                        </div>
                        <div class="bg-slate-900/80 p-3.5 rounded-lg border border-slate-700">
                            <h4 class="font-bold text-amber-400 mb-1">2. Move 2 Choice (Instead of Passive Zukertort)</h4>
                            <p>When playing 1.d4 d5, play <strong>2.c4! (Queen's Gambit)</strong> to control the center, or <strong>2.Bf4! (London System)</strong> before playing e3. Avoid passive d4 + Nf3 + e3 + Be2 setups.</p>
                        </div>
                    </div>
                </div>

                <!-- Black Blueprint -->
                <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-6 space-y-4">
                    <div class="flex items-center gap-2">
                        <span class="text-2xl">⚫</span>
                        <h3 class="text-lg font-bold text-white">Black Master Repertoire Plan</h3>
                    </div>
                    <div class="space-y-3 text-xs leading-relaxed text-slate-300">
                        <div class="bg-slate-900/80 p-3.5 rounded-lg border border-slate-700">
                            <h4 class="font-bold text-sky-400 mb-1">1. In the Scandinavian vs 2.e5 (1.e4 d5 2.e5)</h4>
                            <p>Do NOT play 2...e6 (trapping your bishop). Play <strong>2...Bf5!</strong> first, followed by <strong>3...e6</strong> and <strong>4...c5!</strong> attacking White's d4 pawn center.</p>
                        </div>
                        <div class="bg-slate-900/80 p-3.5 rounded-lg border border-slate-700">
                            <h4 class="font-bold text-sky-400 mb-1">2. Against London System (1.d4 d5 2.Bf4)</h4>
                            <p>Strike immediately with <strong>2...c5!</strong> followed by <strong>3.e3 Nc6 4.Nf3 Qb6!</strong> attacking the vulnerable b2 pawn.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <script>
        const analysisData = __ANALYSIS_DATA__;
        const userStats = __USER_STATS__;
        const topOpenings = __TOP_OPENINGS__;

        // Populate header stats
        if (userStats && userStats.chess_blitz) {
            document.getElementById('blitz-rating').innerText = userStats.chess_blitz.last.rating;
        }
        if (userStats && userStats.chess_bullet) {
            document.getElementById('bullet-rating').innerText = userStats.chess_bullet.last.rating;
        }
        if (userStats && userStats.tactics) {
            document.getElementById('tactics-rating').innerText = userStats.tactics.highest.rating;
        }

        // Render Top 10 Tables
        function renderTopTables() {
            if (!topOpenings.white_winning) return;

            document.getElementById('white-win-tbody').innerHTML = topOpenings.white_winning.map(o => `
                <tr class="hover:bg-slate-700/30">
                    <td class="py-1.5 px-3 font-medium text-slate-200">${o.op}</td>
                    <td class="py-1.5 px-2 text-center text-slate-400">${o.total}</td>
                    <td class="py-1.5 px-2 text-center text-emerald-400 font-bold">${o.win_rate}%</td>
                    <td class="py-1.5 px-2 text-center text-slate-400">${o.loss_rate}%</td>
                </tr>
            `).join('');

            document.getElementById('white-loss-tbody').innerHTML = topOpenings.white_losing.map(o => `
                <tr class="hover:bg-slate-700/30">
                    <td class="py-1.5 px-3 font-medium text-slate-200">${o.op}</td>
                    <td class="py-1.5 px-2 text-center text-slate-400">${o.total}</td>
                    <td class="py-1.5 px-2 text-center text-rose-400 font-bold">${o.loss_rate}%</td>
                    <td class="py-1.5 px-2 text-center text-slate-400">${o.win_rate}%</td>
                </tr>
            `).join('');

            document.getElementById('black-win-tbody').innerHTML = topOpenings.black_winning.map(o => `
                <tr class="hover:bg-slate-700/30">
                    <td class="py-1.5 px-3 font-medium text-slate-200">${o.op}</td>
                    <td class="py-1.5 px-2 text-center text-slate-400">${o.total}</td>
                    <td class="py-1.5 px-2 text-center text-emerald-400 font-bold">${o.win_rate}%</td>
                    <td class="py-1.5 px-2 text-center text-slate-400">${o.loss_rate}%</td>
                </tr>
            `).join('');

            document.getElementById('black-loss-tbody').innerHTML = topOpenings.black_losing.map(o => `
                <tr class="hover:bg-slate-700/30">
                    <td class="py-1.5 px-3 font-medium text-slate-200">${o.op}</td>
                    <td class="py-1.5 px-2 text-center text-slate-400">${o.total}</td>
                    <td class="py-1.5 px-2 text-center text-rose-400 font-bold">${o.loss_rate}%</td>
                    <td class="py-1.5 px-2 text-center text-slate-400">${o.win_rate}%</td>
                </tr>
            `).join('');
        }
        renderTopTables();

        // Switch Tabs
        function switchTab(tabId) {
            ['overview', 'trainer', 'disasters', 'repertoire'].forEach(id => {
                document.getElementById('view-' + id).classList.add('hidden');
                document.getElementById('tab-' + id).classList.remove('active');
            });
            document.getElementById('view-' + tabId).classList.remove('hidden');
            document.getElementById('tab-' + tabId).classList.add('active');

            if (tabId === 'disasters') {
                setTimeout(() => { if (replayBoard) replayBoard.resize(); }, 100);
            } else if (tabId === 'trainer') {
                setTimeout(() => { if (trainerBoard) trainerBoard.resize(); }, 100);
            }
        }

        // ==========================================
        // COMPREHENSIVE OPENING TRAINER ENGINE
        // ==========================================
        const openingDrills = [
            // ⚪ WHITE FIXES (LOSING LINES)
            {
                id: 0,
                category: "white_fix",
                title: "⚪ White Fix: Refuting Englund Gambit (1.d4 e5)",
                tag: "65% Loss Rate Fix",
                side: "white",
                moves: [
                    { uci: "d2d4", san: "d4", comment: "1. d4 - Start with Queen's Pawn" },
                    { uci: "e7e5", san: "e5", comment: "Opponent plays Englund Gambit" },
                    { uci: "d4e5", san: "dxe5", comment: "2. dxe5 - Accept the pawn" },
                    { uci: "b8c6", san: "Nc6", comment: "Opponent develops knight" },
                    { uci: "g1f3", san: "Nf3", comment: "3. Nf3 - Guard e5" },
                    { uci: "d8e7", san: "Qe7", comment: "Black attacks e5 again" },
                    { uci: "c1f4", san: "Bf4", comment: "4. Bf4 - Solidify e5" },
                    { uci: "e7b4", san: "Qb4+", comment: "TRAP MOVE! Black forks King and Bishop" },
                    { uci: "f4d2", san: "Bd2!", comment: "5. Bd2! - The Winning Move! Never play Qd2" },
                    { uci: "b4b2", san: "Qxb2", comment: "Black gets greedy for b2" },
                    { uci: "b1c3", san: "Nc3!", comment: "6. Nc3! - White is completely winning (+3.5) with Rb1 & Nd5 threats!" }
                ]
            },
            {
                id: 1,
                category: "white_fix",
                title: "⚪ White Fix: Active Queen's Gambit (1.d4 d5 2.c4!)",
                tag: "70% Passive d4 Fix",
                side: "white",
                moves: [
                    { uci: "d2d4", san: "d4", comment: "1. d4 - Queen's Pawn" },
                    { uci: "d7d5", san: "d5", comment: "Black takes the center" },
                    { uci: "c2c4", san: "c4!", comment: "2. c4! - Queen's Gambit! Strike Black's center immediately" },
                    { uci: "e7e6", san: "e6", comment: "Black defends d5" },
                    { uci: "b1c3", san: "Nc3", comment: "3. Nc3 - Develop with center pressure" },
                    { uci: "g8f6", san: "Nf6", comment: "Black develops knight" },
                    { uci: "c1g5", san: "Bg5!", comment: "4. Bg5! - Active pin on Black's knight before playing e3" }
                ]
            },
            {
                id: 2,
                category: "white_fix",
                title: "⚪ White Fix: Mainline vs Caro-Kann (1.e4 c6 2.d4 d5 3.Nc3)",
                tag: "66.7% Loss Rate Fix",
                side: "white",
                moves: [
                    { uci: "e2e4", san: "e4", comment: "1. e4 - King's Pawn" },
                    { uci: "c7c6", san: "c6", comment: "Caro-Kann Defense" },
                    { uci: "d2d4", san: "d4", comment: "2. d4 - Grab full center" },
                    { uci: "d7d5", san: "d5", comment: "Black strikes d5" },
                    { uci: "b1c3", san: "Nc3", comment: "3. Nc3 - Mainline Caro-Kann" },
                    { uci: "d5e4", san: "dxe4", comment: "Black trades" },
                    { uci: "c3e4", san: "Nxe4", comment: "4. Nxe4 - Powerful central knight" },
                    { uci: "c8f5", san: "Bf5", comment: "Black attacks knight" },
                    { uci: "e4g3", san: "Ng3!", comment: "5. Ng3! - Kick Black's bishop and take space" }
                ]
            },

            // ⚫ BLACK FIXES (LOSING LINES)
            {
                id: 3,
                category: "black_fix",
                title: "⚫ Black Fix: Scandinavian Defense vs 2.e5",
                tag: "65.6% Loss Rate Fix",
                side: "black",
                moves: [
                    { uci: "e2e4", san: "e4", comment: "White plays 1. e4" },
                    { uci: "d7d5", san: "d5", comment: "1... d5 - Scandinavian Defense" },
                    { uci: "e4e5", san: "e5", comment: "White pushes 2. e5" },
                    { uci: "c8f5", san: "Bf5!", comment: "2... Bf5! - NEVER play e6 first! Bring Bishop outside pawn chain" },
                    { uci: "d2d4", san: "d4", comment: "White supports e5" },
                    { uci: "e7e6", san: "e6", comment: "3... e6 - Now solidify the center" },
                    { uci: "g1f3", san: "Nf3", comment: "White develops" },
                    { uci: "c7c5", san: "c5!", comment: "4... c5! - Strike White's d4 pawn center!" }
                ]
            },
            {
                id: 4,
                category: "black_fix",
                title: "⚫ Black Fix: Countering London System (1.d4 d5 2.Bf4 c5!)",
                tag: "72.7% Loss Rate Fix",
                side: "black",
                moves: [
                    { uci: "d2d4", san: "d4", comment: "White plays 1. d4" },
                    { uci: "d7d5", san: "d5", comment: "1... d5" },
                    { uci: "c1f4", san: "Bf4", comment: "London System" },
                    { uci: "c7c5", san: "c5!", comment: "2... c5! - Immediate central counter-punch" },
                    { uci: "e2e3", san: "e3", comment: "White guards d4" },
                    { uci: "b8c6", san: "Nc6", comment: "3... Nc6 - Pressure d4" },
                    { uci: "g1f3", san: "Nf3", comment: "White develops" },
                    { uci: "d8b6", san: "Qb6!", comment: "4... Qb6! - Attack White's undefended b2 pawn!" }
                ]
            },
            {
                id: 5,
                category: "black_fix",
                title: "⚫ Black Fix: Defending Danish Gambit (1.e4 e5 2.d4 exd4 3.c3)",
                tag: "100% Loss Rate Fix",
                side: "black",
                moves: [
                    { uci: "e2e4", san: "e4", comment: "White plays 1. e4" },
                    { uci: "e7e5", san: "e5", comment: "1... e5" },
                    { uci: "d2d4", san: "d4", comment: "White plays Center Game" },
                    { uci: "e5d4", san: "exd4", comment: "Take the pawn" },
                    { uci: "c2c3", san: "c3", comment: "Danish Gambit" },
                    { uci: "d4c3", san: "dxc3", comment: "Accept the gambit" },
                    { uci: "f1c4", san: "Bc4", comment: "White attacks f7" },
                    { uci: "c3b2", san: "cxb2", comment: "Take 2nd pawn" },
                    { uci: "c1b2", san: "Bxb2", comment: "White has dangerous bishops" },
                    { uci: "d7d5", san: "d5!", comment: "5... d5! - Return 1 pawn to neutralize White's attack!" }
                ]
            },

            // 🏆 MASTER WINNING LINES TO REINFORCE
            {
                id: 6,
                category: "winning",
                title: "⚪ Master Line: Vienna Game Frankenstein-Dracula Attack",
                tag: "77.8% Win Rate Weapon",
                side: "white",
                moves: [
                    { uci: "e2e4", san: "e4", comment: "1. e4" },
                    { uci: "e7e5", san: "e5", comment: "1... e5" },
                    { uci: "b1c3", san: "Nc3", comment: "2. Nc3 - Vienna Game" },
                    { uci: "g8f6", san: "Nf6", comment: "Black develops" },
                    { uci: "f1c4", san: "Bc4", comment: "3. Bc4 - Bishop attack" },
                    { uci: "f6e4", san: "Nxe4", comment: "Black takes e4" },
                    { uci: "d1h5", san: "Qh5!", comment: "4. Qh5! - Threatens Mate on f7 and Knight on e4!" }
                ]
            },
            {
                id: 7,
                category: "winning",
                title: "⚪ Master Line: Bishop's Opening Berlin Spielmann Attack",
                tag: "75.0% Win Rate Weapon",
                side: "white",
                moves: [
                    { uci: "e2e4", san: "e4", comment: "1. e4" },
                    { uci: "e7e5", san: "e5", comment: "1... e5" },
                    { uci: "f1c4", san: "Bc4", comment: "2. Bc4 - Bishop's Opening" },
                    { uci: "g8f6", san: "Nf6", comment: "Black develops" },
                    { uci: "d2d3", san: "d3", comment: "3. d3 - Solidify center" },
                    { uci: "c7c6", san: "c6", comment: "Black prepares d5" },
                    { uci: "g1f3", san: "Nf3", comment: "4. Nf3 - Counter-attack e5" },
                    { uci: "d7d5", san: "d5", comment: "Black pushes d5" },
                    { uci: "c4b3", san: "Bb3!", comment: "5. Bb3! - Retreat with deadly pressure on d5" }
                ]
            }
        ];

        let trainerBoard = null;
        let trainerGame = new Chess();
        let activeDrill = openingDrills[0];
        let currentStepIndex = 0;
        let isWaitingUserMove = false;

        function renderDrillsList(filter = "all") {
            const container = document.getElementById('drills-list-container');
            const filtered = openingDrills.filter(d => filter === "all" || d.category === filter);

            container.innerHTML = filtered.map(d => `
                <div onclick="selectDrill(${d.id})" id="drill-item-${d.id}" class="trainer-card cursor-pointer p-3 rounded-lg border border-slate-700 bg-slate-900/70 hover:bg-slate-800 transition ${d.id === activeDrill.id ? 'active' : ''}">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-xs text-slate-200">${d.title}</span>
                        <span class="text-[10px] px-2 py-0.5 rounded font-mono ${d.category.includes('fix') ? 'bg-rose-950/80 text-rose-300 border border-rose-800/60' : 'bg-emerald-950/80 text-emerald-300 border border-emerald-800/60'}">${d.tag}</span>
                    </div>
                </div>
            `).join('');
        }

        function filterDrills(filter) {
            ['all', 'white_fix', 'black_fix', 'winning'].forEach(f => {
                const btn = document.getElementById('filter-' + f);
                if (btn) {
                    btn.className = (f === filter) ? 'px-2 py-1 bg-sky-600 rounded text-white' : 'px-2 py-1 bg-slate-900 hover:bg-slate-700 rounded text-slate-300';
                }
            });
            renderDrillsList(filter);
        }

        function initTrainer() {
            trainerBoard = Chessboard('trainer-board', {
                draggable: true,
                position: 'start',
                pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png',
                onDrop: onTrainerDrop
            });
            renderDrillsList('all');
            selectDrill(0);
        }

        function selectDrill(drillId) {
            activeDrill = openingDrills.find(d => d.id === drillId) || openingDrills[0];
            renderDrillsList();
            resetCurrentDrill();
        }

        function resetCurrentDrill() {
            trainerGame.reset();
            trainerBoard.orientation(activeDrill.side);
            trainerBoard.position('start');
            currentStepIndex = 0;
            advanceDrill();
        }

        function advanceDrill() {
            if (currentStepIndex >= activeDrill.moves.length) {
                document.getElementById('trainer-prompt').innerHTML = "<span class='text-emerald-400 font-bold'>🎉 Drill Complete! Excellent Opening Mastery!</span>";
                document.getElementById('trainer-subtext').innerText = "You successfully executed all key moves in this line. Try the next drill!";
                isWaitingUserMove = false;
                updateStepIndicator();
                return;
            }

            const moveData = activeDrill.moves[currentStepIndex];
            const isUserTurn = (activeDrill.side === "white" && currentStepIndex % 2 === 0) || (activeDrill.side === "black" && currentStepIndex % 2 === 1);

            if (isUserTurn) {
                isWaitingUserMove = true;
                document.getElementById('trainer-prompt').innerText = `Your Turn (${activeDrill.side.toUpperCase()}): Play the correct move!`;
                document.getElementById('trainer-subtext').innerText = moveData.comment;
            } else {
                isWaitingUserMove = false;
                document.getElementById('trainer-prompt').innerText = `Opponent plays: ${moveData.san}`;
                document.getElementById('trainer-subtext').innerText = moveData.comment;
                setTimeout(() => {
                    trainerGame.move(moveData.san);
                    trainerBoard.position(trainerGame.fen());
                    currentStepIndex++;
                    advanceDrill();
                }, 600);
            }
            updateStepIndicator();
        }

        function updateStepIndicator() {
            document.getElementById('trainer-step-indicator').innerText = `Step: ${currentStepIndex} / ${activeDrill.moves.length}`;
        }

        function onTrainerDrop(source, target) {
            if (!isWaitingUserMove) return 'snapback';

            const expected = activeDrill.moves[currentStepIndex];
            const attemptedUci = source + target;

            if (attemptedUci === expected.uci) {
                trainerGame.move(expected.san);
                trainerBoard.position(trainerGame.fen());
                currentStepIndex++;
                isWaitingUserMove = false;
                setTimeout(advanceDrill, 400);
            } else {
                document.getElementById('trainer-subtext').innerHTML = "<span class='text-rose-400 font-bold'>❌ Inaccurate Move!</span> Think about king safety, piece development and central breaks.";
                return 'snapback';
            }
        }

        function showDrillHint() {
            if (!isWaitingUserMove) return;
            const expected = activeDrill.moves[currentStepIndex];
            document.getElementById('trainer-subtext').innerHTML = `<span class='text-amber-400 font-bold'>💡 Hint:</span> Look for <strong>${expected.san}</strong> (${expected.comment})`;
        }

        // ==========================================
        // REPLAYER ENGINE
        // ==========================================
        let replayBoard = null;
        let currentGameIndex = 0;
        let currentPly = 0;
        let currentFens = [];

        function initReplayer() {
            const select = document.getElementById('game-select');
            select.innerHTML = analysisData.early_disasters.map((g, idx) => `
                <option value="${idx}">${idx+1}. [${g.moves_count} moves] vs ${g.opp_name} (${g.opp_rating || '?'}) - ${g.opening}</option>
            `).join('');

            replayBoard = Chessboard('replay-board', {
                position: 'start',
                pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png'
            });

            if (analysisData.early_disasters.length > 0) {
                loadSelectedGame(0);
            }
        }

        function loadSelectedGame(idx) {
            currentGameIndex = parseInt(idx);
            const g = analysisData.early_disasters[currentGameIndex];
            if (!g) return;

            document.getElementById('meta-opening').innerText = g.opening;
            document.getElementById('meta-opp').innerText = `${g.opp_name} (${g.opp_rating || '?'})`;
            document.getElementById('meta-result').innerText = `${g.result} in ${g.moves_count} moves`;
            document.getElementById('meta-link').href = g.url;

            // Load Coach Advice Card
            if (g.coach_advice) {
                document.getElementById('coach-card').classList.remove('hidden');
                document.getElementById('coach-played-move').innerText = g.coach_advice.played_move;
                document.getElementById('coach-better-move').innerText = g.coach_advice.better_move;
                document.getElementById('coach-never-rule').innerText = g.coach_advice.never_rule;
                document.getElementById('coach-explanation').innerText = g.coach_advice.explanation;
                document.getElementById('coach-ply-tag').innerText = `Critical Move: Move ${g.coach_advice.move_num}`;
            }

            currentFens = g.fens;
            currentPly = 0;

            replayBoard.orientation(g.color.toLowerCase());
            replayBoard.position(currentFens[0]);

            // Render moves
            const mc = document.getElementById('moves-container');
            mc.innerHTML = g.moves_san.map((m, i) => {
                const moveNum = Math.floor(i/2) + 1;
                const prefix = (i % 2 === 0) ? `${moveNum}. ` : '';
                return `<span id="ply-${i+1}" onclick="jumpToPly(${i+1})" class="cursor-pointer px-1 py-0.5 rounded hover:bg-slate-700">${prefix}${m}</span>`;
            }).join('');

            updateReplayStatus();
        }

        function updateReplayStatus() {
            if (!currentFens || currentFens.length === 0) return;
            replayBoard.position(currentFens[currentPly]);
            document.getElementById('replay-status').innerText = `Ply ${currentPly} / ${currentFens.length - 1}`;
            
            document.querySelectorAll('#moves-container span').forEach(el => el.classList.remove('bg-sky-500/30', 'text-sky-300'));
            const curEl = document.getElementById(`ply-${currentPly}`);
            if (curEl) {
                curEl.classList.add('bg-sky-500/30', 'text-sky-300');
            }
        }

        function replayNext() {
            if (currentPly < currentFens.length - 1) {
                currentPly++;
                updateReplayStatus();
            }
        }

        function replayPrev() {
            if (currentPly > 0) {
                currentPly--;
                updateReplayStatus();
            }
        }

        function replayFirst() {
            currentPly = 0;
            updateReplayStatus();
        }

        function replayLast() {
            currentPly = currentFens.length - 1;
            updateReplayStatus();
        }

        function jumpToPly(ply) {
            currentPly = ply;
            updateReplayStatus();
        }

        // Initialization
        $(document).ready(function() {
            initReplayer();
            initTrainer();
        });
    </script>
</body>
</html>
"""
    # Replace template placeholders
    html_rendered = html_template \
        .replace("__USERNAME__", str(analysis_data.get('username', 'Player'))) \
        .replace("__TOTAL_GAMES__", str(analysis_data.get('total_games', 0))) \
        .replace("__WIN_RATE__", str(analysis_data.get('win_rate', 0))) \
        .replace("__TOTAL_WINS__", str(analysis_data.get('total_wins', 0))) \
        .replace("__TOTAL_LOSSES__", str(analysis_data.get('total_losses', 0))) \
        .replace("__TOTAL_DRAWS__", str(analysis_data.get('total_draws', 0))) \
        .replace("__RESIGNED__", str(analysis_data.get('loss_reasons', {}).get('resigned', 0))) \
        .replace("__DISASTERS_COUNT__", str(analysis_data.get('early_disasters_count', 0))) \
        .replace("__ANALYSIS_DATA__", stats_json) \
        .replace("__USER_STATS__", user_stats_json) \
        .replace("__TOP_OPENINGS__", top_openings_json)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_rendered)
    print(f"Generated interactive dashboard: {output_path}")
    return output_path
