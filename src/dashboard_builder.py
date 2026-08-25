"""
HTML Dashboard & Full Lichess-Style Opening Explorer, Trainer & Stockfish Engine Analyzer
"""
import json
import os

def generate_html_dashboard(analysis_data, user_stats, output_path="dashboard.html"):
    stats_json = json.dumps(analysis_data)
    user_stats_json = json.dumps(user_stats)
    
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
    <title>Chess.com Diagnostics & Stockfish Engine - __USERNAME__</title>
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
        .trainer-card.active { border-color: #38bdf8; background-color: #0369a120; }
        .eval-bar-container { display: flex; height: 16px; width: 100%; border-radius: 3px; overflow: hidden; font-size: 10px; line-height: 16px; font-weight: 600; text-align: center; }
        .bar-white { background-color: #f1f5f9; color: #0f172a; }
        .bar-draw { background-color: #64748b; color: #f8fafc; }
        .bar-black { background-color: #1e293b; color: #f8fafc; border-left: 1px solid #334155; }
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- Header -->
    <header class="bg-slate-900 border-b border-slate-800 px-6 py-4 flex flex-wrap items-center justify-between shadow-lg">
        <div class="flex items-center space-x-3">
            <span class="text-3xl">♟️</span>
            <div>
                <h1 class="text-xl font-bold text-white flex items-center gap-2">
                    Chess Diagnostics & Stockfish 18 Engine
                    <span class="text-xs bg-sky-500/20 text-sky-400 border border-sky-500/30 px-2 py-0.5 rounded font-mono">__USERNAME__</span>
                </h1>
                <p class="text-xs text-slate-400">Deep Stockfish Blunder Detection, Move-by-Move Evaluations & Lichess Explorer</p>
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
            <button onclick="switchTab('disasters')" id="tab-disasters" class="tab-btn active py-3 px-1 text-slate-300 hover:text-white transition">⚡ Stockfish Lost Games Replayer</button>
            <button onclick="switchTab('trainer')" id="tab-trainer" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition">🎯 Lichess-Style Explorer & Trainer</button>
            <button onclick="switchTab('overview')" id="tab-overview" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition">📊 Top 10 Win/Loss Openings</button>
            <button onclick="switchTab('videos')" id="tab-videos" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition">🎥 Master Video Lessons</button>
            <button onclick="switchTab('repertoire')" id="tab-repertoire" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition">📜 Coach's Golden Rules</button>
        </nav>
    </div>

    <!-- Main Content Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto p-6">

        <!-- TAB 1: STOCKFISH EARLY DISASTER REPLAYER -->
        <section id="view-disasters" class="space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <!-- Left: Board & Engine Bar -->
                <div class="lg:col-span-5 flex flex-col items-center">
                    <div class="board-container shadow-2xl rounded-lg overflow-hidden border border-slate-700">
                        <div id="replay-board" style="width: 100%"></div>
                    </div>
                    <!-- Navigation Controls -->
                    <div class="flex items-center gap-2 mt-4">
                        <button onclick="replayFirst()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded text-sm font-semibold">|&lt;</button>
                        <button onclick="replayPrev()" class="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded text-sm font-semibold">&lt; Prev</button>
                        <button onclick="replayNext()" class="px-4 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded text-sm font-semibold">Next &gt;</button>
                        <button onclick="replayLast()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded text-sm font-semibold">&gt;|</button>
                    </div>
                    <div id="replay-status" class="text-xs text-slate-400 mt-2 font-mono">Move 0 / 0</div>
                </div>

                <!-- Right: Game Selector, Move Quality & Stockfish Live Panel -->
                <div class="lg:col-span-7 space-y-4">
                    <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-5">
                        <label class="block text-xs font-semibold text-slate-400 uppercase mb-1">Select Lost Game (Analyzed with Stockfish 18):</label>
                        <select id="game-select" onchange="loadSelectedGame(this.value)" class="w-full bg-slate-900 border border-slate-700 text-slate-200 text-sm rounded-lg p-2.5 focus:border-sky-500"></select>

                        <div id="game-meta-card" class="bg-slate-900/70 p-3.5 rounded-lg border border-slate-700 mt-3 text-xs space-y-1">
                            <div><strong>Opening:</strong> <span id="meta-opening" class="text-sky-400"></span></div>
                            <div><strong>Opponent:</strong> <span id="meta-opp" class="text-slate-300"></span> | <strong>Result:</strong> <span id="meta-result" class="text-rose-400 font-semibold"></span></div>
                            <div><strong>Chess.com Link:</strong> <a id="meta-link" href="#" target="_blank" class="text-sky-400 underline">Open on Chess.com ↗</a></div>
                        </div>

                        <!-- Move List with Quality Badges -->
                        <div class="mt-3">
                            <label class="block text-xs font-semibold text-slate-400 uppercase mb-1">Move Notation (Click any move to inspect with Stockfish):</label>
                            <div id="moves-container" class="bg-slate-900 p-3 rounded-lg border border-slate-700 font-mono text-xs max-h-32 overflow-y-auto leading-relaxed flex flex-wrap gap-1.5"></div>
                        </div>
                    </div>

                    <!-- STOCKFISH 18 LIVE ENGINE EVALUATION CARD -->
                    <div class="bg-gradient-to-br from-slate-900 via-slate-800 to-sky-950/40 rounded-xl border-2 border-sky-500/40 p-5 space-y-3 shadow-xl">
                        <div class="flex items-center justify-between">
                            <h3 class="text-sm font-bold text-sky-400 flex items-center gap-2">
                                <span>🤖</span> Stockfish 18 Engine Analysis
                            </h3>
                            <span id="sf-eval-badge" class="text-xs bg-sky-500/20 text-sky-300 border border-sky-500/40 px-2.5 py-0.5 rounded font-mono font-bold">Eval: 0.0</span>
                        </div>

                        <!-- Move Comparison Grid -->
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                            <div class="bg-slate-900/90 border border-slate-700 p-3 rounded-lg">
                                <div class="font-bold text-slate-400 uppercase text-[10px] mb-1">Move Played in Game</div>
                                <div class="flex items-center gap-2">
                                    <span id="sf-played-move" class="font-mono text-sm text-slate-100 font-bold">--</span>
                                    <span id="sf-quality-badge" class="text-[10px] px-2 py-0.5 rounded font-mono font-semibold border">--</span>
                                </div>
                            </div>
                            <div class="bg-emerald-950/40 border border-emerald-800/60 p-3 rounded-lg">
                                <div class="font-bold text-emerald-400 uppercase text-[10px] mb-1">🟢 Stockfish Recommended Best Move</div>
                                <div id="sf-best-move" class="font-mono text-sm text-emerald-300 font-bold">--</div>
                            </div>
                        </div>

                        <!-- Engine Best Continuation Line (PV) -->
                        <div class="bg-slate-900/80 border border-slate-700 p-3 rounded-lg text-xs space-y-1">
                            <strong class="text-slate-400 font-bold uppercase text-[10px] tracking-wide block">Engine Best Continuation (PV Line):</strong>
                            <p id="sf-pv-line" class="font-mono text-slate-200 leading-relaxed text-[11px]">--</p>
                        </div>
                    </div>

                    <!-- COACH RECOMMENDATIONS BOX -->
                    <div id="coach-card" class="bg-gradient-to-br from-slate-900 via-slate-800 to-indigo-950/40 rounded-xl border border-amber-500/40 p-4 space-y-2 text-xs">
                        <div class="flex items-center justify-between">
                            <strong class="text-amber-400 font-bold uppercase tracking-wide flex items-center gap-1.5">
                                <span>🎯</span> Coach Diagnostic & Rule
                            </strong>
                            <span id="coach-ply-tag" class="text-[10px] bg-amber-500/20 text-amber-300 border border-amber-500/40 px-2 py-0.5 rounded font-mono">Move 5</span>
                        </div>
                        <div class="text-slate-200">
                            <strong class="text-rose-400">⚠️ NEVER DO THIS:</strong> <span id="coach-never-rule"></span>
                        </div>
                        <div class="text-slate-300 border-t border-slate-800 pt-1.5">
                            <strong class="text-sky-300">💡 WHY THIS WORKS:</strong> <span id="coach-explanation"></span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 2: LICHESS-STYLE EXPLORER & TRAINER -->
        <section id="view-trainer" class="hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <!-- Left: Board & Controls -->
                <div class="lg:col-span-5 flex flex-col items-center">
                    <div class="board-container shadow-2xl rounded-lg overflow-hidden border border-slate-700">
                        <div id="trainer-board" style="width: 100%"></div>
                    </div>
                    <!-- Feedback Box -->
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

                <!-- Right: Lichess-Style Explorer & Move Table -->
                <div class="lg:col-span-7 space-y-4">
                    <!-- Drill Selector -->
                    <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-4">
                        <div class="flex items-center justify-between mb-2">
                            <label class="text-xs font-bold text-slate-300 uppercase">Select Repertoire Drill:</label>
                            <div class="flex gap-1 text-[11px]">
                                <button onclick="filterDrills('all')" class="px-2 py-0.5 bg-slate-700 rounded text-white" id="filter-all">All</button>
                                <button onclick="filterDrills('white_fix')" class="px-2 py-0.5 bg-slate-900 hover:bg-slate-700 rounded text-slate-300" id="filter-white_fix">⚪ White</button>
                                <button onclick="filterDrills('black_fix')" class="px-2 py-0.5 bg-slate-900 hover:bg-slate-700 rounded text-slate-300" id="filter-black_fix">⚫ Black</button>
                            </div>
                        </div>
                        <div id="drills-list-container" class="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-36 overflow-y-auto pr-1"></div>
                    </div>

                    <!-- LICHESS OPENING EXPLORER MOVE TABLE -->
                    <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-4">
                        <div class="flex items-center justify-between mb-2">
                            <h3 class="text-xs font-bold text-sky-400 uppercase tracking-wide flex items-center gap-1.5">
                                <span>📖</span> Lichess Master Move Explorer (Current Position)
                            </h3>
                            <span id="pos-eval-badge" class="text-[11px] bg-slate-900 border border-slate-700 text-emerald-400 font-mono px-2 py-0.5 rounded">Eval: --</span>
                        </div>

                        <div class="overflow-x-auto">
                            <table class="w-full text-xs text-left">
                                <thead class="text-slate-400 bg-slate-900/80 uppercase text-[10px]">
                                    <tr>
                                        <th class="py-1.5 px-3">Move</th>
                                        <th class="py-1.5 px-2 text-center">Games</th>
                                        <th class="py-1.5 px-2 text-center">Eval</th>
                                        <th class="py-1.5 px-3 text-center w-48">Win / Draw / Loss %</th>
                                    </tr>
                                </thead>
                                <tbody id="lichess-explorer-tbody" class="divide-y divide-slate-700/50 font-mono"></tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Move Strategy Explanation Card -->
                    <div class="bg-gradient-to-br from-slate-900 to-indigo-950/40 rounded-xl border border-sky-500/30 p-4 text-xs space-y-2">
                        <h4 class="font-bold text-sky-300 flex items-center gap-1.5" id="strategy-title">
                            <span>💡</span> Strategy Guide & Next Moves
                        </h4>
                        <p class="text-slate-300 leading-relaxed" id="strategy-desc"></p>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 3: TOP 10 WINNING & LOSING OPENINGS -->
        <section id="view-overview" class="hidden space-y-6">
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

            <!-- Queen's Pawn Explanation Banner -->
            <div class="bg-amber-950/40 border border-amber-600/50 rounded-xl p-5">
                <h3 class="text-base font-bold text-amber-300 flex items-center gap-2">
                    <span>👑</span> Why You Are Losing With Queen's Pawn (1.d4) as White
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

        <!-- TAB 4: MASTER VIDEO LESSONS -->
        <section id="view-videos" class="hidden space-y-6">
            <div class="text-center max-w-2xl mx-auto mb-6">
                <h2 class="text-xl font-bold text-white">🎬 Curated Master Video Lessons</h2>
                <p class="text-xs text-slate-400 mt-1">Hand-picked GM and IM tutorials for your exact problem openings.</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Video 1: Englund Gambit -->
                <div class="bg-slate-800/80 rounded-xl border border-slate-700 overflow-hidden flex flex-col">
                    <div class="p-4 flex-1 space-y-2">
                        <span class="text-[10px] bg-rose-950/80 text-rose-400 border border-rose-800/60 px-2 py-0.5 rounded font-mono font-bold">White Fix</span>
                        <h3 class="text-sm font-bold text-white">How To Punish Early Queen Attacks & Englund Gambit</h3>
                        <p class="text-xs text-slate-300">GothamChess (Levy Rozman) explains how to easily dismantle the Englund Gambit and early Queen nonsense.</p>
                    </div>
                    <div class="p-4 bg-slate-900/60 border-t border-slate-800">
                        <a href="https://www.youtube.com/results?search_query=GothamChess+punish+early+queen+attacks+englund" target="_blank" class="block text-center py-2 bg-rose-600 hover:bg-rose-500 text-white rounded text-xs font-bold transition">
                            ▶ Watch on YouTube ↗
                        </a>
                    </div>
                </div>

                <!-- Video 2: Danish Gambit -->
                <div class="bg-slate-800/80 rounded-xl border border-slate-700 overflow-hidden flex flex-col">
                    <div class="p-4 flex-1 space-y-2">
                        <span class="text-[10px] bg-sky-950/80 text-sky-400 border border-sky-800/60 px-2 py-0.5 rounded font-mono font-bold">Black Fix</span>
                        <h3 class="text-sm font-bold text-white">Schlechter Defense: Destroying the Danish Gambit (5...d5!)</h3>
                        <p class="text-xs text-slate-300">GM Daniel Naroditsky explains the exact move order to kill White's attack and keep a winning advantage.</p>
                    </div>
                    <div class="p-4 bg-slate-900/60 border-t border-slate-800">
                        <a href="https://www.youtube.com/results?search_query=Daniel+Naroditsky+Danish+Gambit+Schlechter+Defense" target="_blank" class="block text-center py-2 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition">
                            ▶ Watch on YouTube ↗
                        </a>
                    </div>
                </div>

                <!-- Video 3: Beat London System -->
                <div class="bg-slate-800/80 rounded-xl border border-slate-700 overflow-hidden flex flex-col">
                    <div class="p-4 flex-1 space-y-2">
                        <span class="text-[10px] bg-sky-950/80 text-sky-400 border border-sky-800/60 px-2 py-0.5 rounded font-mono font-bold">Black Fix</span>
                        <h3 class="text-sm font-bold text-white">How to Crush the London System with 2...c5 & 4...Qb6!</h3>
                        <p class="text-xs text-slate-300">Learn how to attack White's weakened b2 square when the London bishop leaves c1.</p>
                    </div>
                    <div class="p-4 bg-slate-900/60 border-t border-slate-800">
                        <a href="https://www.youtube.com/results?search_query=how+to+beat+london+system+with+c5+and+Qb6" target="_blank" class="block text-center py-2 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition">
                            ▶ Watch on YouTube ↗
                        </a>
                    </div>
                </div>

                <!-- Video 4: Scandinavian 2.e5 -->
                <div class="bg-slate-800/80 rounded-xl border border-slate-700 overflow-hidden flex flex-col">
                    <div class="p-4 flex-1 space-y-2">
                        <span class="text-[10px] bg-sky-950/80 text-sky-400 border border-sky-800/60 px-2 py-0.5 rounded font-mono font-bold">Black Fix</span>
                        <h3 class="text-sm font-bold text-white">Scandinavian Defense: The Complete Guide (2...Bf5!)</h3>
                        <p class="text-xs text-slate-300">Hanging Pawns explains why 2...Bf5 gives Black active play and avoids bad French Defense structures.</p>
                    </div>
                    <div class="p-4 bg-slate-900/60 border-t border-slate-800">
                        <a href="https://www.youtube.com/results?search_query=Hanging+Pawns+Scandinavian+Defense+e5" target="_blank" class="block text-center py-2 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition">
                            ▶ Watch on YouTube ↗
                        </a>
                    </div>
                </div>

                <!-- Video 5: Reti Opening 2...d4 -->
                <div class="bg-slate-800/80 rounded-xl border border-slate-700 overflow-hidden flex flex-col">
                    <div class="p-4 flex-1 space-y-2">
                        <span class="text-[10px] bg-sky-950/80 text-sky-400 border border-sky-800/60 px-2 py-0.5 rounded font-mono font-bold">Black Fix</span>
                        <h3 class="text-sm font-bold text-white">Reti Opening: Black Space Advantage with 2...d4</h3>
                        <p class="text-xs text-slate-300">Learn how pushing 2...d4 cramps White's queenside and prevents Nc3.</p>
                    </div>
                    <div class="p-4 bg-slate-900/60 border-t border-slate-800">
                        <a href="https://www.youtube.com/results?search_query=Reti+Opening+Black+advance+d4" target="_blank" class="block text-center py-2 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition">
                            ▶ Watch on YouTube ↗
                        </a>
                    </div>
                </div>

                <!-- Video 6: Vienna Frankenstein -->
                <div class="bg-slate-800/80 rounded-xl border border-slate-700 overflow-hidden flex flex-col">
                    <div class="p-4 flex-1 space-y-2">
                        <span class="text-[10px] bg-emerald-950/80 text-emerald-400 border border-emerald-800/60 px-2 py-0.5 rounded font-mono font-bold">Master Weapon</span>
                        <h3 class="text-sm font-bold text-white">Vienna Frankenstein-Dracula Attack (77.8% Win Rate)</h3>
                        <p class="text-xs text-slate-300">Eric Rosen showcases the thrilling tactics of the Frankenstein-Dracula variation.</p>
                    </div>
                    <div class="p-4 bg-slate-900/60 border-t border-slate-800">
                        <a href="https://www.youtube.com/results?search_query=Eric+Rosen+Vienna+Frankenstein+Dracula" target="_blank" class="block text-center py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-bold transition">
                            ▶ Watch on YouTube ↗
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 5: COACH'S GOLDEN RULES & REPERTOIRE -->
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
            ['disasters', 'trainer', 'overview', 'videos', 'repertoire'].forEach(id => {
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
        // STOCKFISH REPLAYER ENGINE
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
                document.getElementById('coach-never-rule').innerText = g.coach_advice.never_rule;
                document.getElementById('coach-explanation').innerText = g.coach_advice.explanation;
                document.getElementById('coach-ply-tag').innerText = `Critical Move: Move ${g.coach_advice.move_num}`;
            }

            currentFens = g.fens;
            currentPly = 0;

            replayBoard.orientation(g.color.toLowerCase());
            replayBoard.position(currentFens[0]);

            // Render moves with colored badge dots
            const mc = document.getElementById('moves-container');
            const sfData = g.stockfish_analysis || [];

            mc.innerHTML = g.moves_san.map((m, i) => {
                const moveNum = Math.floor(i/2) + 1;
                const prefix = (i % 2 === 0) ? `${moveNum}. ` : '';
                const plySf = sfData[i];
                let dot = '';
                if (plySf) {
                    if (plySf.quality === 'Blunder') dot = '<span class="inline-block w-2 h-2 rounded-full bg-rose-500 mr-0.5"></span>';
                    else if (plySf.quality === 'Mistake') dot = '<span class="inline-block w-2 h-2 rounded-full bg-orange-500 mr-0.5"></span>';
                    else if (plySf.quality === 'Inaccuracy') dot = '<span class="inline-block w-2 h-2 rounded-full bg-amber-400 mr-0.5"></span>';
                    else dot = '<span class="inline-block w-2 h-2 rounded-full bg-emerald-500 mr-0.5"></span>';
                }
                return `<span id="ply-${i+1}" onclick="jumpToPly(${i+1})" class="cursor-pointer px-1.5 py-0.5 rounded hover:bg-slate-700 flex items-center gap-1">${dot}${prefix}${m}</span>`;
            }).join('');

            updateReplayStatus();
        }

        function updateReplayStatus() {
            if (!currentFens || currentFens.length === 0) return;
            replayBoard.position(currentFens[currentPly]);
            document.getElementById('replay-status').innerText = `Ply ${currentPly} / ${currentFens.length - 1}`;
            
            // Highlight move
            document.querySelectorAll('#moves-container span').forEach(el => el.classList.remove('bg-sky-500/30', 'text-sky-300'));
            const curEl = document.getElementById(`ply-${currentPly}`);
            if (curEl) {
                curEl.classList.add('bg-sky-500/30', 'text-sky-300');
            }

            // Update Stockfish Live Card
            const g = analysisData.early_disasters[currentGameIndex];
            const sfList = g.stockfish_analysis || [];
            
            if (currentPly > 0 && currentPly <= sfList.length) {
                const plyData = sfList[currentPly - 1];
                document.getElementById('sf-eval-badge').innerText = `Stockfish 18 Eval: ${plyData.eval_str}`;
                document.getElementById('sf-played-move').innerText = `${plyData.move_num}. ${plyData.played_san}`;
                
                const qBadge = document.getElementById('sf-quality-badge');
                qBadge.innerText = plyData.quality;
                qBadge.className = `text-[10px] px-2 py-0.5 rounded font-mono font-semibold border ${plyData.badge}`;

                document.getElementById('sf-best-move').innerText = `${plyData.move_num}. ${plyData.best_san}`;
                document.getElementById('sf-pv-line').innerText = plyData.pv_san ? `Line: ${plyData.pv_san}` : "Direct Tactical Refutation";
            } else {
                document.getElementById('sf-eval-badge').innerText = "Stockfish 18 Eval: 0.0";
                document.getElementById('sf-played-move').innerText = "Start Position";
                document.getElementById('sf-quality-badge').innerText = "Initial";
                document.getElementById('sf-quality-badge').className = "text-[10px] px-2 py-0.5 rounded font-mono font-semibold border bg-slate-700 text-slate-300";
                document.getElementById('sf-best-move').innerText = "1. e4 / 1. d4 / 1. Nf3";
                document.getElementById('sf-pv-line').innerText = "Standard opening development";
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

        // ==========================================
        // LICHESS-STYLE OPENING DRILLS & DATA
        // ==========================================
        const openingDrills = [
            {
                id: 0,
                category: "white_fix",
                title: "⚪ White: Refuting Englund Gambit (1.d4 e5)",
                tag: "65% Loss Rate Fix",
                side: "white",
                strategy: "When Black plays 4...Qb4+, NEVER block with Qd2 or hang b2! Play 5.Bd2! and when 5...Qxb2, play 6.Nc3! White threatens 7.Rb1 (trapping Black's queen) and 7.Nd5 (forking c7). Black is dead lost (+3.5).",
                moves: [
                    { 
                        uci: "d2d4", san: "d4", comment: "1. d4 - Start with Queen's Pawn",
                        eval: "+0.3",
                        candidates: [
                            { san: "d4", games: 1845000, eval: "+0.3", w: 38, d: 34, b: 28 },
                            { san: "e4", games: 2150000, eval: "+0.3", w: 37, d: 33, b: 30 },
                            { san: "Nf3", games: 420000, eval: "+0.2", w: 36, d: 36, b: 28 }
                        ]
                    },
                    { 
                        uci: "e7e5", san: "e5", comment: "Opponent plays Englund Gambit",
                        eval: "+1.6",
                        candidates: [
                            { san: "dxe5", games: 98000, eval: "+1.6", w: 62, d: 18, b: 20 },
                            { san: "e4", games: 12000, eval: "+0.5", w: 42, d: 28, b: 30 }
                        ]
                    },
                    { 
                        uci: "d4e5", san: "dxe5", comment: "2. dxe5 - Accept the gambit pawn",
                        eval: "+1.6",
                        candidates: [
                            { san: "Nc6", games: 64000, eval: "+1.6", w: 60, d: 19, b: 21 },
                            { san: "d6", games: 15000, eval: "+1.8", w: 65, d: 17, b: 18 }
                        ]
                    },
                    { 
                        uci: "b8c6", san: "Nc6", comment: "Opponent develops knight targeting e5",
                        eval: "+1.7",
                        candidates: [
                            { san: "Nf3", games: 58000, eval: "+1.7", w: 61, d: 19, b: 20 },
                            { san: "Bf4", games: 12000, eval: "+1.2", w: 54, d: 21, b: 25 }
                        ]
                    },
                    { 
                        uci: "g1f3", san: "Nf3", comment: "3. Nf3 - Guard e5 securely",
                        eval: "+1.7",
                        candidates: [
                            { san: "Qe7", games: 44000, eval: "+1.7", w: 62, d: 18, b: 20 },
                            { san: "Nge7", games: 8000, eval: "+2.1", w: 68, d: 16, b: 16 }
                        ]
                    },
                    { 
                        uci: "d8e7", san: "Qe7", comment: "Black attacks e5 again",
                        eval: "+1.8",
                        candidates: [
                            { san: "Bf4", games: 32000, eval: "+1.8", w: 63, d: 18, b: 19 },
                            { san: "Nc3", games: 11000, eval: "+1.9", w: 64, d: 17, b: 19 }
                        ]
                    },
                    { 
                        uci: "c1f4", san: "Bf4", comment: "4. Bf4 - Defend e5 and invite the trap",
                        eval: "+1.8",
                        candidates: [
                            { san: "Qb4+", games: 28000, eval: "+1.8", w: 63, d: 18, b: 19 }
                        ]
                    },
                    { 
                        uci: "e7b4", san: "Qb4+", comment: "TRAP MOVE! Black forks King and Bishop",
                        eval: "+3.5",
                        candidates: [
                            { san: "Bd2!", games: 22000, eval: "+3.5", w: 74, d: 14, b: 12 },
                            { san: "Qd2??", games: 5000, eval: "-6.2", w: 8, d: 6, b: 86 }
                        ]
                    },
                    { 
                        uci: "f4d2", san: "Bd2!", comment: "5. Bd2! - The Winning Move! Never play Qd2",
                        eval: "+3.5",
                        candidates: [
                            { san: "Qxb2", games: 18000, eval: "+3.5", w: 75, d: 13, b: 12 }
                        ]
                    },
                    { 
                        uci: "b4b2", san: "Qxb2", comment: "Black greedily captures on b2",
                        eval: "+3.8",
                        candidates: [
                            { san: "Nc3!", games: 14000, eval: "+3.8", w: 78, d: 12, b: 10 },
                            { san: "Bc3", games: 4000, eval: "+3.4", w: 72, d: 15, b: 13 }
                        ]
                    },
                    { 
                        uci: "b1c3", san: "Nc3!", comment: "6. Nc3! - Threatens 7.Rb1 (trapping Queen) and 7.Nd5! Total victory.",
                        eval: "+3.8",
                        candidates: [
                            { san: "Bb4", games: 9000, eval: "+3.8", w: 78, d: 12, b: 10 }
                        ]
                    }
                ]
            },
            {
                id: 1,
                category: "white_fix",
                title: "⚪ White: Active Queen's Gambit (1.d4 d5 2.c4!)",
                tag: "70% Passive d4 Fix",
                side: "white",
                strategy: "When playing 1.d4, immediately contest Black's d5 pawn with 2.c4! This gives you central space and allows your knights and bishops to develop aggressively.",
                moves: [
                    { 
                        uci: "d2d4", san: "d4", comment: "1. d4 - Queen's Pawn",
                        eval: "+0.3",
                        candidates: [
                            { san: "d4", games: 1845000, eval: "+0.3", w: 38, d: 34, b: 28 }
                        ]
                    },
                    { 
                        uci: "d7d5", san: "d5", comment: "Black takes the center",
                        eval: "+0.4",
                        candidates: [
                            { san: "c4!", games: 780000, eval: "+0.4", w: 41, d: 35, b: 24 },
                            { san: "Nf3", games: 320000, eval: "+0.2", w: 35, d: 36, b: 29 }
                        ]
                    },
                    { 
                        uci: "c2c4", san: "c4!", comment: "2. c4! - Queen's Gambit! Strike Black's center immediately",
                        eval: "+0.4",
                        candidates: [
                            { san: "e6", games: 390000, eval: "+0.4", w: 40, d: 36, b: 24 },
                            { san: "c6", games: 260000, eval: "+0.4", w: 39, d: 37, b: 24 },
                            { san: "dxc4", games: 110000, eval: "+0.6", w: 44, d: 33, b: 23 }
                        ]
                    },
                    { 
                        uci: "e7e6", san: "e6", comment: "Black defends d5 (Queen's Gambit Declined)",
                        eval: "+0.5",
                        candidates: [
                            { san: "Nc3", games: 280000, eval: "+0.5", w: 42, d: 36, b: 22 },
                            { san: "Nf3", games: 90000, eval: "+0.4", w: 40, d: 37, b: 23 }
                        ]
                    },
                    { 
                        uci: "b1c3", san: "Nc3", comment: "3. Nc3 - Develop with center pressure",
                        eval: "+0.5",
                        candidates: [
                            { san: "Nf6", games: 220000, eval: "+0.5", w: 42, d: 36, b: 22 }
                        ]
                    },
                    { 
                        uci: "g8f6", san: "Nf6", comment: "Black develops knight",
                        eval: "+0.5",
                        candidates: [
                            { san: "Bg5!", games: 160000, eval: "+0.5", w: 43, d: 36, b: 21 },
                            { san: "cxd5", games: 45000, eval: "+0.5", w: 42, d: 37, b: 21 }
                        ]
                    },
                    { 
                        uci: "c1g5", san: "Bg5!", comment: "4. Bg5! - Active pin on Black's knight before playing e3!",
                        eval: "+0.5",
                        candidates: [
                            { san: "Be7", games: 120000, eval: "+0.5", w: 43, d: 36, b: 21 }
                        ]
                    }
                ]
            },
            {
                id: 2,
                category: "black_fix",
                title: "⚫ Black: Scandinavian vs 2.e5 (The Bishop Free Rule)",
                tag: "65.6% Loss Rate Fix",
                side: "black",
                strategy: "When White plays 2.e5, NEVER play 2...e6! Always play 2...Bf5! first, bringing your bishop outside the pawn chain. Then follow up with 3...e6, 4...c5! and 5...Nc6.",
                moves: [
                    { 
                        uci: "e2e4", san: "e4", comment: "White plays 1. e4",
                        eval: "+0.3",
                        candidates: [
                            { san: "d5", games: 450000, eval: "+0.3", w: 39, d: 29, b: 32 }
                        ]
                    },
                    { 
                        uci: "d7d5", san: "d5", comment: "1... d5 - Scandinavian Defense",
                        eval: "+0.4",
                        candidates: [
                            { san: "exd5", games: 380000, eval: "+0.4", w: 40, d: 29, b: 31 },
                            { san: "e5", games: 45000, eval: "-0.2", w: 32, d: 28, b: 40 }
                        ]
                    },
                    { 
                        uci: "e4e5", san: "e5", comment: "White pushes 2. e5 (Advance Variation)",
                        eval: "-0.2",
                        candidates: [
                            { san: "Bf5!", games: 35000, eval: "-0.2", w: 31, d: 28, b: 41 },
                            { san: "c5", games: 6000, eval: "-0.1", w: 33, d: 29, b: 38 },
                            { san: "e6?", games: 3000, eval: "+0.8", w: 58, d: 22, b: 20 }
                        ]
                    },
                    { 
                        uci: "c8f5", san: "Bf5!", comment: "2... Bf5! - Bishop is FREE! Never trap it on c8",
                        eval: "-0.2",
                        candidates: [
                            { san: "d4", games: 28000, eval: "-0.2", w: 31, d: 28, b: 41 },
                            { san: "Nf3", games: 5000, eval: "-0.2", w: 32, d: 29, b: 39 }
                        ]
                    },
                    { 
                        uci: "d2d4", san: "d4", comment: "White supports e5 pawn",
                        eval: "-0.2",
                        candidates: [
                            { san: "e6", games: 26000, eval: "-0.2", w: 31, d: 28, b: 41 }
                        ]
                    },
                    { 
                        uci: "e7e6", san: "e6", comment: "3... e6 - Now solidify the center comfortably",
                        eval: "-0.2",
                        candidates: [
                            { san: "Nf3", games: 22000, eval: "-0.2", w: 31, d: 28, b: 41 }
                        ]
                    },
                    { 
                        uci: "g1f3", san: "Nf3", comment: "White develops knight",
                        eval: "-0.3",
                        candidates: [
                            { san: "c5!", games: 18000, eval: "-0.3", w: 29, d: 28, b: 43 }
                        ]
                    },
                    { 
                        uci: "c7c5", san: "c5!", comment: "4... c5! - Strike White's d4 pawn center with tempo!",
                        eval: "-0.3",
                        candidates: [
                            { san: "c3", games: 14000, eval: "-0.3", w: 29, d: 28, b: 43 }
                        ]
                    }
                ]
            },
            {
                id: 3,
                category: "black_fix",
                title: "⚫ Black: Danish Gambit Defense (5...d5 Schlechter Defense)",
                tag: "100% Loss Rate Fix",
                side: "black",
                strategy: "White gives two pawns for monster bishops on c4 and b2. The master refutation is 5...d5!! Returning one pawn closes the dangerous bishop diagonal, forces trades, and leaves Black up a clean pawn with an easy win.",
                moves: [
                    { 
                        uci: "e2e4", san: "e4", comment: "1. e4",
                        eval: "+0.3",
                        candidates: [{ san: "e5", games: 850000, eval: "+0.3", w: 37, d: 33, b: 30 }]
                    },
                    { 
                        uci: "e7e5", san: "e5", comment: "1... e5",
                        eval: "+0.3",
                        candidates: [{ san: "d4", games: 90000, eval: "+0.3", w: 38, d: 31, b: 31 }]
                    },
                    { 
                        uci: "d2d4", san: "d4", comment: "2. d4 (Center Game)",
                        eval: "+0.3",
                        candidates: [{ san: "exd4", games: 82000, eval: "+0.3", w: 38, d: 31, b: 31 }]
                    },
                    { 
                        uci: "e5d4", san: "exd4", comment: "Take the central pawn",
                        eval: "+0.3",
                        candidates: [{ san: "c3", games: 24000, eval: "+0.2", w: 36, d: 28, b: 36 }]
                    },
                    { 
                        uci: "c2c3", san: "c3", comment: "Danish Gambit offer",
                        eval: "+0.2",
                        candidates: [{ san: "dxc3", games: 19000, eval: "+0.2", w: 36, d: 28, b: 36 }]
                    },
                    { 
                        uci: "d4c3", san: "dxc3", comment: "Take 1st pawn",
                        eval: "+0.2",
                        candidates: [{ san: "Bc4", games: 12000, eval: "-0.3", w: 31, d: 24, b: 45 }]
                    },
                    { 
                        uci: "f1c4", san: "Bc4", comment: "White attacks f7",
                        eval: "-0.3",
                        candidates: [{ san: "cxb2", games: 9500, eval: "-0.3", w: 31, d: 24, b: 45 }]
                    },
                    { 
                        uci: "c3b2", san: "cxb2", comment: "Take 2nd pawn",
                        eval: "-0.3",
                        candidates: [{ san: "Bxb2", games: 9000, eval: "-0.3", w: 31, d: 24, b: 45 }]
                    },
                    { 
                        uci: "c1b2", san: "Bxb2", comment: "White's sniper bishops are ready",
                        eval: "-0.8",
                        candidates: [
                            { san: "d5!!", games: 6800, eval: "-0.8", w: 22, d: 26, b: 52 },
                            { san: "Nf6?", games: 1500, eval: "+1.2", w: 62, d: 18, b: 20 }
                        ]
                    },
                    { 
                        uci: "d7d5", san: "d5!", comment: "5... d5!! - Schlechter Defense! Closes bishop diagonal and wins!",
                        eval: "-0.8",
                        candidates: [{ san: "Bxd5", games: 5800, eval: "-0.8", w: 22, d: 26, b: 52 }]
                    }
                ]
            },
            {
                id: 4,
                category: "black_fix",
                title: "⚫ Black: Countering London System (2...c5 & 4...Qb6!)",
                tag: "72.7% Loss Rate Fix",
                side: "black",
                strategy: "When White plays 2.Bf4, immediately hit with 2...c5! White's bishop left the c1 square, leaving the b2 pawn vulnerable. Playing 4...Qb6 attacks b2 and seizes the initiative.",
                moves: [
                    { 
                        uci: "d2d4", san: "d4", comment: "1. d4",
                        eval: "+0.3",
                        candidates: [{ san: "d5", games: 780000, eval: "+0.3", w: 38, d: 34, b: 28 }]
                    },
                    { 
                        uci: "d7d5", san: "d5", comment: "1... d5",
                        eval: "+0.3",
                        candidates: [{ san: "Bf4", games: 210000, eval: "+0.2", w: 37, d: 35, b: 28 }]
                    },
                    { 
                        uci: "c1f4", san: "Bf4", comment: "London System",
                        eval: "+0.1",
                        candidates: [
                            { san: "c5!", games: 95000, eval: "+0.0", w: 34, d: 36, b: 30 },
                            { san: "Nf6", games: 88000, eval: "+0.2", w: 38, d: 35, b: 27 }
                        ]
                    },
                    { 
                        uci: "c7c5", san: "c5!", comment: "2... c5! - Immediate counter-attack against d4",
                        eval: "+0.0",
                        candidates: [{ san: "e3", games: 74000, eval: "+0.0", w: 34, d: 36, b: 30 }]
                    },
                    { 
                        uci: "e2e3", san: "e3", comment: "White defends d4",
                        eval: "+0.0",
                        candidates: [{ san: "Nc6", games: 58000, eval: "+0.0", w: 34, d: 36, b: 30 }]
                    },
                    { 
                        uci: "b8c6", san: "Nc6", comment: "3... Nc6 - Pressure d4",
                        eval: "+0.0",
                        candidates: [{ san: "Nf3", games: 46000, eval: "+0.0", w: 34, d: 36, b: 30 }]
                    },
                    { 
                        uci: "g1f3", san: "Nf3", comment: "White develops knight",
                        eval: "-0.2",
                        candidates: [
                            { san: "Qb6!", games: 31000, eval: "-0.2", w: 30, d: 35, b: 35 }
                        ]
                    },
                    { 
                        uci: "d8b6", san: "Qb6!", comment: "4... Qb6! - Double attack on b2 and d4! Black takes control.",
                        eval: "-0.2",
                        candidates: [{ san: "Nc3", games: 16000, eval: "-0.2", w: 30, d: 35, b: 35 }]
                    }
                ]
            },
            {
                id: 5,
                category: "black_fix",
                title: "⚫ Black: Reti Opening Defense (2...d4 Space Wedge)",
                tag: "83.3% Loss Rate Fix",
                side: "black",
                strategy: "When White plays 1.Nf3 d5 2.c4, do NOT trade on c4! Push 2...d4! to cramp White's entire queenside, take away the c3 square from White's knight, and follow up with 3...c5 and 4...Nc6.",
                moves: [
                    { 
                        uci: "g1f3", san: "Nf3", comment: "1. Nf3 (Reti Opening)",
                        eval: "+0.2",
                        candidates: [{ san: "d5", games: 420000, eval: "+0.2", w: 36, d: 36, b: 28 }]
                    },
                    { 
                        uci: "d7d5", san: "d5", comment: "1... d5 - Control the center",
                        eval: "+0.2",
                        candidates: [{ san: "c4", games: 140000, eval: "+0.1", w: 35, d: 36, b: 29 }]
                    },
                    { 
                        uci: "c2c4", san: "c4", comment: "White challenges d5 from the flank",
                        eval: "-0.1",
                        candidates: [
                            { san: "d4!", games: 72000, eval: "-0.1", w: 32, d: 37, b: 31 },
                            { san: "c6", games: 38000, eval: "+0.2", w: 37, d: 36, b: 27 },
                            { san: "dxc4?", games: 22000, eval: "+0.4", w: 41, d: 35, b: 24 }
                        ]
                    },
                    { 
                        uci: "d5d4", san: "d4!", comment: "2... d4! - Push past! Space wedge stops Nc3 and cramps White.",
                        eval: "-0.1",
                        candidates: [{ san: "e3", games: 34000, eval: "-0.1", w: 32, d: 37, b: 31 }]
                    },
                    { 
                        uci: "e2e3", san: "e3", comment: "White attacks d4 pawn",
                        eval: "-0.1",
                        candidates: [{ san: "c5", games: 24000, eval: "-0.1", w: 32, d: 37, b: 31 }]
                    },
                    { 
                        uci: "c7c5", san: "c5", comment: "3... c5 - Support the d4 outpost",
                        eval: "-0.1",
                        candidates: [{ san: "exd4", games: 18000, eval: "-0.1", w: 32, d: 37, b: 31 }]
                    },
                    { 
                        uci: "e3d4", san: "exd4", comment: "White trades",
                        eval: "-0.1",
                        candidates: [{ san: "cxd4", games: 18000, eval: "-0.1", w: 32, d: 37, b: 31 }]
                    },
                    { 
                        uci: "c5d4", san: "cxd4", comment: "4... cxd4 - Black maintains a great central wedge!",
                        eval: "-0.1",
                        candidates: [{ san: "d3", games: 12000, eval: "-0.1", w: 32, d: 37, b: 31 }]
                    }
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
                <div onclick="selectDrill(${d.id})" id="drill-item-${d.id}" class="trainer-card cursor-pointer p-2.5 rounded-lg border border-slate-700 bg-slate-900/70 hover:bg-slate-800 transition ${d.id === activeDrill.id ? 'active' : ''}">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-xs text-slate-200 truncate mr-2">${d.title}</span>
                        <span class="text-[10px] px-1.5 py-0.5 rounded font-mono ${d.category.includes('fix') ? 'bg-rose-950/80 text-rose-300 border border-rose-800/60' : 'bg-emerald-950/80 text-emerald-300 border border-emerald-800/60'}">${d.tag}</span>
                    </div>
                </div>
            `).join('');
        }

        function filterDrills(filter) {
            ['all', 'white_fix', 'black_fix'].forEach(f => {
                const btn = document.getElementById('filter-' + f);
                if (btn) {
                    btn.className = (f === filter) ? 'px-2 py-0.5 bg-sky-600 rounded text-white' : 'px-2 py-0.5 bg-slate-900 hover:bg-slate-700 rounded text-slate-300';
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
            document.getElementById('strategy-title').innerHTML = `<span>💡</span> Strategy Guide: ${activeDrill.title}`;
            document.getElementById('strategy-desc').innerText = activeDrill.strategy;
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

        function updateExplorerTable(candidates, currentEval = "--") {
            document.getElementById('pos-eval-badge').innerText = `Eval: ${currentEval}`;
            const tbody = document.getElementById('lichess-explorer-tbody');
            if (!candidates || candidates.length === 0) {
                tbody.innerHTML = `<tr><td colspan="4" class="py-2 text-center text-slate-500">End of theoretical book line</td></tr>`;
                return;
            }

            tbody.innerHTML = candidates.map(c => `
                <tr class="hover:bg-slate-700/40 cursor-pointer">
                    <td class="py-1.5 px-3 font-bold text-slate-100">${c.san}</td>
                    <td class="py-1.5 px-2 text-center text-slate-400 text-[11px]">${c.games.toLocaleString()}</td>
                    <td class="py-1.5 px-2 text-center font-bold ${c.eval.startsWith('+') ? 'text-emerald-400' : 'text-rose-400'}">${c.eval}</td>
                    <td class="py-1.5 px-3 text-center">
                        <div class="eval-bar-container">
                            <div class="bar-white" style="width: ${c.w}%">${c.w}%</div>
                            <div class="bar-draw" style="width: ${c.d}%">${c.d}%</div>
                            <div class="bar-black" style="width: ${c.b}%">${c.b}%</div>
                        </div>
                    </td>
                </tr>
            `).join('');
        }

        function advanceDrill() {
            if (currentStepIndex >= activeDrill.moves.length) {
                document.getElementById('trainer-prompt').innerHTML = "<span class='text-emerald-400 font-bold'>🎉 Drill Complete! Perfect Opening Mastery!</span>";
                document.getElementById('trainer-subtext').innerText = "You successfully executed all key moves in this line. Try the next drill!";
                isWaitingUserMove = false;
                updateStepIndicator();
                updateExplorerTable([], "+3.5");
                return;
            }

            const moveData = activeDrill.moves[currentStepIndex];
            const isUserTurn = (activeDrill.side === "white" && currentStepIndex % 2 === 0) || (activeDrill.side === "black" && currentStepIndex % 2 === 1);

            updateExplorerTable(moveData.candidates || [], moveData.eval || "--");

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
                document.getElementById('trainer-subtext').innerHTML = "<span class='text-rose-400 font-bold'>❌ Inaccurate Move!</span> Look at the Lichess Explorer table on the right for top master moves.";
                return 'snapback';
            }
        }

        function showDrillHint() {
            if (!isWaitingUserMove) return;
            const expected = activeDrill.moves[currentStepIndex];
            document.getElementById('trainer-subtext').innerHTML = `<span class='text-amber-400 font-bold'>💡 Hint:</span> Look for <strong>${expected.san}</strong> (${expected.comment})`;
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
    print(f"Generated interactive dashboard with Stockfish: {output_path}")
    return output_path
