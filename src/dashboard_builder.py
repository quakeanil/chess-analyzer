"""
HTML Dashboard & Full Lichess-Style Opening Explorer, Trainer, Sparring Bot & Stockfish Engine
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
    <title>Chess Diagnostics & Opening Sparring Bot - __USERNAME__</title>
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
        .board-container { max-width: 420px; width: 100%; margin: 0 auto; position: relative; }
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
                    Chess Diagnostics & Opening Sparring Bot
                    <span class="text-xs bg-sky-500/20 text-sky-400 border border-sky-500/30 px-2 py-0.5 rounded font-mono">__USERNAME__</span>
                </h1>
                <p class="text-xs text-slate-400">Play Against Opening-Locked PC Bots, Stockfish 18 Move Arrows & Study Tracker</p>
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
        <nav class="flex space-x-8 text-sm overflow-x-auto">
            <button onclick="switchTab('sparring')" id="tab-sparring" class="tab-btn active py-3 px-1 text-slate-300 hover:text-white transition whitespace-nowrap">⚔️ Opening Sparring Bot & "What If?"</button>
            <button onclick="switchTab('disasters')" id="tab-disasters" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition whitespace-nowrap">⚡ Stockfish Lost Games Replayer</button>
            <button onclick="switchTab('trainer')" id="tab-trainer" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition whitespace-nowrap">🎯 Lichess Explorer & Trainer</button>
            <button onclick="switchTab('overview')" id="tab-overview" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition whitespace-nowrap">📊 Top 10 Win/Loss Openings</button>
            <button onclick="switchTab('videos')" id="tab-videos" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition whitespace-nowrap">🎥 Master Video Lessons</button>
            <button onclick="switchTab('repertoire')" id="tab-repertoire" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition whitespace-nowrap">📜 Coach's Golden Rules</button>
        </nav>
    </div>

    <!-- Main Content Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto p-6">

        <!-- TAB 0: OPENING SPARRING BOT (PLAY VS LOCKED PC OPENINGS & WHAT-IF) -->
        <section id="view-sparring" class="space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <!-- Left: Interactive Sparring Chessboard -->
                <div class="lg:col-span-5 flex flex-col items-center">
                    <div class="board-container shadow-2xl rounded-lg overflow-hidden border border-slate-700 relative">
                        <div id="sparring-board" style="width: 100%"></div>
                        <!-- SVG ARROWS FOR SPARRING -->
                        <svg id="sparring-arrows-svg" class="absolute inset-0 w-full h-full pointer-events-none z-10" style="width: 100%; height: 100%;">
                            <defs>
                                <marker id="spar-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                                    <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#22c55e" />
                                </marker>
                                <marker id="spar-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                                    <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#ef4444" />
                                </marker>
                            </defs>
                        </svg>
                    </div>

                    <!-- Sparring Controls -->
                    <div class="flex items-center gap-2 mt-4">
                        <button onclick="resetSparringGame()" class="px-4 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded text-sm font-bold shadow flex items-center gap-1.5">
                            <span>🔄</span> New Sparring Game
                        </button>
                        <button onclick="undoSparringMove()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-sm font-semibold">
                            ↩️ Takeback
                        </button>
                        <button onclick="showSparringHint()" class="px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white rounded text-sm font-bold">
                            💡 Show Best Move
                        </button>
                    </div>

                    <div id="sparring-game-status" class="text-xs text-slate-400 mt-2 font-mono">Move 1 | Your Turn (White)</div>
                </div>

                <!-- Right: Opening Selector, Top 5 Lichess Moves & What-If Branch Explorer -->
                <div class="lg:col-span-7 space-y-4">
                    <!-- Opening Bot Selector -->
                    <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-4 space-y-2.5">
                        <div class="flex items-center justify-between">
                            <label class="text-xs font-bold text-sky-400 uppercase tracking-wide flex items-center gap-1.5">
                                <span>🤖</span> Select Opening to Spar Against:
                            </label>
                            <span id="sparring-bot-tag" class="text-[10px] bg-sky-500/20 text-sky-300 border border-sky-500/40 px-2 py-0.5 rounded font-mono font-bold">Bot Locked: Scandinavian</span>
                        </div>

                        <select id="sparring-opening-select" onchange="selectSparringOpening(this.value)" class="w-full bg-slate-900 border border-slate-700 text-slate-200 text-sm rounded-lg p-2.5 focus:border-sky-500 font-medium">
                            <optgroup label="⚪ Practice As White (PC Plays As Black):">
                                <option value="scandi">⚪ White vs 🤖 Scandinavian Defense (Start with 1.e4 -> PC plays 1...d5)</option>
                                <option value="englund">⚪ White vs 🤖 Englund Gambit (Start with 1.d4 -> PC plays 1...e5 2...Nc6 & 4...Qb4+)</option>
                                <option value="qg_white">⚪ White Queen's Gambit Practice (Start with 1.d4 d5 2.c4 -> PC plays QGD/Slav)</option>
                                <option value="sicilian">⚪ White vs 🤖 Sicilian Defense (Start with 1.e4 -> PC plays 1...c5)</option>
                                <option value="french">⚪ White vs 🤖 French Defense (Start with 1.e4 -> PC plays 1...e6)</option>
                                <option value="caro">⚪ White vs 🤖 Caro-Kann Defense (Start with 1.e4 -> PC plays 1...c6)</option>
                            </optgroup>
                            <optgroup label="⚫ Practice As Black (PC Plays As White):">
                                <option value="scandi_black">⚫ Black vs 🤖 Scandinavian 2.e5 (PC plays 1.e4 d5 2.e5 - Drill 2...Bf5!)</option>
                                <option value="london_black">⚫ Black vs 🤖 London System (PC plays 1.d4 d5 2.Bf4 - Drill 2...c5! & 4...Qb6!)</option>
                                <option value="danish_black">⚫ Black vs 🤖 Danish Gambit (PC plays 1.e4 e5 2.d4 3.c3 - Drill 5...d5!!)</option>
                                <option value="reti_black">⚫ Black vs 🤖 Reti Opening (PC plays 1.Nf3 d5 2.c4 - Drill 2...d4!)</option>
                            </optgroup>
                        </select>

                        <!-- "What-If" Preset Branch Buttons -->
                        <div class="pt-1">
                            <div class="text-[10px] font-bold text-slate-400 uppercase mb-1 flex items-center gap-1">
                                <span>🔀</span> "What If?" Quick Variations (Click to jump & test against):
                            </div>
                            <div id="whatif-buttons-container" class="flex flex-wrap gap-1.5"></div>
                        </div>
                    </div>

                    <!-- LICHESS MASTER TOP 5 MOVES EXPLORER TABLE (INTERACTIVE) -->
                    <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-4 space-y-2">
                        <div class="flex items-center justify-between">
                            <h3 class="text-xs font-bold text-sky-400 uppercase tracking-wide flex items-center gap-1.5">
                                <span>📖</span> Lichess Master Top Moves (Click any move to play / force bot)
                            </h3>
                            <span id="sparring-eval-badge" class="text-[11px] bg-slate-900 border border-slate-700 text-emerald-400 font-mono px-2 py-0.5 rounded">Eval: --</span>
                        </div>

                        <div class="overflow-x-auto">
                            <table class="w-full text-xs text-left">
                                <thead class="text-slate-400 bg-slate-900/80 uppercase text-[10px]">
                                    <tr>
                                        <th class="py-1.5 px-3">Move</th>
                                        <th class="py-1.5 px-2">Variation Name</th>
                                        <th class="py-1.5 px-2 text-center">Games</th>
                                        <th class="py-1.5 px-2 text-center">Eval</th>
                                        <th class="py-1.5 px-3 text-center w-36">Win / Draw / Loss %</th>
                                        <th class="py-1.5 px-2 text-center">Action</th>
                                    </tr>
                                </thead>
                                <tbody id="sparring-explorer-tbody" class="divide-y divide-slate-700/50 font-mono"></tbody>
                            </table>
                        </div>
                    </div>

                    <!-- LIVE MOVE COACH & NOTATION -->
                    <div class="bg-gradient-to-br from-slate-900 via-slate-800 to-sky-950/40 rounded-xl border border-sky-500/40 p-3.5 space-y-2 shadow-xl">
                        <div id="sparring-feedback-box" class="bg-slate-900/90 border border-slate-700 p-2.5 rounded-lg text-xs space-y-1">
                            <div class="font-bold text-slate-200" id="sparring-feedback-title">Make your opening move!</div>
                            <p class="text-slate-400" id="sparring-feedback-sub">Play on the board or click any move above to branch.</p>
                        </div>

                        <!-- Live Moves Notation -->
                        <div class="bg-slate-900/70 p-2.5 rounded-lg border border-slate-700">
                            <div class="text-[10px] font-bold text-slate-400 uppercase mb-1">Game Notation:</div>
                            <div id="sparring-moves-list" class="font-mono text-xs text-slate-200 flex flex-wrap gap-1.5 max-h-20 overflow-y-auto">
                                <span class="text-slate-500 italic">No moves played yet</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 1: STOCKFISH EARLY DISASTER REPLAYER & STUDY TRACKER -->
        <section id="view-disasters" class="hidden space-y-6">

            <!-- STUDY PROGRESS BANNER -->
            <div class="bg-slate-800/90 border border-slate-700 rounded-xl p-4 shadow-lg flex flex-wrap items-center justify-between gap-4">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-xl text-emerald-400 font-bold">
                        ✓
                    </div>
                    <div>
                        <div class="text-xs font-bold text-slate-400 uppercase tracking-wide">Losses Study Progress</div>
                        <div class="text-base font-bold text-white flex items-center gap-2">
                            <span id="study-count-text">0 / 40 Studied</span>
                            <span id="study-pct-badge" class="text-xs bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 px-2 py-0.5 rounded font-mono">0% Complete</span>
                        </div>
                    </div>
                </div>

                <!-- Progress Bar -->
                <div class="flex-1 max-w-xs bg-slate-900 h-3 rounded-full overflow-hidden border border-slate-700">
                    <div id="study-progress-bar" class="bg-emerald-500 h-full transition-all duration-300" style="width: 0%"></div>
                </div>

                <!-- Filter Buttons -->
                <div class="flex items-center gap-1.5 text-xs">
                    <button onclick="filterStudiedGames('all')" id="btn-filter-all" class="px-2.5 py-1 bg-sky-600 rounded text-white font-medium">All (<span id="cnt-all">40</span>)</button>
                    <button onclick="filterStudiedGames('unstudied')" id="btn-filter-unstudied" class="px-2.5 py-1 bg-slate-900 hover:bg-slate-700 rounded text-slate-300 font-medium">⏳ Unstudied (<span id="cnt-unstudied">40</span>)</button>
                    <button onclick="filterStudiedGames('studied')" id="btn-filter-studied" class="px-2.5 py-1 bg-slate-900 hover:bg-slate-700 rounded text-slate-300 font-medium">✅ Studied (<span id="cnt-studied">0</span>)</button>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <!-- Left: Board, Arrow SVG Overlay & Controls -->
                <div class="lg:col-span-5 flex flex-col items-center">
                    <div class="board-container shadow-2xl rounded-lg overflow-hidden border border-slate-700 relative">
                        <div id="replay-board" style="width: 100%"></div>
                        <!-- SVG ARROW OVERLAY -->
                        <svg id="replay-arrows-svg" class="absolute inset-0 w-full h-full pointer-events-none z-10" style="width: 100%; height: 100%;">
                            <defs>
                                <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                                    <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#22c55e" />
                                </marker>
                                <marker id="arrow-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                                    <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#ef4444" />
                                </marker>
                            </defs>
                        </svg>
                    </div>

                    <!-- Navigation Controls & Arrow Toggle -->
                    <div class="flex items-center gap-2 mt-4">
                        <button onclick="replayFirst()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded text-sm font-semibold">|&lt;</button>
                        <button onclick="replayPrev()" class="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded text-sm font-semibold">&lt; Prev</button>
                        <button onclick="replayNext()" class="px-4 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded text-sm font-semibold">Next &gt;</button>
                        <button onclick="replayLast()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded text-sm font-semibold">&gt;|</button>
                    </div>

                    <div class="flex items-center justify-between w-full max-w-[420px] mt-2 px-1">
                        <div id="replay-status" class="text-xs text-slate-400 font-mono">Move 0 / 0</div>
                        <button onclick="toggleArrowDisplay()" id="btn-arrow-toggle" class="text-xs text-emerald-400 hover:text-emerald-300 font-semibold flex items-center gap-1 bg-slate-800 px-2 py-0.5 rounded border border-emerald-500/40">
                            <span>🎯</span> Arrow: ON
                        </button>
                    </div>
                </div>

                <!-- Right: Game Selector, Study Actions, Stockfish Panel & Notes -->
                <div class="lg:col-span-7 space-y-4">
                    <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-5">
                        <div class="flex items-center justify-between mb-1.5">
                            <label class="text-xs font-semibold text-slate-400 uppercase">Select Lost Game:</label>
                            <div class="flex items-center gap-2">
                                <button onclick="toggleCurrentGameStudied()" id="btn-toggle-study" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-lg transition shadow flex items-center gap-1.5">
                                    <span>✅</span> Mark as Studied
                                </button>
                                <button onclick="jumpNextUnstudied()" class="px-3 py-1 bg-slate-700 hover:bg-slate-600 text-slate-200 text-xs font-medium rounded-lg transition">
                                    ⏭️ Next Unstudied
                                </button>
                            </div>
                        </div>
                        <select id="game-select" onchange="loadSelectedGame(this.value)" class="w-full bg-slate-900 border border-slate-700 text-slate-200 text-sm rounded-lg p-2.5 focus:border-sky-500 font-mono"></select>

                        <div id="game-meta-card" class="bg-slate-900/70 p-3.5 rounded-lg border border-slate-700 mt-3 text-xs space-y-1">
                            <div><strong>Opening:</strong> <span id="meta-opening" class="text-sky-400"></span></div>
                            <div><strong>Opponent:</strong> <span id="meta-opp" class="text-slate-300"></span> | <strong>Result:</strong> <span id="meta-result" class="text-rose-400 font-semibold"></span></div>
                            <div><strong>Chess.com Link:</strong> <a id="meta-link" href="#" target="_blank" class="text-sky-400 underline">Open on Chess.com ↗</a></div>
                        </div>

                        <!-- Move List with Quality Badges -->
                        <div class="mt-3">
                            <label class="block text-xs font-semibold text-slate-400 uppercase mb-1">Move Notation (Click any move to inspect Stockfish & Arrows):</label>
                            <div id="moves-container" class="bg-slate-900 p-3 rounded-lg border border-slate-700 font-mono text-xs max-h-28 overflow-y-auto leading-relaxed flex flex-wrap gap-1.5"></div>
                        </div>

                        <!-- Personal Study Notes Input -->
                        <div class="mt-3 pt-3 border-t border-slate-700/60">
                            <label class="block text-[11px] font-bold text-amber-400 uppercase mb-1 flex items-center gap-1">
                                <span>📝</span> My Study Notes for this Game:
                            </label>
                            <input type="text" id="game-user-note" oninput="saveCurrentGameNote(this.value)" placeholder="e.g. In Englund, remember 5.Bd2! and 6.Nc3!..." class="w-full bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg p-2 focus:border-amber-400 focus:outline-none">
                        </div>
                    </div>

                    <!-- STOCKFISH 18 LIVE ENGINE EVALUATION CARD -->
                    <div class="bg-gradient-to-br from-slate-900 via-slate-800 to-sky-950/40 rounded-xl border-2 border-sky-500/40 p-4 space-y-3 shadow-xl">
                        <div class="flex items-center justify-between">
                            <h3 class="text-xs font-bold text-sky-400 uppercase tracking-wide flex items-center gap-2">
                                <span>🤖</span> Stockfish 18 Engine Analysis
                            </h3>
                            <span id="sf-eval-badge" class="text-xs bg-sky-500/20 text-sky-300 border border-sky-500/40 px-2.5 py-0.5 rounded font-mono font-bold">Eval: 0.0</span>
                        </div>

                        <!-- Move Comparison Grid -->
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                            <div class="bg-slate-900/90 border border-slate-700 p-2.5 rounded-lg">
                                <div class="font-bold text-slate-400 uppercase text-[10px] mb-1">Move Played in Game</div>
                                <div class="flex items-center gap-2">
                                    <span id="sf-played-move" class="font-mono text-sm text-slate-100 font-bold">--</span>
                                    <span id="sf-quality-badge" class="text-[10px] px-2 py-0.5 rounded font-mono font-semibold border">--</span>
                                </div>
                            </div>
                            <div class="bg-emerald-950/40 border border-emerald-800/60 p-2.5 rounded-lg">
                                <div class="font-bold text-emerald-400 uppercase text-[10px] mb-1">🟢 Stockfish Recommended Best Move</div>
                                <div id="sf-best-move" class="font-mono text-sm text-emerald-300 font-bold">--</div>
                            </div>
                        </div>

                        <!-- Engine Best Continuation Line (PV) -->
                        <div class="bg-slate-900/80 border border-slate-700 p-2.5 rounded-lg text-xs space-y-1">
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

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
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
        </section>

    </main>

    <script>
        const analysisData = __ANALYSIS_DATA__;
        const userStats = __USER_STATS__;
        const topOpenings = __TOP_OPENINGS__;

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
            ['sparring', 'disasters', 'trainer', 'overview', 'videos', 'repertoire'].forEach(id => {
                document.getElementById('view-' + id).classList.add('hidden');
                document.getElementById('tab-' + id).classList.remove('active');
            });
            document.getElementById('view-' + tabId).classList.remove('hidden');
            document.getElementById('tab-' + tabId).classList.add('active');

            if (tabId === 'sparring') {
                setTimeout(() => { if (sparringBoard) sparringBoard.resize(); }, 100);
            } else if (tabId === 'disasters') {
                setTimeout(() => { 
                    if (replayBoard) replayBoard.resize(); 
                    renderReplayArrows();
                }, 100);
            } else if (tabId === 'trainer') {
                setTimeout(() => { if (trainerBoard) trainerBoard.resize(); }, 100);
            }
        }

        // ==========================================
        // ⚔️ MASTER OPENING SPARRING BOT & LICHESS TOP 5
        // ==========================================
        const masterOpeningDatabase = {
            "": [
                { san: "e4", games: 2450000, eval: "+0.3", w: 38, d: 34, b: 28, name: "King's Pawn Opening" },
                { san: "d4", games: 2180000, eval: "+0.3", w: 38, d: 35, b: 27, name: "Queen's Pawn Opening" },
                { san: "Nf3", games: 520000, eval: "+0.2", w: 36, d: 37, b: 27, name: "Zukertort / Réti" },
                { san: "c4", games: 410000, eval: "+0.2", w: 37, d: 36, b: 27, name: "English Opening" }
            ],
            "e4": [
                { san: "e5", games: 980000, eval: "+0.3", w: 37, d: 33, b: 30, name: "Open Game (1...e5)" },
                { san: "c5", games: 890000, eval: "+0.2", w: 36, d: 34, b: 30, name: "Sicilian Defense" },
                { san: "e6", games: 450000, eval: "+0.4", w: 40, d: 32, b: 28, name: "French Defense" },
                { san: "c6", games: 390000, eval: "+0.3", w: 39, d: 34, b: 27, name: "Caro-Kann Defense" },
                { san: "d5", games: 320000, eval: "+0.4", w: 42, d: 29, b: 29, name: "Scandinavian Defense" }
            ],
            "e4 d5": [
                { san: "exd5", games: 280000, eval: "+0.4", w: 42, d: 30, b: 28, name: "Mainline Accepted" },
                { san: "Nc3", games: 22000, eval: "+0.1", w: 36, d: 31, b: 33, name: "Nimzowitsch Defense" },
                { san: "e5", games: 14000, eval: "-0.2", w: 31, d: 28, b: 41, name: "Advance Variation" }
            ],
            "e4 d5 exd5": [
                { san: "Qxd5", games: 195000, eval: "+0.4", w: 42, d: 30, b: 28, name: "Mieses-Kotroc Mainline" },
                { san: "Nf6", games: 78000, eval: "+0.5", w: 43, d: 29, b: 28, name: "Modern / Portuguese Variation" },
                { san: "c6", games: 6500, eval: "+1.2", w: 56, d: 20, b: 24, name: "Blackburne-Kloosterboer Gambit" }
            ],
            "e4 d5 exd5 Qxd5": [
                { san: "Nc3", games: 185000, eval: "+0.4", w: 42, d: 30, b: 28, name: "Develop Knight with Tempo" },
                { san: "Nf3", games: 7000, eval: "+0.1", w: 35, d: 32, b: 33, name: "Passive Knight Development" }
            ],
            "e4 d5 exd5 Qxd5 Nc3": [
                { san: "Qa5", games: 110000, eval: "+0.4", w: 41, d: 31, b: 28, name: "Classical Mainline (Qa5)" },
                { san: "Qd6", games: 52000, eval: "+0.4", w: 42, d: 30, b: 28, name: "Gubinsky-Melts (Qd6)" },
                { san: "Qd8", games: 22000, eval: "+0.5", w: 45, d: 28, b: 27, name: "Backward Retreat (Qd8)" }
            ],
            "e4 d5 exd5 Qxd5 Nc3 Qa5": [
                { san: "d4", games: 85000, eval: "+0.4", w: 42, d: 31, b: 27, name: "Central Advance" },
                { san: "Nf3", games: 22000, eval: "+0.3", w: 39, d: 33, b: 28, name: "Knight Development" }
            ],
            "e4 d5 exd5 Qxd5 Nc3 Qa5 d4": [
                { san: "Nf6", games: 62000, eval: "+0.4", w: 41, d: 31, b: 28, name: "Classical Knight" },
                { san: "c6", games: 18000, eval: "+0.4", w: 42, d: 32, b: 26, name: "Solidifying c6" }
            ],
            "d4": [
                { san: "d5", games: 920000, eval: "+0.3", w: 38, d: 35, b: 27, name: "Closed Game (1...d5)" },
                { san: "Nf6", games: 880000, eval: "+0.3", w: 37, d: 36, b: 27, name: "Indian Defenses (1...Nf6)" },
                { san: "e6", games: 140000, eval: "+0.3", w: 39, d: 34, b: 27, name: "Horwitz Defense" },
                { san: "e5", games: 32000, eval: "+1.6", w: 62, d: 18, b: 20, name: "Englund Gambit" }
            ],
            "d4 e5": [
                { san: "dxe5", games: 29000, eval: "+1.6", w: 62, d: 18, b: 20, name: "Accept the Gambit" }
            ],
            "d4 e5 dxe5": [
                { san: "Nc6", games: 22000, eval: "+1.6", w: 61, d: 19, b: 20, name: "Attack e5 Pawn" },
                { san: "d6", games: 4500, eval: "+1.8", w: 66, d: 17, b: 17, name: "Blackburne Gambit" }
            ],
            "d4 e5 dxe5 Nc6": [
                { san: "Nf3", games: 20000, eval: "+1.7", w: 61, d: 19, b: 20, name: "Defend e5" }
            ],
            "d4 e5 dxe5 Nc6 Nf3": [
                { san: "Qe7", games: 17000, eval: "+1.7", w: 62, d: 18, b: 20, name: "Triple attack on e5" }
            ],
            "d4 e5 dxe5 Nc6 Nf3 Qe7": [
                { san: "Bf4", games: 14000, eval: "+1.8", w: 63, d: 18, b: 19, name: "Defend e5 (Sets up 4...Qb4+)" }
            ],
            "d4 e5 dxe5 Nc6 Nf3 Qe7 Bf4": [
                { san: "Qb4+", games: 13000, eval: "+1.8", w: 63, d: 18, b: 19, name: "The Double Attack Trap!" }
            ],
            "d4 e5 dxe5 Nc6 Nf3 Qe7 Bf4 Qb4+": [
                { san: "Bd2!", games: 10500, eval: "+3.5", w: 74, d: 14, b: 12, name: "The Winning Refutation!" },
                { san: "Qd2??", games: 2200, eval: "-6.2", w: 8, d: 6, b: 86, name: "Blunder! Loses to Qxb2" }
            ],
            "d4 e5 dxe5 Nc6 Nf3 Qe7 Bf4 Qb4+ Bd2": [
                { san: "Qxb2", games: 9800, eval: "+3.5", w: 75, d: 13, b: 12, name: "Greedy Capture on b2" }
            ],
            "d4 e5 dxe5 Nc6 Nf3 Qe7 Bf4 Qb4+ Bd2 Qxb2": [
                { san: "Nc3!", games: 8200, eval: "+3.8", w: 78, d: 12, b: 10, name: "Threatens 7.Rb1 & 7.Nd5! (+3.8)" },
                { san: "Bc3", games: 1400, eval: "+3.4", w: 72, d: 15, b: 13, name: "Bishop Defense" }
            ],
            "d4 d5": [
                { san: "c4", games: 580000, eval: "+0.4", w: 41, d: 35, b: 24, name: "Queen's Gambit!" },
                { san: "Nf3", games: 220000, eval: "+0.2", w: 36, d: 36, b: 28, name: "Passive d4 Setup" },
                { san: "Bf4", games: 160000, eval: "+0.2", w: 37, d: 35, b: 28, name: "London System" }
            ],
            "d4 d5 Bf4": [
                { san: "c5!", games: 82000, eval: "+0.0", w: 34, d: 36, b: 30, name: "Strike at d4 Center!" },
                { san: "Nf6", games: 55000, eval: "+0.2", w: 38, d: 35, b: 27, name: "Classical Knight" }
            ],
            "d4 d5 Bf4 c5 e3": [
                { san: "Nc6", games: 52000, eval: "+0.0", w: 34, d: 36, b: 30, name: "Knight Pressure on d4" }
            ],
            "d4 d5 Bf4 c5 e3 Nc6 Nf3": [
                { san: "Qb6!", games: 28000, eval: "-0.2", w: 30, d: 35, b: 35, name: "Double Attack on b2 & d4!" }
            ],
            "e4 e5 d4 exd4 c3 dxc3 Bc4 cxb2 Bxb2": [
                { san: "d5!!", games: 6800, eval: "-0.8", w: 22, d: 26, b: 52, name: "Schlechter Defense Refutation!" },
                { san: "Nf6?", games: 1500, eval: "+1.2", w: 62, d: 18, b: 20, name: "Allows e5 Attack" }
            ]
        };

        const sparringRepertoires = {
            scandi: {
                title: "⚪ White vs 🤖 Scandinavian Defense",
                userSide: "white",
                expectedFirst: "e4",
                goal: "Start with 1.e4. Black will play 1...d5. Take with 2.exd5 and gain tempo on Black's queen with 3.Nc3!",
                botTag: "Bot Locked: Scandinavian (1.e4 d5)",
                whatifs: [
                    { label: "▶ 2...Qxd5 (Mainline Qa5)", seq: ["e4", "d5", "exd5", "Qxd5", "Nc3", "Qa5"] },
                    { label: "▶ 2...Qxd5 3...Qd6 (Modern)", seq: ["e4", "d5", "exd5", "Qxd5", "Nc3", "Qd6"] },
                    { label: "▶ 2...Nf6 (Portuguese)", seq: ["e4", "d5", "exd5", "Nf6"] },
                    { label: "▶ 2.e5 (Advance Bf5)", seq: ["e4", "d5", "e5", "Bf5"] }
                ]
            },
            englund: {
                title: "⚪ White vs 🤖 Englund Gambit",
                userSide: "white",
                expectedFirst: "d4",
                goal: "Start with 1.d4. Black will play the Englund Gambit (1...e5 2.dxe5 Nc6 3.Nf3 Qe7 4.Bf4 Qb4+). Refute it with 5.Bd2! Qxb2 6.Nc3! (+3.5 White).",
                botTag: "Bot Locked: Englund Gambit (1.d4 e5)",
                whatifs: [
                    { label: "▶ Refute Trap (5.Bd2! Qxb2 6.Nc3!)", seq: ["d4", "e5", "dxe5", "Nc6", "Nf3", "Qe7", "Bf4", "Qb4+", "Bd2", "Qxb2", "Nc3"] },
                    { label: "▶ Black Plays 4...Qb4+ (Trap Start)", seq: ["d4", "e5", "dxe5", "Nc6", "Nf3", "Qe7", "Bf4", "Qb4+"] }
                ]
            },
            qg_white: {
                title: "⚪ White Queen's Gambit Practice",
                userSide: "white",
                expectedFirst: "d4",
                goal: "Play 1.d4 d5 2.c4! to control the center. Black will respond with QGD (2...e6), Slav (2...c6) or QGA (2...dxc4).",
                botTag: "Bot Locked: Queen's Gambit (1.d4 d5 2.c4)",
                whatifs: [
                    { label: "▶ 2...e6 (Queen's Gambit Declined)", seq: ["d4", "d5", "c4", "e6", "Nc3", "Nf6"] },
                    { label: "▶ 2...c6 (Slav Defense)", seq: ["d4", "d5", "c4", "c6", "Nf3", "Nf6"] },
                    { label: "▶ 2...dxc4 (Queen's Gambit Accepted)", seq: ["d4", "d5", "c4", "dxc4", "Nf3"] }
                ]
            },
            sicilian: {
                title: "⚪ White vs 🤖 Sicilian Defense",
                userSide: "white",
                expectedFirst: "e4",
                goal: "Start with 1.e4. Black will play 1...c5 (Open Sicilian). Practice 2.Nf3 and 3.d4!",
                botTag: "Bot Locked: Sicilian Defense (1.e4 c5)",
                whatifs: [
                    { label: "▶ 2...d6 (Najdorf / Dragon)", seq: ["e4", "c5", "Nf3", "d6", "d4", "cxd4", "Nxd4", "Nf6", "Nc3", "a6"] },
                    { label: "▶ 2...Nc6 (Classical Sicilian)", seq: ["e4", "c5", "Nf3", "Nc6", "d4", "cxd4", "Nxd4"] },
                    { label: "▶ 2...e6 (French Sicilian)", seq: ["e4", "c5", "Nf3", "e6", "d4", "cxd4", "Nxd4"] }
                ]
            },
            french: {
                title: "⚪ White vs 🤖 French Defense",
                userSide: "white",
                expectedFirst: "e4",
                goal: "Start with 1.e4. Black will play 1...e6 and 2...d5. Practice 3.e5 (Advance) or 3.Nc3 (Classical).",
                botTag: "Bot Locked: French Defense (1.e4 e6)",
                whatifs: [
                    { label: "▶ Advance Variation (3.e5 c5)", seq: ["e4", "e6", "d4", "d5", "e5", "c5", "c3", "Nc6"] },
                    { label: "▶ Classical 3.Nc3 Nf6", seq: ["e4", "e6", "d4", "d5", "Nc3", "Nf6"] }
                ]
            },
            caro: {
                title: "⚪ White vs 🤖 Caro-Kann Defense",
                userSide: "white",
                expectedFirst: "e4",
                goal: "Start with 1.e4. Black will play 1...c6 and 2...d5. Gain central space with 3.e5 or 3.Nc3.",
                botTag: "Bot Locked: Caro-Kann (1.e4 c6)",
                whatifs: [
                    { label: "▶ Advance Variation (3.e5 Bf5)", seq: ["e4", "c6", "d4", "d5", "e5", "Bf5", "Nf3", "e6"] },
                    { label: "▶ Classical 3.Nc3 dxe4", seq: ["e4", "c6", "d4", "d5", "Nc3", "dxe4", "Nxe4"] }
                ]
            },
            scandi_black: {
                title: "⚫ Black vs 🤖 Scandinavian 2.e5",
                userSide: "black",
                expectedFirst: "d5",
                goal: "When PC plays 1.e4, reply 1...d5. When PC pushes 2.e5, play 2...Bf5! outside the pawn chain.",
                botTag: "Bot Locked: Scandi 2.e5",
                whatifs: [
                    { label: "▶ 2.e5 Bf5! (Bishop Free)", seq: ["e4", "d5", "e5", "Bf5", "d4", "e6", "Nf3", "c5"] }
                ]
            },
            london_black: {
                title: "⚫ Black vs 🤖 London System",
                userSide: "black",
                expectedFirst: "d5",
                goal: "When PC plays 1.d4, play 1...d5. When PC plays 2.Bf4, strike immediately with 2...c5! and 4...Qb6!",
                botTag: "Bot Locked: London System",
                whatifs: [
                    { label: "▶ 2...c5! 4...Qb6! (Counter-Attack)", seq: ["d4", "d5", "Bf4", "c5", "e3", "Nc6", "Nf3", "Qb6"] }
                ]
            },
            danish_black: {
                title: "⚫ Black vs 🤖 Danish Gambit",
                userSide: "black",
                expectedFirst: "e5",
                goal: "When PC plays 1.e4 e5 2.d4 exd4 3.c3, accept the gambit and play 5...d5!! (Schlechter Defense).",
                botTag: "Bot Locked: Danish Gambit",
                whatifs: [
                    { label: "▶ 5...d5!! (Schlechter Refutation)", seq: ["e4", "e5", "d4", "exd4", "c3", "dxc3", "Bc4", "cxb2", "Bxb2", "d5"] }
                ]
            },
            reti_black: {
                title: "⚫ Black vs 🤖 Reti Opening",
                userSide: "black",
                expectedFirst: "d5",
                goal: "When PC plays 1.Nf3, play 1...d5. When PC plays 2.c4, push 2...d4! seizing space.",
                botTag: "Bot Locked: Reti Opening",
                whatifs: [
                    { label: "▶ 2...d4! (Space Wedge)", seq: ["Nf3", "d5", "c4", "d4"] }
                ]
            }
        };

        let sparringBoard = null;
        let sparringGame = new Chess();
        let currentSparringRep = sparringRepertoires.scandi;

        function initSparring() {
            sparringBoard = Chessboard('sparring-board', {
                draggable: true,
                position: 'start',
                pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png',
                onDrop: onSparringDrop
            });

            selectSparringOpening("scandi");
        }

        function selectSparringOpening(key) {
            currentSparringRep = sparringRepertoires[key] || sparringRepertoires.scandi;
            document.getElementById('sparring-bot-tag').innerText = currentSparringRep.botTag;
            
            // Render What-If Preset Buttons
            const wiContainer = document.getElementById('whatif-buttons-container');
            const whatifs = currentSparringRep.whatifs || [];
            if (whatifs.length > 0) {
                wiContainer.innerHTML = whatifs.map((wi, i) => `
                    <button onclick="loadWhatIfSequence(${i})" class="px-2 py-1 bg-slate-900 hover:bg-sky-700 text-slate-200 text-[11px] font-medium rounded border border-slate-700 transition">
                        ${wi.label}
                    </button>
                `).join('');
            } else {
                wiContainer.innerHTML = `<span class="text-slate-500 italic text-[11px]">Free play active</span>`;
            }

            resetSparringGame();
        }

        function loadWhatIfSequence(idx) {
            const wi = currentSparringRep.whatifs[idx];
            if (!wi) return;

            sparringGame.reset();
            for (let san of wi.seq) {
                sparringGame.move(san);
            }
            sparringBoard.position(sparringGame.fen());
            clearSparringArrows();
            updateSparringMovesUI();
            updateSparringStatus();
            updateSparringExplorerTable();

            document.getElementById('sparring-feedback-title').innerHTML = `<span class="text-amber-400 font-bold">🔀 Branch Loaded: ${wi.label}</span>`;
            document.getElementById('sparring-feedback-sub').innerText = `Jumped to position after: ${wi.seq.join(' ')}. You can now continue playing from here!`;
        }

        function resetSparringGame() {
            sparringGame.reset();
            sparringBoard.orientation(currentSparringRep.userSide);
            sparringBoard.position('start');
            clearSparringArrows();
            updateSparringStatus();
            updateSparringMovesUI();
            updateSparringExplorerTable();

            document.getElementById('sparring-feedback-title').innerText = "Make your opening move!";
            if (currentSparringRep.userSide === "white") {
                document.getElementById('sparring-feedback-sub').innerText = `Start with 1.${currentSparringRep.expectedFirst} to begin the ${currentSparringRep.title} drill.`;
            } else {
                document.getElementById('sparring-feedback-sub').innerText = "PC is playing White. Waiting for opening move...";
                setTimeout(makeBotMove, 400);
            }
        }

        function getMovesHistorySAN() {
            return sparringGame.history().join(" ");
        }

        function updateSparringExplorerTable() {
            const hist = getMovesHistorySAN();
            const turn = sparringGame.turn() === 'w' ? 'White' : 'Black';
            const isUserTurn = (turn.toLowerCase() === currentSparringRep.userSide);
            
            const candidates = masterOpeningDatabase[hist] || [];
            const tbody = document.getElementById('sparring-explorer-tbody');
            const evalBadge = document.getElementById('sparring-eval-badge');

            if (candidates.length === 0) {
                // Generate legal moves
                const legals = sparringGame.moves({ verbose: true });
                if (legals.length === 0) {
                    tbody.innerHTML = `<tr><td colspan="6" class="py-2 text-center text-slate-500">Game Over</td></tr>`;
                    evalBadge.innerText = "Game Over";
                    return;
                }
                evalBadge.innerText = "Open Play";
                tbody.innerHTML = legals.slice(0, 5).map(m => `
                    <tr class="hover:bg-slate-700/40 cursor-pointer" onclick="forcePlaySparringMove('${m.san}')">
                        <td class="py-1.5 px-3 font-bold text-slate-100">${m.san}</td>
                        <td class="py-1.5 px-2 text-slate-400 text-[11px]">Legal Move</td>
                        <td class="py-1.5 px-2 text-center text-slate-400 text-[11px]">--</td>
                        <td class="py-1.5 px-2 text-center font-bold text-slate-300">0.0</td>
                        <td class="py-1.5 px-3 text-center">
                            <div class="eval-bar-container">
                                <div class="bar-white" style="width: 50%">50%</div>
                                <div class="bar-black" style="width: 50%">50%</div>
                            </div>
                        </td>
                        <td class="py-1.5 px-2 text-center">
                            <button onclick="event.stopPropagation(); forcePlaySparringMove('${m.san}')" class="px-2 py-0.5 bg-sky-600 hover:bg-sky-500 text-white rounded text-[10px] font-bold">
                                ${isUserTurn ? 'Play' : 'Force Bot'}
                            </button>
                        </td>
                    </tr>
                `).join('');
                return;
            }

            evalBadge.innerText = `Master Book (${candidates[0].eval})`;
            tbody.innerHTML = candidates.map(c => `
                <tr class="hover:bg-slate-700/40 cursor-pointer" onclick="forcePlaySparringMove('${c.san}')">
                    <td class="py-1.5 px-3 font-bold text-slate-100">${c.san}</td>
                    <td class="py-1.5 px-2 text-slate-300 text-[11px] font-sans">${c.name || ''}</td>
                    <td class="py-1.5 px-2 text-center text-slate-400 text-[11px]">${c.games.toLocaleString()}</td>
                    <td class="py-1.5 px-2 text-center font-bold ${c.eval.startsWith('+') ? 'text-emerald-400' : 'text-rose-400'}">${c.eval}</td>
                    <td class="py-1.5 px-3 text-center">
                        <div class="eval-bar-container">
                            <div class="bar-white" style="width: ${c.w}%">${c.w}%</div>
                            <div class="bar-draw" style="width: ${c.d}%">${c.d}%</div>
                            <div class="bar-black" style="width: ${c.b}%">${c.b}%</div>
                        </div>
                    </td>
                    <td class="py-1.5 px-2 text-center">
                        <button onclick="event.stopPropagation(); forcePlaySparringMove('${c.san}')" class="px-2 py-0.5 ${isUserTurn ? 'bg-emerald-600 hover:bg-emerald-500' : 'bg-sky-600 hover:bg-sky-500'} text-white rounded text-[10px] font-bold transition">
                            ${isUserTurn ? '▶ Play' : '🤖 Force Bot'}
                        </button>
                    </td>
                </tr>
            `).join('');
        }

        function forcePlaySparringMove(sanMove) {
            const move = sparringGame.move(sanMove);
            if (!move) return;

            sparringBoard.position(sparringGame.fen());
            clearSparringArrows();
            updateSparringMovesUI();
            updateSparringStatus();
            updateSparringExplorerTable();

            if (sparringGame.game_over()) {
                handleSparringGameOver();
                return;
            }

            const turn = sparringGame.turn() === 'w' ? 'white' : 'black';
            if (turn !== currentSparringRep.userSide) {
                // Trigger Bot reply
                setTimeout(makeBotMove, 300);
            }
        }

        function onSparringDrop(source, target) {
            const turn = sparringGame.turn() === 'w' ? 'white' : 'black';
            if (turn !== currentSparringRep.userSide) return 'snapback';

            const move = sparringGame.move({
                from: source,
                to: target,
                promotion: 'q'
            });

            if (move === null) return 'snapback';

            clearSparringArrows();
            updateSparringMovesUI();
            updateSparringStatus();
            updateSparringExplorerTable();

            if (sparringGame.game_over()) {
                handleSparringGameOver();
                return;
            }

            setTimeout(makeBotMove, 300);
        }

        function getSmartFallbackMove() {
            const hist = getMovesHistorySAN();
            const legals = sparringGame.moves({ verbose: true });
            if (legals.length === 0) return null;

            const captures = legals.filter(m => m.captured);
            if (captures.length > 0) return captures[0].san;

            const centralPawns = legals.filter(m => m.piece === 'p' && ['d5','e5','c5','d4','e4','c4'].includes(m.to));
            if (centralPawns.length > 0) return centralPawns[0].san;

            const devMoves = legals.filter(m => ['n','b'].includes(m.piece) && ['f6','c6','f3','c3','e7','d7','e2','d2','b4','g4','c4','f4'].includes(m.to));
            if (devMoves.length > 0) return devMoves[0].san;

            const castle = legals.filter(m => m.san === 'O-O' || m.san === 'O-O-O');
            if (castle.length > 0) return castle[0].san;

            return legals[0].san;
        }

        function makeBotMove() {
            if (sparringGame.game_over()) return;

            const hist = getMovesHistorySAN();
            const candidates = masterOpeningDatabase[hist] || [];

            let chosenMove = null;

            if (candidates && candidates.length > 0) {
                // Weighted pick based on games count
                chosenMove = candidates[0].san;
                if (candidates.length > 1 && Math.random() > 0.4) {
                    chosenMove = candidates[1].san;
                }
            }

            if (!chosenMove) {
                chosenMove = getSmartFallbackMove();
            }

            if (chosenMove) {
                const res = sparringGame.move(chosenMove);
                if (res) {
                    sparringBoard.position(sparringGame.fen());
                    updateSparringMovesUI();
                    updateSparringStatus();
                    updateSparringExplorerTable();
                    document.getElementById('sparring-feedback-title').innerHTML = `<span class="text-emerald-400 font-bold">📖 Bot Plays: ${res.san}</span>`;
                    document.getElementById('sparring-feedback-sub').innerText = "Opponent is playing strictly according to theoretical master opening lines.";
                }
            }
        }

        function undoSparringMove() {
            sparringGame.undo();
            sparringGame.undo();
            sparringBoard.position(sparringGame.fen());
            clearSparringArrows();
            updateSparringMovesUI();
            updateSparringStatus();
            updateSparringExplorerTable();
        }

        function showSparringHint() {
            const legals = sparringGame.moves({ verbose: true });
            if (legals.length === 0) return;

            const hist = getMovesHistorySAN();
            const candidates = masterOpeningDatabase[hist] || [];
            
            let bestSan = legals[0].san;
            let bestFrom = legals[0].from;
            let bestTo = legals[0].to;

            if (candidates.length > 0) {
                bestSan = candidates[0].san;
                const found = legals.find(m => m.san === bestSan);
                if (found) {
                    bestFrom = found.from;
                    bestTo = found.to;
                }
            }

            drawSparringArrow(bestFrom, bestTo, "#22c55e", "spar-green");
            document.getElementById('sparring-feedback-sub').innerHTML = `<span class="text-amber-400 font-bold">💡 Recommended Move:</span> <strong>${bestSan}</strong> (from ${bestFrom} to ${bestTo})`;
        }

        function updateSparringStatus() {
            const turn = sparringGame.turn() === 'w' ? 'White' : 'Black';
            const isUser = (turn.toLowerCase() === currentSparringRep.userSide);
            const moveNum = Math.floor(sparringGame.history().length / 2) + 1;
            document.getElementById('sparring-game-status').innerText = `Move ${moveNum} | ${isUser ? 'Your Turn (' + turn + ')' : 'PC Thinking...'}`;
        }

        function updateSparringMovesUI() {
            const moves = sparringGame.history();
            const container = document.getElementById('sparring-moves-list');
            if (moves.length === 0) {
                container.innerHTML = `<span class="text-slate-500 italic">No moves played yet</span>`;
                return;
            }

            container.innerHTML = moves.map((m, i) => {
                const num = Math.floor(i/2) + 1;
                const pref = (i % 2 === 0) ? `${num}. ` : '';
                return `<span class="px-1.5 py-0.5 bg-slate-800 rounded text-slate-200 border border-slate-700">${pref}${m}</span>`;
            }).join('');
        }

        function drawSparringArrow(fromSq, toSq, color, markerId) {
            const svg = document.getElementById('sparring-arrows-svg');
            if (!svg) return;
            const boardEl = document.getElementById('sparring-board');
            const boardWidth = boardEl ? boardEl.clientWidth : 420;
            const orientation = currentSparringRep.userSide;

            const arrowHtml = drawSvgArrow(fromSq, toSq, color, markerId, orientation, boardWidth, false);
            svg.innerHTML = `
                <defs>
                    <marker id="spar-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#22c55e" />
                    </marker>
                    <marker id="spar-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#ef4444" />
                    </marker>
                </defs>
                ${arrowHtml}
            `;
        }

        function clearSparringArrows() {
            const svg = document.getElementById('sparring-arrows-svg');
            if (svg) {
                svg.innerHTML = `
                    <defs>
                        <marker id="spar-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#22c55e" />
                        </marker>
                        <marker id="spar-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#ef4444" />
                        </marker>
                    </defs>
                `;
            }
        }

        function handleSparringGameOver() {
            if (sparringGame.in_checkmate()) {
                const winner = sparringGame.turn() === 'w' ? 'Black' : 'White';
                document.getElementById('sparring-feedback-title').innerHTML = `<span class="text-amber-400 font-bold">🏆 Checkmate! ${winner} Wins!</span>`;
            } else if (sparringGame.in_draw()) {
                document.getElementById('sparring-feedback-title').innerHTML = `<span class="text-slate-300 font-bold">🤝 Game Drawn!</span>`;
            }
        }

        // ==========================================
        // PERSISTENT STUDY PROGRESS TRACKER
        // ==========================================
        const STORAGE_KEY_STUDIED = `chess_studied_${analysisData.username}`;
        const STORAGE_KEY_NOTES = `chess_notes_${analysisData.username}`;

        function getStudiedSet() {
            try {
                const raw = localStorage.getItem(STORAGE_KEY_STUDIED);
                return new Set(raw ? JSON.parse(raw) : []);
            } catch (e) {
                return new Set();
            }
        }

        function saveStudiedSet(studiedSet) {
            try {
                localStorage.setItem(STORAGE_KEY_STUDIED, JSON.stringify(Array.from(studiedSet)));
            } catch (e) {}
        }

        function getNotesDict() {
            try {
                const raw = localStorage.getItem(STORAGE_KEY_NOTES);
                return raw ? JSON.parse(raw) : {};
            } catch (e) {
                return {};
            }
        }

        function saveNotesDict(notesDict) {
            try {
                localStorage.setItem(STORAGE_KEY_NOTES, JSON.stringify(notesDict));
            } catch (e) {}
        }

        let currentStudyFilter = "all";

        function updateStudyProgressUI() {
            const studiedSet = getStudiedSet();
            const totalCount = analysisData.early_disasters.length;
            const studiedCount = Array.from(studiedSet).filter(idx => idx >= 0 && idx < totalCount).length;
            const unstudiedCount = totalCount - studiedCount;
            const pct = totalCount > 0 ? Math.round((studiedCount / totalCount) * 100) : 0;

            document.getElementById('study-count-text').innerText = `${studiedCount} / ${totalCount} Studied`;
            document.getElementById('study-pct-badge').innerText = `${pct}% Complete`;
            document.getElementById('study-progress-bar').style.width = `${pct}%`;

            document.getElementById('cnt-all').innerText = totalCount;
            document.getElementById('cnt-unstudied').innerText = unstudiedCount;
            document.getElementById('cnt-studied').innerText = studiedCount;

            const btn = document.getElementById('btn-toggle-study');
            if (btn) {
                if (studiedSet.has(currentGameIndex)) {
                    btn.innerHTML = `<span>✓</span> Studied (Click to Unmark)`;
                    btn.className = `px-3 py-1 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold rounded-lg transition shadow flex items-center gap-1.5 border border-emerald-400`;
                } else {
                    btn.innerHTML = `<span>✅</span> Mark as Studied`;
                    btn.className = `px-3 py-1 bg-slate-700 hover:bg-emerald-600 text-white text-xs font-bold rounded-lg transition shadow flex items-center gap-1.5`;
                }
            }

            renderGameSelectorOptions();
        }

        function toggleCurrentGameStudied() {
            const studiedSet = getStudiedSet();
            if (studiedSet.has(currentGameIndex)) {
                studiedSet.delete(currentGameIndex);
            } else {
                studiedSet.add(currentGameIndex);
            }
            saveStudiedSet(studiedSet);
            updateStudyProgressUI();
        }

        function filterStudiedGames(filter) {
            currentStudyFilter = filter;
            ['all', 'unstudied', 'studied'].forEach(f => {
                const btn = document.getElementById('btn-filter-' + f);
                if (btn) {
                    btn.className = (f === filter) ? 'px-2.5 py-1 bg-sky-600 rounded text-white font-medium' : 'px-2.5 py-1 bg-slate-900 hover:bg-slate-700 rounded text-slate-300 font-medium';
                }
            });
            renderGameSelectorOptions();
        }

        function renderGameSelectorOptions() {
            const studiedSet = getStudiedSet();
            const select = document.getElementById('game-select');
            if (!select) return;
            const total = analysisData.early_disasters.length;

            let html = "";
            for (let idx = 0; idx < total; idx++) {
                const g = analysisData.early_disasters[idx];
                const isStudied = studiedSet.has(idx);

                if (currentStudyFilter === "unstudied" && isStudied) continue;
                if (currentStudyFilter === "studied" && !isStudied) continue;

                const icon = isStudied ? "✅" : "⏳";
                const isSelected = (idx === currentGameIndex) ? "selected" : "";
                html += `<option value="${idx}" ${isSelected}>${icon} ${idx+1}. [${g.moves_count} moves] vs ${g.opp_name} (${g.opp_rating || '?'}) - ${g.opening}</option>`;
            }

            if (!html) {
                html = `<option value="">No games found in this filter</option>`;
            }
            select.innerHTML = html;
        }

        function jumpNextUnstudied() {
            const studiedSet = getStudiedSet();
            const total = analysisData.early_disasters.length;
            
            for (let idx = currentGameIndex + 1; idx < total; idx++) {
                if (!studiedSet.has(idx)) {
                    loadSelectedGame(idx);
                    return;
                }
            }
            for (let idx = 0; idx <= currentGameIndex; idx++) {
                if (!studiedSet.has(idx)) {
                    loadSelectedGame(idx);
                    return;
                }
            }
            alert("🎉 Amazing! You have studied all 40 lost games in this dataset!");
        }

        function saveCurrentGameNote(noteText) {
            const notesDict = getNotesDict();
            notesDict[currentGameIndex] = noteText;
            saveNotesDict(notesDict);
        }

        function loadCurrentGameNote() {
            const notesDict = getNotesDict();
            const noteInput = document.getElementById('game-user-note');
            if (noteInput) noteInput.value = notesDict[currentGameIndex] || "";
        }

        // ==========================================
        // STOCKFISH ARROW DRAWING ENGINE
        // ==========================================
        let showArrows = true;

        function toggleArrowDisplay() {
            showArrows = !showArrows;
            const btn = document.getElementById('btn-arrow-toggle');
            if (showArrows) {
                btn.innerHTML = `<span>🎯</span> Arrow: ON`;
                btn.className = `text-xs text-emerald-400 hover:text-emerald-300 font-semibold flex items-center gap-1 bg-slate-800 px-2 py-0.5 rounded border border-emerald-500/40`;
            } else {
                btn.innerHTML = `<span>🎯</span> Arrow: OFF`;
                btn.className = `text-xs text-slate-400 hover:text-slate-300 font-semibold flex items-center gap-1 bg-slate-800 px-2 py-0.5 rounded border border-slate-700`;
            }
            renderReplayArrows();
        }

        function getSquareCenter(square, orientation, boardWidth) {
            if (!square || square.length < 2) return null;
            const sqSize = boardWidth / 8.0;
            const files = 'abcdefgh';
            const fileIdx = files.indexOf(square[0].toLowerCase());
            const rankNum = parseInt(square[1]);

            if (fileIdx === -1 || isNaN(rankNum) || rankNum < 1 || rankNum > 8) return null;

            let x, y;
            if (orientation === 'white') {
                x = (fileIdx + 0.5) * sqSize;
                y = (8 - rankNum + 0.5) * sqSize;
            } else {
                x = (7 - fileIdx + 0.5) * sqSize;
                y = (rankNum - 1 + 0.5) * sqSize;
            }
            return { x, y, sqSize };
        }

        function drawSvgArrow(fromSq, toSq, color, markerId, orientation, boardWidth, isDashed = false) {
            const p1 = getSquareCenter(fromSq, orientation, boardWidth);
            const p2 = getSquareCenter(toSq, orientation, boardWidth);
            if (!p1 || !p2) return "";

            const dx = p2.x - p1.x;
            const dy = p2.y - p1.y;
            const dist = Math.hypot(dx, dy);
            if (dist === 0) return "";

            const shorten = p1.sqSize * 0.28;
            const targetX = p2.x - (dx / dist) * shorten;
            const targetY = p2.y - (dy / dist) * shorten;

            const strokeWidth = p1.sqSize * 0.16;
            const radius = p1.sqSize * 0.12;
            const dashAttr = isDashed ? 'stroke-dasharray="6,4"' : '';

            return `
                <circle cx="${p1.x}" cy="${p1.y}" r="${radius}" fill="${color}" opacity="0.85" />
                <line x1="${p1.x}" y1="${p1.y}" x2="${targetX}" y2="${targetY}" stroke="${color}" stroke-width="${strokeWidth}" stroke-linecap="round" marker-end="url(#${markerId})" opacity="0.85" ${dashAttr} />
            `;
        }

        function renderReplayArrows() {
            const svg = document.getElementById('replay-arrows-svg');
            if (!svg) return;

            if (!showArrows) {
                svg.innerHTML = `
                    <defs>
                        <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#22c55e" />
                        </marker>
                        <marker id="arrow-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#ef4444" />
                        </marker>
                    </defs>
                `;
                return;
            }

            const g = analysisData.early_disasters[currentGameIndex];
            if (!g) return;

            const boardEl = document.getElementById('replay-board');
            const boardWidth = boardEl ? boardEl.clientWidth : 420;
            const orientation = g.color.toLowerCase();
            const sfList = g.stockfish_analysis || [];

            let arrowsHtml = `
                <defs>
                    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#22c55e" />
                    </marker>
                    <marker id="arrow-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#ef4444" />
                    </marker>
                </defs>
            `;

            if (currentPly > 0 && currentPly <= sfList.length) {
                const plyData = sfList[currentPly - 1];

                if (plyData.played_uci && (plyData.quality === 'Blunder' || plyData.quality === 'Mistake' || plyData.quality === 'Inaccuracy')) {
                    const fromSq = plyData.played_uci.substring(0, 2);
                    const toSq = plyData.played_uci.substring(2, 4);
                    arrowsHtml += drawSvgArrow(fromSq, toSq, "#ef4444", "arrow-red", orientation, boardWidth, true);
                }

                if (plyData.best_uci) {
                    const fromSq = plyData.best_uci.substring(0, 2);
                    const toSq = plyData.best_uci.substring(2, 4);
                    arrowsHtml += drawSvgArrow(fromSq, toSq, "#22c55e", "arrow-green", orientation, boardWidth, false);
                }
            }

            svg.innerHTML = arrowsHtml;
        }

        // ==========================================
        // STOCKFISH REPLAYER ENGINE
        // ==========================================
        let replayBoard = null;
        let currentGameIndex = 0;
        let currentPly = 0;
        let currentFens = [];

        function initReplayer() {
            replayBoard = Chessboard('replay-board', {
                position: 'start',
                pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png'
            });

            updateStudyProgressUI();

            if (analysisData.early_disasters.length > 0) {
                loadSelectedGame(0);
            }

            window.addEventListener('resize', () => {
                if (replayBoard) replayBoard.resize();
                if (sparringBoard) sparringBoard.resize();
                renderReplayArrows();
            });
        }

        function loadSelectedGame(idx) {
            if (idx === "" || idx === null || isNaN(idx)) return;
            currentGameIndex = parseInt(idx);
            const g = analysisData.early_disasters[currentGameIndex];
            if (!g) return;

            document.getElementById('meta-opening').innerText = g.opening;
            document.getElementById('meta-opp').innerText = `${g.opp_name} (${g.opp_rating || '?'})`;
            document.getElementById('meta-result').innerText = `${g.result} in ${g.moves_count} moves`;
            document.getElementById('meta-link').href = g.url;

            if (g.coach_advice) {
                document.getElementById('coach-card').classList.remove('hidden');
                document.getElementById('coach-never-rule').innerText = g.coach_advice.never_rule;
                document.getElementById('coach-explanation').innerText = g.coach_advice.explanation;
                document.getElementById('coach-ply-tag').innerText = `Critical Move: Move ${g.coach_advice.move_num}`;
            }

            loadCurrentGameNote();
            updateStudyProgressUI();

            currentFens = g.fens;
            currentPly = 0;

            replayBoard.orientation(g.color.toLowerCase());
            replayBoard.position(currentFens[0]);

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
            
            document.querySelectorAll('#moves-container span').forEach(el => el.classList.remove('bg-sky-500/30', 'text-sky-300'));
            const curEl = document.getElementById(`ply-${currentPly}`);
            if (curEl) {
                curEl.classList.add('bg-sky-500/30', 'text-sky-300');
            }

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

            renderReplayArrows();
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
                    { uci: "d2d4", san: "d4", comment: "1. d4 - Start with Queen's Pawn", eval: "+0.3", candidates: [{ san: "d4", games: 1845000, eval: "+0.3", w: 38, d: 34, b: 28 }] },
                    { uci: "e7e5", san: "e5", comment: "Opponent plays Englund Gambit", eval: "+1.6", candidates: [{ san: "dxe5", games: 98000, eval: "+1.6", w: 62, d: 18, b: 20 }] },
                    { uci: "d4e5", san: "dxe5", comment: "2. dxe5 - Accept the gambit pawn", eval: "+1.6", candidates: [{ san: "Nc6", games: 64000, eval: "+1.6", w: 60, d: 19, b: 21 }] },
                    { uci: "b8c6", san: "Nc6", comment: "Opponent develops knight", eval: "+1.7", candidates: [{ san: "Nf3", games: 58000, eval: "+1.7", w: 61, d: 19, b: 20 }] },
                    { uci: "g1f3", san: "Nf3", comment: "3. Nf3 - Guard e5 securely", eval: "+1.7", candidates: [{ san: "Qe7", games: 44000, eval: "+1.7", w: 62, d: 18, b: 20 }] },
                    { uci: "d8e7", san: "Qe7", comment: "Black attacks e5 again", eval: "+1.8", candidates: [{ san: "Bf4", games: 32000, eval: "+1.8", w: 63, d: 18, b: 19 }] },
                    { uci: "c1f4", san: "Bf4", comment: "4. Bf4 - Defend e5 and invite the trap", eval: "+1.8", candidates: [{ san: "Qb4+", games: 28000, eval: "+1.8", w: 63, d: 18, b: 19 }] },
                    { uci: "e7b4", san: "Qb4+", comment: "TRAP MOVE! Black forks King and Bishop", eval: "+3.5", candidates: [{ san: "Bd2!", games: 22000, eval: "+3.5", w: 74, d: 14, b: 12 }] },
                    { uci: "f4d2", san: "Bd2!", comment: "5. Bd2! - The Winning Move! Never play Qd2", eval: "+3.5", candidates: [{ san: "Qxb2", games: 18000, eval: "+3.5", w: 75, d: 13, b: 12 }] },
                    { uci: "b4b2", san: "Qxb2", comment: "Black greedily captures on b2", eval: "+3.8", candidates: [{ san: "Nc3!", games: 14000, eval: "+3.8", w: 78, d: 12, b: 10 }] },
                    { uci: "b1c3", san: "Nc3!", comment: "6. Nc3! - Threatens 7.Rb1 and 7.Nd5! Total victory.", eval: "+3.8", candidates: [{ san: "Bb4", games: 9000, eval: "+3.8", w: 78, d: 12, b: 10 }] }
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

        $(document).ready(function() {
            initSparring();
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
    print(f"Generated interactive dashboard with What-If & Top 5 Explorer: {output_path}")
    return output_path
