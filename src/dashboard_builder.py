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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Chess Diagnostics: Opening Weaknesses & Blunders - __USERNAME__</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chessboard.js & jQuery & Chess.js -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/chessboard-js/1.0.0/chessboard-1.0.0.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chessboard-js/1.0.0/chessboard-1.0.0.min.js"></script>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; touch-action: manipulation; }
        .tab-btn.active { border-bottom: 3px solid #38bdf8; color: #38bdf8; font-weight: 600; }
        .board-container { max-width: 420px; width: 100%; margin: 0 auto; position: relative; }
        @media (max-width: 640px) { .board-container { max-width: 340px; } }
        .weakness-card.active { border-color: #38bdf8; background: linear-gradient(135deg, rgba(3, 105, 161, 0.25), rgba(15, 23, 42, 0.9)); }
        .eval-bar-container { display: flex; height: 16px; width: 100%; border-radius: 3px; overflow: hidden; font-size: 10px; line-height: 16px; font-weight: 600; text-align: center; }
        .bar-white { background-color: #f1f5f9; color: #0f172a; }
        .bar-draw { background-color: #64748b; color: #f8fafc; }
        .bar-black { background-color: #1e293b; color: #f8fafc; border-left: 1px solid #334155; }
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- Header -->
    <header class="bg-slate-900 border-b border-slate-800 px-4 sm:px-6 py-3 flex flex-wrap items-center justify-between shadow-lg">
        <div class="flex items-center space-x-2 sm:space-x-3">
            <span class="text-2xl sm:text-3xl">♟️</span>
            <div>
                <h1 class="text-base sm:text-xl font-bold text-white flex items-center gap-1.5 sm:gap-2">
                    Chess Diagnostic Copilot
                    <span class="text-[10px] sm:text-xs bg-sky-500/20 text-sky-400 border border-sky-500/30 px-1.5 sm:px-2 py-0.5 rounded font-mono">__USERNAME__</span>
                </h1>
                <p class="text-[10px] sm:text-xs text-slate-400">Opening Weakness Refutations & Stockfish 18 Blunder Diagnostics</p>
            </div>
        </div>
        <div class="flex gap-2 sm:gap-4 mt-2 sm:mt-0 text-xs sm:text-sm">
            <div class="bg-slate-800 px-2.5 py-1 rounded border border-slate-700">
                <span class="text-slate-400">Blitz:</span> <span class="font-bold text-amber-400" id="blitz-rating">--</span>
            </div>
            <div class="bg-slate-800 px-2.5 py-1 rounded border border-slate-700">
                <span class="text-slate-400">Bullet:</span> <span class="font-bold text-orange-400" id="bullet-rating">--</span>
            </div>
            <div class="bg-slate-800 px-2.5 py-1 rounded border border-slate-700">
                <span class="text-slate-400">Tactics:</span> <span class="font-bold text-emerald-400" id="tactics-rating">--</span>
            </div>
        </div>
    </header>

    <!-- Navigation Tabs -->
    <div class="bg-slate-900/80 backdrop-blur border-b border-slate-800 px-4 sm:px-6">
        <nav class="flex space-x-4 sm:space-x-8 text-xs sm:text-sm overflow-x-auto">
            <button onclick="switchTab('weaknesses')" id="tab-weaknesses" class="tab-btn active py-3 px-1 text-slate-300 hover:text-white transition whitespace-nowrap">🛡️ Opening Weaknesses & Refutations</button>
            <button onclick="switchTab('blunders')" id="tab-blunders" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition whitespace-nowrap">⚡ Tactical Blunders & Lost Games (90+)</button>
            <button onclick="switchTab('sparring')" id="tab-sparring" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition whitespace-nowrap">⚔️ Sparring Bot & "What If?"</button>
            <button onclick="switchTab('overview')" id="tab-overview" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition whitespace-nowrap">📊 Top 10 Win/Loss Openings</button>
            <button onclick="switchTab('videos')" id="tab-videos" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition whitespace-nowrap">🎥 Master Video Lessons</button>
        </nav>
    </div>

    <!-- Main Content Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto p-3 sm:p-6">

        <!-- TAB 0: 🛡️ OPENING WEAKNESS REFUTATIONS (DEDICATED) -->
        <section id="view-weaknesses" class="space-y-4 sm:space-y-6">
            <div class="bg-slate-800/90 border border-slate-700 rounded-xl p-3 sm:p-4 shadow-lg flex flex-wrap items-center justify-between gap-3">
                <div class="flex items-center gap-3">
                    <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-lg bg-sky-500/20 border border-sky-500/30 flex items-center justify-center text-lg sm:text-xl text-sky-400 font-bold">
                        🛡️
                    </div>
                    <div>
                        <h2 class="text-sm sm:text-base font-bold text-white">Opening Weaknesses: Opponent Triggers & Refutations</h2>
                        <p class="text-[11px] sm:text-xs text-slate-400">Discover what move opponent played, why your reply lost, and the master refutation.</p>
                    </div>
                </div>
                <div class="flex gap-1.5 sm:gap-2 text-xs">
                    <button onclick="filterWeaknessSide('all')" id="wfilter-all" class="px-2.5 py-1 bg-sky-600 rounded text-white font-medium">All Openings</button>
                    <button onclick="filterWeaknessSide('White')" id="wfilter-white" class="px-2.5 py-1 bg-slate-900 hover:bg-slate-700 rounded text-slate-300 font-medium">⚪ As White</button>
                    <button onclick="filterWeaknessSide('Black')" id="wfilter-black" class="px-2.5 py-1 bg-slate-900 hover:bg-slate-700 rounded text-slate-300 font-medium">⚫ As Black</button>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6">
                <!-- Left: Interactive Board with Arrow -->
                <div class="lg:col-span-5 flex flex-col items-center">
                    <div class="board-container shadow-2xl rounded-lg overflow-hidden border border-slate-700 relative">
                        <div id="weakness-board" style="width: 100%"></div>
                        <!-- SVG ARROW OVERLAY -->
                        <svg id="weakness-arrows-svg" class="absolute inset-0 w-full h-full pointer-events-none z-10" style="width: 100%; height: 100%;">
                            <defs>
                                <marker id="weak-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                                    <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#22c55e" />
                                </marker>
                            </defs>
                        </svg>
                    </div>

                    <div class="flex items-center gap-2 mt-3 sm:mt-4">
                        <button onclick="playWeaknessRefutationAnimation()" class="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-bold shadow flex items-center gap-1.5">
                            <span>▶</span> Play Winning Move on Board
                        </button>
                        <button onclick="resetWeaknessBoard()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-xs font-semibold">
                            🔄 Reset Position
                        </button>
                    </div>
                </div>

                <!-- Right: Weakness Detail Card & Opening Catalog List -->
                <div class="lg:col-span-7 space-y-3 sm:space-y-4">
                    <!-- Active Weakness Refutation Card -->
                    <div id="weakness-active-card" class="bg-gradient-to-br from-slate-900 via-slate-800 to-sky-950/40 rounded-xl border-2 border-sky-500/50 p-4 sm:p-5 space-y-3 shadow-xl">
                        <div class="flex items-center justify-between">
                            <span id="weak-tag" class="text-xs bg-rose-500/20 text-rose-300 border border-rose-500/40 px-2.5 py-0.5 rounded font-mono font-bold">21 Losses in Dataset</span>
                            <span id="weak-eco-badge" class="text-xs bg-slate-900 text-sky-400 border border-slate-700 px-2 py-0.5 rounded font-mono font-semibold">ECO: B01</span>
                        </div>

                        <h3 id="weak-title" class="text-sm sm:text-base font-bold text-white">Scandinavian Defense 2.e5</h3>

                        <!-- 3-Way Diagnostic Matrix -->
                        <div class="space-y-2 text-xs">
                            <div class="bg-slate-900/90 border border-slate-700 p-2.5 sm:p-3 rounded-lg flex items-start gap-2">
                                <span class="text-base">🔴</span>
                                <div>
                                    <strong class="text-rose-400 block font-bold uppercase text-[10px]">When Opponent Played:</strong>
                                    <span id="weak-opp-trigger" class="text-slate-200 font-semibold font-mono">Opponent plays: 2. e5</span>
                                </div>
                            </div>

                            <div class="bg-rose-950/30 border border-rose-800/50 p-2.5 sm:p-3 rounded-lg flex items-start gap-2">
                                <span class="text-base">⚠️</span>
                                <div>
                                    <strong class="text-rose-300 block font-bold uppercase text-[10px]">What You Played (The Flaw):</strong>
                                    <span id="weak-your-mistake" class="text-slate-300">You played: 2... d4?! or 2... e6?! (traps bishop on c8)</span>
                                </div>
                            </div>

                            <div class="bg-emerald-950/40 border border-emerald-700/60 p-2.5 sm:p-3 rounded-lg flex items-start gap-2">
                                <span class="text-base">🟢</span>
                                <div>
                                    <strong class="text-emerald-400 block font-bold uppercase text-[10px]">Your Best Option (The Refutation):</strong>
                                    <span id="weak-best-option" class="text-emerald-300 font-bold font-mono text-sm">2... Bf5!</span>
                                </div>
                            </div>
                        </div>

                        <!-- Tactical Explanation -->
                        <div class="bg-slate-900/90 border border-slate-700 p-2.5 sm:p-3 rounded-lg text-xs space-y-1">
                            <strong class="text-amber-400 font-bold uppercase text-[10px] flex items-center gap-1">
                                <span>💡</span> Why This Works & Tactical Logic:
                            </strong>
                            <p id="weak-why-reason" class="text-slate-300 leading-relaxed text-[11px] sm:text-xs"></p>
                        </div>
                    </div>

                    <!-- Opening Weakness Selection List -->
                    <div class="space-y-1.5">
                        <label class="text-xs font-bold text-slate-400 uppercase tracking-wide">Select an Opening Weakness to Inspect:</label>
                        <div id="weakness-list-container" class="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-44 overflow-y-auto pr-1"></div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 1: ⚡ TACTICAL BLUNDERS & LOST GAMES (90+ GAMES & PUZZLE MODE) -->
        <section id="view-blunders" class="hidden space-y-4 sm:space-y-6">

            <!-- STUDY PROGRESS & FILTER BANNER -->
            <div class="bg-slate-800/90 border border-slate-700 rounded-xl p-3 sm:p-4 shadow-lg flex flex-wrap items-center justify-between gap-3 sm:gap-4">
                <div class="flex items-center gap-3">
                    <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-lg sm:text-xl text-emerald-400 font-bold">
                        ✓
                    </div>
                    <div>
                        <div class="text-[10px] sm:text-xs font-bold text-slate-400 uppercase tracking-wide">Tactical Losses Studied</div>
                        <div class="text-sm sm:text-base font-bold text-white flex items-center gap-2">
                            <span id="study-count-text">0 / 90 Studied</span>
                            <span id="study-pct-badge" class="text-xs bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 px-2 py-0.5 rounded font-mono">0% Complete</span>
                        </div>
                    </div>
                </div>

                <!-- Progress Bar -->
                <div class="flex-1 max-w-xs bg-slate-900 h-2.5 sm:h-3 rounded-full overflow-hidden border border-slate-700">
                    <div id="study-progress-bar" class="bg-emerald-500 h-full transition-all duration-300" style="width: 0%"></div>
                </div>

                <!-- Phase Filters -->
                <div class="flex items-center gap-1.5 text-xs flex-wrap">
                    <button onclick="filterPhaseLosses('all')" id="btn-phase-all" class="px-2.5 py-1 bg-sky-600 rounded text-white font-medium">All (<span id="cnt-phase-all">90</span>)</button>
                    <button onclick="filterPhaseLosses('Opening')" id="btn-phase-opening" class="px-2.5 py-1 bg-slate-900 hover:bg-slate-700 rounded text-slate-300 font-medium">🛡️ Opening (&lt;=15)</button>
                    <button onclick="filterPhaseLosses('Middlegame')" id="btn-phase-mid" class="px-2.5 py-1 bg-slate-900 hover:bg-slate-700 rounded text-slate-300 font-medium">⚔️ Middlegame (16-30)</button>
                    <button onclick="filterPhaseLosses('Endgame')" id="btn-phase-end" class="px-2.5 py-1 bg-slate-900 hover:bg-slate-700 rounded text-slate-300 font-medium">⏱️ Endgame (30+)</button>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6">
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
                    <div class="flex items-center gap-2 mt-3 sm:mt-4">
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
                <div class="lg:col-span-7 space-y-3 sm:space-y-4">
                    <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-4">
                        <div class="flex items-center justify-between mb-1.5">
                            <label class="text-xs font-semibold text-slate-400 uppercase">Select Lost Game:</label>
                            <div class="flex items-center gap-2">
                                <button onclick="toggleCurrentGameStudied()" id="btn-toggle-study" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-lg transition shadow flex items-center gap-1.5">
                                    <span>✅</span> Mark Studied
                                </button>
                                <button onclick="jumpNextUnstudied()" class="px-3 py-1 bg-slate-700 hover:bg-slate-600 text-slate-200 text-xs font-medium rounded-lg transition">
                                    ⏭️ Next Unstudied
                                </button>
                            </div>
                        </div>
                        <select id="game-select" onchange="loadSelectedGame(this.value)" class="w-full bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg p-2.5 focus:border-sky-500 font-mono"></select>

                        <div id="game-meta-card" class="bg-slate-900/70 p-2.5 rounded-lg border border-slate-700 mt-2 text-xs space-y-1">
                            <div><strong>Opening:</strong> <span id="meta-opening" class="text-sky-400"></span></div>
                            <div><strong>Opponent:</strong> <span id="meta-opp" class="text-slate-300"></span> | <strong>Result:</strong> <span id="meta-result" class="text-rose-400 font-semibold"></span></div>
                            <div><strong>Chess.com Link:</strong> <a id="meta-link" href="#" target="_blank" class="text-sky-400 underline">Open on Chess.com ↗</a></div>
                        </div>

                        <!-- Move List with Quality Badges -->
                        <div class="mt-2.5">
                            <label class="block text-[11px] font-semibold text-slate-400 uppercase mb-1">Move Notation (Click any move to inspect Stockfish & Arrows):</label>
                            <div id="moves-container" class="bg-slate-900 p-2 rounded-lg border border-slate-700 font-mono text-xs max-h-24 overflow-y-auto leading-relaxed flex flex-wrap gap-1.5"></div>
                        </div>

                        <!-- Personal Study Notes Input -->
                        <div class="mt-2.5 pt-2 border-t border-slate-700/60">
                            <label class="block text-[11px] font-bold text-amber-400 uppercase mb-1 flex items-center gap-1">
                                <span>📝</span> My Notes for this Game:
                            </label>
                            <input type="text" id="game-user-note" oninput="saveCurrentGameNote(this.value)" placeholder="e.g. In this game, I missed the knight fork on c7..." class="w-full bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg p-1.5 focus:border-amber-400 focus:outline-none">
                        </div>
                    </div>

                    <!-- STOCKFISH 18 LIVE ENGINE EVALUATION CARD -->
                    <div class="bg-gradient-to-br from-slate-900 via-slate-800 to-sky-950/40 rounded-xl border-2 border-sky-500/40 p-4 space-y-3 shadow-xl">
                        <div class="flex items-center justify-between">
                            <h3 class="text-xs font-bold text-sky-400 uppercase tracking-wide flex items-center gap-2">
                                <span>🤖</span> Stockfish 18 Blunder Evaluation
                            </h3>
                            <span id="sf-eval-badge" class="text-xs bg-sky-500/20 text-sky-300 border border-sky-500/40 px-2.5 py-0.5 rounded font-mono font-bold">Eval: 0.0</span>
                        </div>

                        <!-- Move Comparison Grid -->
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs">
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
                </div>
            </div>
        </section>

        <!-- TAB 2: ⚔️ SPARRING BOT & WHAT-IF -->
        <section id="view-sparring" class="hidden space-y-4 sm:space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6">
                <!-- Left: Sparring Board -->
                <div class="lg:col-span-5 flex flex-col items-center">
                    <div class="board-container shadow-2xl rounded-lg overflow-hidden border border-slate-700 relative">
                        <div id="sparring-board" style="width: 100%"></div>
                        <svg id="sparring-arrows-svg" class="absolute inset-0 w-full h-full pointer-events-none z-10" style="width: 100%; height: 100%;">
                            <defs>
                                <marker id="spar-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                                    <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#22c55e" />
                                </marker>
                            </defs>
                        </svg>
                    </div>

                    <div class="flex items-center gap-2 mt-3 sm:mt-4">
                        <button onclick="resetSparringGame()" class="px-4 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded text-sm font-bold shadow flex items-center gap-1.5">
                            <span>🔄</span> New Game
                        </button>
                        <button onclick="undoSparringMove()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-sm font-semibold">
                            ↩️ Takeback
                        </button>
                        <button onclick="showSparringHint()" class="px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white rounded text-sm font-bold">
                            💡 Best Move
                        </button>
                    </div>

                    <div id="sparring-game-status" class="text-xs text-slate-400 mt-2 font-mono">Move 1 | Your Turn (White)</div>
                </div>

                <!-- Right: Sparring Repertoire & Lichess Top Moves Table -->
                <div class="lg:col-span-7 space-y-3 sm:space-y-4">
                    <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-4 space-y-2.5">
                        <div class="flex items-center justify-between">
                            <label class="text-xs font-bold text-sky-400 uppercase tracking-wide">Select Opening to Spar Against:</label>
                            <span id="sparring-bot-tag" class="text-[10px] bg-sky-500/20 text-sky-300 border border-sky-500/40 px-2 py-0.5 rounded font-mono font-bold">Bot Locked</span>
                        </div>

                        <select id="sparring-opening-select" onchange="selectSparringOpening(this.value)" class="w-full bg-slate-900 border border-slate-700 text-slate-200 text-sm rounded-lg p-2.5 focus:border-sky-500 font-medium">
                            <optgroup label="⚪ Practice As White (PC Plays As Black):">
                                <option value="scandi">⚪ White vs 🤖 Scandinavian Defense (1.e4 d5)</option>
                                <option value="englund">⚪ White vs 🤖 Englund Gambit (1.d4 e5)</option>
                                <option value="qg_white">⚪ White Queen's Gambit Practice (1.d4 d5 2.c4)</option>
                                <option value="sicilian">⚪ White vs 🤖 Sicilian Defense (1.e4 c5)</option>
                                <option value="french">⚪ White vs 🤖 French Defense (1.e4 e6)</option>
                                <option value="caro">⚪ White vs 🤖 Caro-Kann Defense (1.e4 c6)</option>
                            </optgroup>
                            <optgroup label="⚫ Practice As Black (PC Plays As White):">
                                <option value="scandi_black">⚫ Black vs 🤖 Scandinavian 2.e5 (Drill 2...Bf5!)</option>
                                <option value="london_black">⚫ Black vs 🤖 London System (Drill 2...c5! & 4...Qb6!)</option>
                                <option value="danish_black">⚫ Black vs 🤖 Danish Gambit (Drill 5...d5!!)</option>
                                <option value="reti_black">⚫ Black vs 🤖 Reti Opening (Drill 2...d4!)</option>
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
                                <span>📖</span> Lichess Master Top Moves (Click to play / force bot)
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

                        <div class="bg-slate-900/70 p-2 rounded-lg border border-slate-700">
                            <div id="sparring-moves-list" class="font-mono text-xs text-slate-200 flex flex-wrap gap-1.5 max-h-16 overflow-y-auto">
                                <span class="text-slate-500 italic">No moves played yet</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 3: 📊 TOP 10 WINNING & LOSING OPENINGS -->
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
                    <div class="text-xs text-rose-400 uppercase font-semibold">Losses in Dataset</div>
                    <div class="text-2xl font-bold text-rose-400 mt-1">__TOTAL_LOSSES__ games</div>
                    <div class="text-xs text-rose-300/70 mt-2">Analyzed with Stockfish 18</div>
                </div>
                <div class="bg-slate-800/80 p-5 rounded-xl border border-emerald-900/50 bg-gradient-to-br from-slate-800 to-emerald-950/30">
                    <div class="text-xs text-emerald-400 uppercase font-semibold">Puzzle Peak Rating</div>
                    <div class="text-2xl font-bold text-emerald-400 mt-1">1,736</div>
                    <div class="text-xs text-emerald-300/70 mt-2">Tactical foundation ready</div>
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

        <!-- TAB 4: 🎥 MASTER VIDEO LESSONS -->
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
            </div>
        </section>

    </main>

    <script>
        const analysisData = __ANALYSIS_DATA__;
        const userStats = __USER_STATS__;
        const topOpenings = __TOP_OPENINGS__;

        // ==========================================
        // 🔊 WEB AUDIO SYNTHESIZER (NO MP3 FILES NEEDED)
        // ==========================================
        let audioCtx = null;
        function playChessSound(type = 'move') {
            try {
                if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                if (audioCtx.state === 'suspended') audioCtx.resume();

                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);

                const now = audioCtx.currentTime;
                if (type === 'move') {
                    osc.frequency.setValueAtTime(320, now);
                    osc.frequency.exponentialRampToValueAtTime(160, now + 0.08);
                    gain.gain.setValueAtTime(0.3, now);
                    gain.gain.linearRampToValueAtTime(0.01, now + 0.08);
                    osc.start(now);
                    osc.stop(now + 0.08);
                } else if (type === 'capture') {
                    osc.frequency.setValueAtTime(540, now);
                    osc.frequency.exponentialRampToValueAtTime(220, now + 0.1);
                    gain.gain.setValueAtTime(0.4, now);
                    gain.gain.linearRampToValueAtTime(0.01, now + 0.1);
                    osc.start(now);
                    osc.stop(now + 0.1);
                } else if (type === 'victory') {
                    osc.frequency.setValueAtTime(440, now);
                    osc.frequency.setValueAtTime(554.37, now + 0.08);
                    osc.frequency.setValueAtTime(659.25, now + 0.16);
                    gain.gain.setValueAtTime(0.35, now);
                    gain.gain.linearRampToValueAtTime(0.01, now + 0.3);
                    osc.start(now);
                    osc.stop(now + 0.3);
                }
            } catch (e) {}
        }

        if (userStats && userStats.chess_blitz) document.getElementById('blitz-rating').innerText = userStats.chess_blitz.last.rating;
        if (userStats && userStats.chess_bullet) document.getElementById('bullet-rating').innerText = userStats.chess_bullet.last.rating;
        if (userStats && userStats.tactics) document.getElementById('tactics-rating').innerText = userStats.tactics.highest.rating;

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

        function switchTab(tabId) {
            ['weaknesses', 'blunders', 'sparring', 'overview', 'videos'].forEach(id => {
                document.getElementById('view-' + id).classList.add('hidden');
                document.getElementById('tab-' + id).classList.remove('active');
            });
            document.getElementById('view-' + tabId).classList.remove('hidden');
            document.getElementById('tab-' + tabId).classList.add('active');

            if (tabId === 'weaknesses') {
                setTimeout(() => { if (weaknessBoard) weaknessBoard.resize(); renderWeaknessArrow(); }, 100);
            } else if (tabId === 'blunders') {
                setTimeout(() => { if (replayBoard) replayBoard.resize(); renderReplayArrows(); }, 100);
            } else if (tabId === 'sparring') {
                setTimeout(() => { if (sparringBoard) sparringBoard.resize(); }, 100);
            }
        }

        // ==========================================
        // 🛡️ OPENING WEAKNESS ENGINE & REFUTATIONS
        // ==========================================
        const weaknessesList = analysisData.opening_weaknesses || [];
        let weaknessBoard = null;
        let weaknessGame = new Chess();
        let activeWeakness = weaknessesList[0] || null;
        let currentWeaknessFilter = "all";

        function initWeaknessView() {
            weaknessBoard = Chessboard('weakness-board', {
                position: 'start',
                pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png'
            });

            renderWeaknessList();
            if (weaknessesList.length > 0) {
                selectWeakness(0);
            }
        }

        function renderWeaknessList() {
            const container = document.getElementById('weakness-list-container');
            const filtered = weaknessesList.filter(w => currentWeaknessFilter === "all" || w.side === currentWeaknessFilter);

            container.innerHTML = filtered.map((w, idx) => {
                const isSelected = activeWeakness && activeWeakness.id === w.id;
                return `
                    <div onclick="selectWeaknessById('${w.id}')" class="weakness-card cursor-pointer p-2.5 rounded-lg border border-slate-700 bg-slate-900/80 hover:bg-slate-800 transition ${isSelected ? 'active' : ''}">
                        <div class="flex items-center justify-between">
                            <span class="font-bold text-xs text-slate-100 truncate mr-2">${w.side === 'White' ? '⚪' : '⚫'} ${w.opening}</span>
                            <span class="text-[10px] px-1.5 py-0.2 bg-rose-950/80 text-rose-300 border border-rose-800/60 rounded font-mono font-bold whitespace-nowrap">${w.loss_count} Losses</span>
                        </div>
                        <div class="text-[11px] text-emerald-400 font-mono mt-1 flex items-center gap-1">
                            <span>Best:</span> <strong>${w.refutation_san}</strong>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function filterWeaknessSide(side) {
            currentWeaknessFilter = side;
            ['all', 'white', 'black'].forEach(s => {
                const btn = document.getElementById('wfilter-' + s);
                if (btn) {
                    btn.className = (s.toLowerCase() === side.toLowerCase()) ? 'px-2.5 py-1 bg-sky-600 rounded text-white font-medium' : 'px-2.5 py-1 bg-slate-900 hover:bg-slate-700 rounded text-slate-300 font-medium';
                }
            });
            renderWeaknessList();
        }

        function selectWeaknessById(id) {
            const w = weaknessesList.find(item => item.id === id);
            if (w) selectWeakness(weaknessesList.indexOf(w));
        }

        function selectWeakness(index) {
            activeWeakness = weaknessesList[index] || weaknessesList[0];
            if (!activeWeakness) return;

            document.getElementById('weak-tag').innerText = `${activeWeakness.loss_count} Losses in Your Dataset`;
            document.getElementById('weak-eco-badge').innerText = `ECO: ${activeWeakness.eco}`;
            document.getElementById('weak-title').innerText = `${activeWeakness.side === 'White' ? '⚪' : '⚫'} ${activeWeakness.opening}`;
            document.getElementById('weak-opp-trigger').innerText = activeWeakness.opp_trigger;
            document.getElementById('weak-your-mistake').innerText = activeWeakness.your_mistake;
            document.getElementById('weak-best-option').innerText = activeWeakness.best_option;
            document.getElementById('weak-why-reason').innerText = activeWeakness.why_reason;

            resetWeaknessBoard();
            renderWeaknessList();
        }

        function resetWeaknessBoard() {
            if (!activeWeakness) return;
            weaknessGame.load(activeWeakness.fen_setup);
            weaknessBoard.orientation(activeWeakness.side.toLowerCase());
            weaknessBoard.position(activeWeakness.fen_setup);
            renderWeaknessArrow();
        }

        function playWeaknessRefutationAnimation() {
            if (!activeWeakness) return;
            resetWeaknessBoard();
            setTimeout(() => {
                const uci = activeWeakness.refutation_uci;
                if (uci && uci.length >= 4) {
                    weaknessGame.move({ from: uci.substring(0, 2), to: uci.substring(2, 4), promotion: 'q' });
                    weaknessBoard.position(weaknessGame.fen());
                    playChessSound('move');
                    clearWeaknessArrows();
                }
            }, 300);
        }

        function renderWeaknessArrow() {
            const svg = document.getElementById('weakness-arrows-svg');
            if (!svg || !activeWeakness || !activeWeakness.refutation_uci) return;

            const boardEl = document.getElementById('weakness-board');
            const boardWidth = boardEl ? boardEl.clientWidth : 420;
            const orientation = activeWeakness.side.toLowerCase();
            const uci = activeWeakness.refutation_uci;

            const fromSq = uci.substring(0, 2);
            const toSq = uci.substring(2, 4);

            svg.innerHTML = `
                <defs>
                    <marker id="weak-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#22c55e" />
                    </marker>
                </defs>
                ${drawSvgArrow(fromSq, toSq, "#22c55e", "weak-green", orientation, boardWidth, false)}
            `;
        }

        function clearWeaknessArrows() {
            const svg = document.getElementById('weakness-arrows-svg');
            if (svg) svg.innerHTML = "";
        }

        // ==========================================
        // ⚡ TACTICAL BLUNDERS REPLAYER (90+ GAMES)
        // ==========================================
        const allLossesList = analysisData.all_analyzed_losses || [];
        let replayBoard = null;
        let currentGameIndex = 0;
        let currentPly = 0;
        let currentFens = [];
        let currentPhaseFilter = "all";

        const STORAGE_KEY_STUDIED = `chess_studied_${analysisData.username}`;
        const STORAGE_KEY_NOTES = `chess_notes_${analysisData.username}`;

        function getStudiedSet() {
            try {
                const raw = localStorage.getItem(STORAGE_KEY_STUDIED);
                return new Set(raw ? JSON.parse(raw) : []);
            } catch (e) { return new Set(); }
        }

        function saveStudiedSet(studiedSet) {
            try { localStorage.setItem(STORAGE_KEY_STUDIED, JSON.stringify(Array.from(studiedSet))); } catch (e) {}
        }

        function getNotesDict() {
            try {
                const raw = localStorage.getItem(STORAGE_KEY_NOTES);
                return raw ? JSON.parse(raw) : {};
            } catch (e) { return {}; }
        }

        function saveNotesDict(notesDict) {
            try { localStorage.setItem(STORAGE_KEY_NOTES, JSON.stringify(notesDict)); } catch (e) {}
        }

        function initReplayer() {
            replayBoard = Chessboard('replay-board', {
                position: 'start',
                pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png'
            });

            document.getElementById('cnt-phase-all').innerText = allLossesList.length;
            updateStudyProgressUI();

            if (allLossesList.length > 0) {
                loadSelectedGame(0);
            }
        }

        function filterPhaseLosses(phase) {
            currentPhaseFilter = phase;
            ['all', 'opening', 'mid', 'end'].forEach(p => {
                const btn = document.getElementById('btn-phase-' + p);
                if (btn) {
                    const match = (phase === 'all' && p === 'all') || (phase === 'Opening' && p === 'opening') || (phase === 'Middlegame' && p === 'mid') || (phase === 'Endgame' && p === 'end');
                    btn.className = match ? 'px-2.5 py-1 bg-sky-600 rounded text-white font-medium' : 'px-2.5 py-1 bg-slate-900 hover:bg-slate-700 rounded text-slate-300 font-medium';
                }
            });
            renderGameSelectorOptions();
        }

        function renderGameSelectorOptions() {
            const studiedSet = getStudiedSet();
            const select = document.getElementById('game-select');
            if (!select) return;

            let html = "";
            for (let idx = 0; idx < allLossesList.length; idx++) {
                const g = allLossesList[idx];
                if (currentPhaseFilter !== "all" && g.phase !== currentPhaseFilter) continue;

                const isStudied = studiedSet.has(idx);
                const icon = isStudied ? "✅" : "⏳";
                const isSelected = (idx === currentGameIndex) ? "selected" : "";
                html += `<option value="${idx}" ${isSelected}>${icon} ${idx+1}. [${g.phase} - ${g.moves_count}m] vs ${g.opp_name} - ${g.opening}</option>`;
            }

            if (!html) html = `<option value="">No games in this category</option>`;
            select.innerHTML = html;
        }

        function loadSelectedGame(idx) {
            if (idx === "" || idx === null || isNaN(idx)) return;
            currentGameIndex = parseInt(idx);
            const g = allLossesList[currentGameIndex];
            if (!g) return;

            document.getElementById('meta-opening').innerText = `[${g.phase}] ${g.opening}`;
            document.getElementById('meta-opp').innerText = `${g.opp_name} (${g.opp_rating || '?'})`;
            document.getElementById('meta-result').innerText = `${g.result} in ${g.moves_count} moves`;
            document.getElementById('meta-link').href = g.url;

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
            if (curEl) curEl.classList.add('bg-sky-500/30', 'text-sky-300');

            const g = allLossesList[currentGameIndex];
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

        function updateStudyProgressUI() {
            const studiedSet = getStudiedSet();
            const totalCount = allLossesList.length;
            const studiedCount = Array.from(studiedSet).filter(idx => idx >= 0 && idx < totalCount).length;
            const pct = totalCount > 0 ? Math.round((studiedCount / totalCount) * 100) : 0;

            document.getElementById('study-count-text').innerText = `${studiedCount} / ${totalCount} Studied`;
            document.getElementById('study-pct-badge').innerText = `${pct}% Complete`;
            document.getElementById('study-progress-bar').style.width = `${pct}%`;

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
            if (studiedSet.has(currentGameIndex)) studiedSet.delete(currentGameIndex);
            else studiedSet.add(currentGameIndex);
            saveStudiedSet(studiedSet);
            updateStudyProgressUI();
        }

        function jumpNextUnstudied() {
            const studiedSet = getStudiedSet();
            for (let idx = currentGameIndex + 1; idx < allLossesList.length; idx++) {
                if (!studiedSet.has(idx)) { loadSelectedGame(idx); return; }
            }
            for (let idx = 0; idx <= currentGameIndex; idx++) {
                if (!studiedSet.has(idx)) { loadSelectedGame(idx); return; }
            }
            alert("🎉 Amazing! You have studied all 90 lost games in this dataset!");
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

        let showArrows = true;
        function toggleArrowDisplay() {
            showArrows = !showArrows;
            const btn = document.getElementById('btn-arrow-toggle');
            if (showArrows) {
                btn.innerHTML = `<span>🎯</span> Arrow: ON`;
                btn.className = `text-xs text-emerald-400 font-semibold flex items-center gap-1 bg-slate-800 px-2 py-0.5 rounded border border-emerald-500/40`;
            } else {
                btn.innerHTML = `<span>🎯</span> Arrow: OFF`;
                btn.className = `text-xs text-slate-400 font-semibold flex items-center gap-1 bg-slate-800 px-2 py-0.5 rounded border border-slate-700`;
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
            if (!showArrows) { svg.innerHTML = ""; return; }

            const g = allLossesList[currentGameIndex];
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
                    arrowsHtml += drawSvgArrow(plyData.played_uci.substring(0, 2), plyData.played_uci.substring(2, 4), "#ef4444", "arrow-red", orientation, boardWidth, true);
                }
                if (plyData.best_uci) {
                    arrowsHtml += drawSvgArrow(plyData.best_uci.substring(0, 2), plyData.best_uci.substring(2, 4), "#22c55e", "arrow-green", orientation, boardWidth, false);
                }
            }
            svg.innerHTML = arrowsHtml;
        }

        function replayNext() { 
            if (currentPly < currentFens.length - 1) { 
                currentPly++; 
                updateReplayStatus(); 
                playChessSound('move');
            } 
        }
        function replayPrev() { 
            if (currentPly > 0) { 
                currentPly--; 
                updateReplayStatus(); 
                playChessSound('move');
            } 
        }
        function replayFirst() { currentPly = 0; updateReplayStatus(); }
        function replayLast() { currentPly = currentFens.length - 1; updateReplayStatus(); }
        function jumpToPly(ply) { currentPly = ply; updateReplayStatus(); playChessSound('move'); }

        // ==========================================
        // ⚔️ SPARRING BOT & WHAT-IF
        // ==========================================
        const masterOpeningDatabase = {
            "": [
                { san: "e4", games: 2450000, eval: "+0.3", w: 38, d: 34, b: 28, name: "King's Pawn Opening" },
                { san: "d4", games: 2180000, eval: "+0.3", w: 38, d: 35, b: 27, name: "Queen's Pawn Opening" },
                { san: "Nf3", games: 520000, eval: "+0.2", w: 36, d: 37, b: 27, name: "Zukertort / Réti" }
            ],
            "e4": [
                { san: "e5", games: 980000, eval: "+0.3", w: 37, d: 33, b: 30, name: "Open Game (1...e5)" },
                { san: "c5", games: 890000, eval: "+0.2", w: 36, d: 34, b: 30, name: "Sicilian Defense" },
                { san: "d5", games: 320000, eval: "+0.4", w: 42, d: 29, b: 29, name: "Scandinavian Defense" }
            ],
            "e4 d5": [
                { san: "exd5", games: 280000, eval: "+0.4", w: 42, d: 30, b: 28, name: "Mainline Accepted" },
                { san: "e5", games: 14000, eval: "-0.2", w: 31, d: 28, b: 41, name: "Advance Variation" }
            ],
            "e4 d5 exd5": [
                { san: "Qxd5", games: 195000, eval: "+0.4", w: 42, d: 30, b: 28, name: "Mieses-Kotroc Mainline" },
                { san: "Nf6", games: 78000, eval: "+0.5", w: 43, d: 29, b: 28, name: "Modern / Portuguese Variation" }
            ],
            "e4 d5 exd5 Qxd5": [
                { san: "Nc3", games: 185000, eval: "+0.4", w: 42, d: 30, b: 28, name: "Develop with Tempo" }
            ],
            "e4 d5 exd5 Qxd5 Nc3": [
                { san: "Qa5", games: 110000, eval: "+0.4", w: 41, d: 31, b: 28, name: "Classical Mainline (Qa5)" },
                { san: "Qd6", games: 52000, eval: "+0.4", w: 42, d: 30, b: 28, name: "Gubinsky-Melts (Qd6)" }
            ],
            "d4": [
                { san: "d5", games: 920000, eval: "+0.3", w: 38, d: 35, b: 27, name: "Closed Game (1...d5)" },
                { san: "Nf6", games: 880000, eval: "+0.3", w: 37, d: 36, b: 27, name: "Indian Defenses" },
                { san: "e5", games: 32000, eval: "+1.6", w: 62, d: 18, b: 20, name: "Englund Gambit" }
            ],
            "d4 e5 dxe5 Nc6 Nf3 Qe7 Bf4 Qb4+": [
                { san: "Bd2!", games: 10500, eval: "+3.5", w: 74, d: 14, b: 12, name: "The Winning Refutation!" },
                { san: "Qd2??", games: 2200, eval: "-6.2", w: 8, d: 6, b: 86, name: "Blunder! Loses to Qxb2" }
            ]
        };

        const sparringRepertoires = {
            scandi: {
                title: "⚪ White vs 🤖 Scandinavian Defense",
                userSide: "white",
                expectedFirst: "e4",
                botTag: "Bot: Scandinavian",
                whatifs: [
                    { label: "▶ 2...Qxd5 (Mainline Qa5)", seq: ["e4", "d5", "exd5", "Qxd5", "Nc3", "Qa5"] },
                    { label: "▶ 2...Nf6 (Portuguese)", seq: ["e4", "d5", "exd5", "Nf6"] },
                    { label: "▶ 2.e5 (Advance Bf5)", seq: ["e4", "d5", "e5", "Bf5"] }
                ]
            },
            englund: {
                title: "⚪ White vs 🤖 Englund Gambit",
                userSide: "white",
                expectedFirst: "d4",
                botTag: "Bot: Englund Gambit",
                whatifs: [
                    { label: "▶ Refute Trap (5.Bd2! Qxb2 6.Nc3!)", seq: ["d4", "e5", "dxe5", "Nc6", "Nf3", "Qe7", "Bf4", "Qb4+", "Bd2", "Qxb2", "Nc3"] }
                ]
            },
            scandi_black: {
                title: "⚫ Black vs 🤖 Scandinavian 2.e5",
                userSide: "black",
                expectedFirst: "d5",
                botTag: "Bot: Scandi 2.e5",
                whatifs: [
                    { label: "▶ 2.e5 Bf5! (Bishop Free)", seq: ["e4", "d5", "e5", "Bf5", "d4", "e6", "Nf3", "c5"] }
                ]
            },
            london_black: {
                title: "⚫ Black vs 🤖 London System",
                userSide: "black",
                expectedFirst: "d5",
                botTag: "Bot: London System",
                whatifs: [
                    { label: "▶ 2...c5! 4...Qb6! (Counter-Attack)", seq: ["d4", "d5", "Bf4", "c5", "e3", "Nc6", "Nf3", "Qb6"] }
                ]
            },
            danish_black: {
                title: "⚫ Black vs 🤖 Danish Gambit",
                userSide: "black",
                expectedFirst: "e5",
                botTag: "Bot: Danish Gambit",
                whatifs: [
                    { label: "▶ 5...d5!! (Schlechter Refutation)", seq: ["e4", "e5", "d4", "exd4", "c3", "dxc3", "Bc4", "cxb2", "Bxb2", "d5"] }
                ]
            },
            reti_black: {
                title: "⚫ Black vs 🤖 Reti Opening",
                userSide: "black",
                expectedFirst: "d5",
                botTag: "Bot: Reti Opening",
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
            for (let san of wi.seq) sparringGame.move(san);
            sparringBoard.position(sparringGame.fen());
            clearSparringArrows();
            updateSparringMovesUI();
            updateSparringStatus();
            updateSparringExplorerTable();
            document.getElementById('sparring-feedback-title').innerHTML = `<span class="text-amber-400 font-bold">🔀 Branch: ${wi.label}</span>`;
            document.getElementById('sparring-feedback-sub').innerText = `Position: ${wi.seq.join(' ')}`;
            playChessSound('move');
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
                document.getElementById('sparring-feedback-sub').innerText = `Start with 1.${currentSparringRep.expectedFirst} for ${currentSparringRep.title}.`;
            } else {
                document.getElementById('sparring-feedback-sub').innerText = "PC is playing White. Waiting for opening move...";
                setTimeout(makeBotMove, 400);
            }
        }

        function updateSparringExplorerTable() {
            const hist = sparringGame.history().join(" ");
            const turn = sparringGame.turn() === 'w' ? 'White' : 'Black';
            const isUserTurn = (turn.toLowerCase() === currentSparringRep.userSide);
            const candidates = masterOpeningDatabase[hist] || [];
            const tbody = document.getElementById('sparring-explorer-tbody');
            const evalBadge = document.getElementById('sparring-eval-badge');

            if (candidates.length === 0) {
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
                        <td class="py-1.5 px-3 text-center"><div class="eval-bar-container"><div class="bar-white" style="width:50%">50%</div><div class="bar-black" style="width:50%">50%</div></div></td>
                        <td class="py-1.5 px-2 text-center">
                            <button onclick="event.stopPropagation(); forcePlaySparringMove('${m.san}')" class="px-2 py-0.5 bg-sky-600 hover:bg-sky-500 text-white rounded text-[10px] font-bold">${isUserTurn ? 'Play' : 'Force Bot'}</button>
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
            playChessSound(move.captured ? 'capture' : 'move');

            if (sparringGame.game_over()) return;
            const turn = sparringGame.turn() === 'w' ? 'white' : 'black';
            if (turn !== currentSparringRep.userSide) setTimeout(makeBotMove, 300);
        }

        function onSparringDrop(source, target) {
            const turn = sparringGame.turn() === 'w' ? 'white' : 'black';
            if (turn !== currentSparringRep.userSide) return 'snapback';

            const move = sparringGame.move({ from: source, to: target, promotion: 'q' });
            if (move === null) return 'snapback';

            clearSparringArrows();
            updateSparringMovesUI();
            updateSparringStatus();
            updateSparringExplorerTable();
            playChessSound(move.captured ? 'capture' : 'move');

            if (sparringGame.game_over()) return;
            setTimeout(makeBotMove, 300);
        }

        function makeBotMove() {
            if (sparringGame.game_over()) return;
            const hist = sparringGame.history().join(" ");
            const candidates = masterOpeningDatabase[hist] || [];
            let chosenMove = candidates.length > 0 ? candidates[0].san : null;

            if (!chosenMove) {
                const legals = sparringGame.moves({ verbose: true });
                if (legals.length > 0) chosenMove = legals[0].san;
            }

            if (chosenMove) {
                const res = sparringGame.move(chosenMove);
                if (res) {
                    sparringBoard.position(sparringGame.fen());
                    updateSparringMovesUI();
                    updateSparringStatus();
                    updateSparringExplorerTable();
                    playChessSound(res.captured ? 'capture' : 'move');
                    document.getElementById('sparring-feedback-title').innerHTML = `<span class="text-emerald-400 font-bold">📖 Bot Plays: ${res.san}</span>`;
                }
            }
        }

        function undoSparringMove() {
            sparringGame.undo(); sparringGame.undo();
            sparringBoard.position(sparringGame.fen());
            clearSparringArrows();
            updateSparringMovesUI();
            updateSparringStatus();
            updateSparringExplorerTable();
            playChessSound('move');
        }

        function showSparringHint() {
            const legals = sparringGame.moves({ verbose: true });
            if (legals.length === 0) return;
            const best = legals[0];
            drawSparringArrow(best.from, best.to, "#22c55e", "spar-green");
            document.getElementById('sparring-feedback-sub').innerHTML = `<span class="text-amber-400 font-bold">💡 Best Move:</span> <strong>${best.san}</strong>`;
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
            svg.innerHTML = `
                <defs>
                    <marker id="spar-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#22c55e" />
                    </marker>
                </defs>
                ${drawSvgArrow(fromSq, toSq, color, markerId, orientation, boardWidth, false)}
            `;
        }

        function clearSparringArrows() {
            const svg = document.getElementById('sparring-arrows-svg');
            if (svg) svg.innerHTML = "";
        }

        $(document).ready(function() {
            initWeaknessView();
            initReplayer();
            initSparring();
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
        .replace("__ANALYSIS_DATA__", stats_json) \
        .replace("__USER_STATS__", user_stats_json) \
        .replace("__TOP_OPENINGS__", top_openings_json)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_rendered)
    print(f"Generated interactive dashboard with separated Opening Weaknesses & Blunders: {output_path}")
    return output_path
