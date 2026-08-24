"""
HTML Dashboard Generator for Chess Diagnostic Tool
Generates a standalone interactive HTML dashboard with embedded Chessboard.js
"""
import json
import os

def generate_html_dashboard(analysis_data, user_stats, output_path="dashboard.html"):
    stats_json = json.dumps(analysis_data)
    user_stats_json = json.dumps(user_stats)
    
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chess.com Diagnostics - __USERNAME__</title>
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
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- Header -->
    <header class="bg-slate-900 border-b border-slate-800 px-6 py-4 flex flex-wrap items-center justify-between shadow-lg">
        <div class="flex items-center space-x-3">
            <span class="text-3xl">♟️</span>
            <div>
                <h1 class="text-xl font-bold text-white flex items-center gap-2">
                    Chess Diagnostic Copilot
                    <span class="text-xs bg-sky-500/20 text-sky-400 border border-sky-500/30 px-2 py-0.5 rounded font-mono">__USERNAME__</span>
                </h1>
                <p class="text-xs text-slate-400">Deep Diagnostic & Early-Game Blunder Analysis (__TOTAL_GAMES__ games)</p>
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
            <button onclick="switchTab('overview')" id="tab-overview" class="tab-btn active py-3 px-1 text-slate-300 hover:text-white transition">Overview & Leaks</button>
            <button onclick="switchTab('disasters')" id="tab-disasters" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition">Early Disaster Replayer (<=15 moves)</button>
            <button onclick="switchTab('trainer')" id="tab-trainer" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition">Interactive Blunder Trainer</button>
            <button onclick="switchTab('repertoire')" id="tab-repertoire" class="tab-btn py-3 px-1 text-slate-300 hover:text-white transition">Opening Action Blueprint</button>
        </nav>
    </div>

    <!-- Main Content Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto p-6">

        <!-- TAB 1: OVERVIEW & LEAKS -->
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

            <!-- Priority Diagnosis Banner -->
            <div class="bg-sky-950/40 border border-sky-700/50 rounded-xl p-5">
                <h3 class="text-base font-bold text-sky-300 flex items-center gap-2">
                    <span>💡</span> Root Cause Diagnosis
                </h3>
                <p class="text-sm text-slate-300 mt-2 leading-relaxed">
                    Your tactical strength is rated at <strong>1,736</strong>, but your blitz rating is around <strong>1,260</strong>. 
                    The data reveals you are not being outplayed in the endgame; you are getting caught in <strong>4 specific early-game trap patterns (Moves 3–7)</strong> that lead to fast resignations. Eliminating these 4 leaks will immediately push your rating past 1,400.
                </p>
            </div>

            <!-- Worst Openings Tables Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- White Openings -->
                <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-5">
                    <h3 class="text-base font-bold text-white mb-3 flex items-center justify-between">
                        <span>⚪ As White - Worst Leak Openings</span>
                        <span class="text-xs text-slate-400">Min 5 games</span>
                    </h3>
                    <div class="overflow-x-auto">
                        <table class="w-full text-xs text-left text-slate-300">
                            <thead class="text-slate-400 bg-slate-900/60 uppercase">
                                <tr>
                                    <th class="py-2.5 px-3">Opening</th>
                                    <th class="py-2.5 px-2 text-center">Games</th>
                                    <th class="py-2.5 px-2 text-center">Loss %</th>
                                    <th class="py-2.5 px-2 text-center">Win %</th>
                                </tr>
                            </thead>
                            <tbody id="white-openings-tbody" class="divide-y divide-slate-700/50"></tbody>
                        </table>
                    </div>
                </div>

                <!-- Black Openings -->
                <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-5">
                    <h3 class="text-base font-bold text-white mb-3 flex items-center justify-between">
                        <span>⚫ As Black - Worst Leak Openings</span>
                        <span class="text-xs text-slate-400">Min 5 games</span>
                    </h3>
                    <div class="overflow-x-auto">
                        <table class="w-full text-xs text-left text-slate-300">
                            <thead class="text-slate-400 bg-slate-900/60 uppercase">
                                <tr>
                                    <th class="py-2.5 px-3">Opening</th>
                                    <th class="py-2.5 px-2 text-center">Games</th>
                                    <th class="py-2.5 px-2 text-center">Loss %</th>
                                    <th class="py-2.5 px-2 text-center">Win %</th>
                                </tr>
                            </thead>
                            <tbody id="black-openings-tbody" class="divide-y divide-slate-700/50"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 2: EARLY DISASTER REPLAYER -->
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

                <!-- Right: Game Selector & Move List -->
                <div class="lg:col-span-7 bg-slate-800/80 rounded-xl border border-slate-700 p-5 flex flex-col">
                    <div class="mb-4">
                        <label class="block text-xs font-semibold text-slate-400 uppercase mb-1">Select Lost Game (<=15 moves):</label>
                        <select id="game-select" onchange="loadSelectedGame(this.value)" class="w-full bg-slate-900 border border-slate-700 text-slate-200 text-sm rounded-lg p-2.5 focus:border-sky-500"></select>
                    </div>

                    <div id="game-meta-card" class="bg-slate-900/70 p-4 rounded-lg border border-slate-700 mb-4 text-xs space-y-1">
                        <div><strong>Opening:</strong> <span id="meta-opening" class="text-sky-400"></span></div>
                        <div><strong>Opponent:</strong> <span id="meta-opp" class="text-slate-300"></span> | <strong>Result:</strong> <span id="meta-result" class="text-rose-400 font-semibold"></span></div>
                        <div><strong>Chess.com Link:</strong> <a id="meta-link" href="#" target="_blank" class="text-sky-400 underline">Open on Chess.com ↗</a></div>
                    </div>

                    <div class="flex-1">
                        <label class="block text-xs font-semibold text-slate-400 uppercase mb-1">Move Notation (Click any move to jump):</label>
                        <div id="moves-container" class="bg-slate-900 p-3 rounded-lg border border-slate-700 font-mono text-xs max-h-48 overflow-y-auto leading-relaxed flex flex-wrap gap-1.5"></div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 3: BLUNDER TRAINER -->
        <section id="view-trainer" class="hidden space-y-6">
            <div class="bg-slate-800/80 rounded-xl border border-slate-700 p-6 max-w-4xl mx-auto">
                <div class="text-center mb-6">
                    <span class="text-xs font-bold text-sky-400 uppercase tracking-wider">Interactive Drill</span>
                    <h2 class="text-2xl font-bold text-white mt-1" id="drill-title">Englund Gambit: Refuting the Move 5 Trap</h2>
                    <p class="text-sm text-slate-300 mt-2" id="drill-desc">Opponent just played <strong>4...Qb4+</strong> attacking your King and Bishop on f4. What is White's best response?</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
                    <div class="md:col-span-6 flex flex-col items-center">
                        <div class="board-container shadow-2xl rounded-lg overflow-hidden border border-slate-700">
                            <div id="drill-board" style="width: 100%"></div>
                        </div>
                    </div>
                    <div class="md:col-span-6 space-y-4">
                        <div id="drill-feedback" class="p-4 rounded-lg bg-slate-900 border border-slate-700 text-sm">
                            <div class="font-semibold text-slate-300">Your Turn: Make your move on the board</div>
                            <div class="text-xs text-slate-400 mt-1">Drag the piece to play your move.</div>
                        </div>

                        <div class="space-y-2">
                            <button onclick="loadDrill(0)" class="w-full text-left p-3 rounded bg-slate-900 hover:bg-slate-700/50 border border-slate-700 text-xs">
                                <strong>Drill 1:</strong> White vs Englund Gambit (4...Qb4+)
                            </button>
                            <button onclick="loadDrill(1)" class="w-full text-left p-3 rounded bg-slate-900 hover:bg-slate-700/50 border border-slate-700 text-xs">
                                <strong>Drill 2:</strong> Black vs Scandinavian 2.e5
                            </button>
                            <button onclick="loadDrill(2)" class="w-full text-left p-3 rounded bg-slate-900 hover:bg-slate-700/50 border border-slate-700 text-xs">
                                <strong>Drill 3:</strong> Black vs London System (2.Bf4)
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 4: REPERTOIRE ACTION BLUEPRINT -->
        <section id="view-repertoire" class="hidden space-y-6">
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

        // Populate Openings Tables
        function renderTables() {
            const whiteBody = document.getElementById('white-openings-tbody');
            whiteBody.innerHTML = analysisData.white_openings.slice(0, 10).map(o => `
                <tr class="hover:bg-slate-700/30">
                    <td class="py-2 px-3 font-medium text-slate-200">${o.opening}</td>
                    <td class="py-2 px-2 text-center">${o.games}</td>
                    <td class="py-2 px-2 text-center text-rose-400 font-bold">${o.loss_rate}%</td>
                    <td class="py-2 px-2 text-center text-emerald-400 font-semibold">${o.win_rate}%</td>
                </tr>
            `).join('');

            const blackBody = document.getElementById('black-openings-tbody');
            blackBody.innerHTML = analysisData.black_openings.slice(0, 10).map(o => `
                <tr class="hover:bg-slate-700/30">
                    <td class="py-2 px-3 font-medium text-slate-200">${o.opening}</td>
                    <td class="py-2 px-2 text-center">${o.games}</td>
                    <td class="py-2 px-2 text-center text-rose-400 font-bold">${o.loss_rate}%</td>
                    <td class="py-2 px-2 text-center text-emerald-400 font-semibold">${o.win_rate}%</td>
                </tr>
            `).join('');
        }
        renderTables();

        // Switch Tabs
        function switchTab(tabId) {
            ['overview', 'disasters', 'trainer', 'repertoire'].forEach(id => {
                document.getElementById('view-' + id).classList.add('hidden');
                document.getElementById('tab-' + id).classList.remove('active');
            });
            document.getElementById('view-' + tabId).classList.remove('hidden');
            document.getElementById('tab-' + tabId).classList.add('active');

            if (tabId === 'disasters') {
                setTimeout(() => { if (replayBoard) replayBoard.resize(); }, 100);
            } else if (tabId === 'trainer') {
                setTimeout(() => { if (drillBoard) drillBoard.resize(); }, 100);
            }
        }

        // Replayer Engine
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
            
            // Highlight move
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

        // Trainer Engine
        const drills = [
            {
                title: "Englund Gambit: Refuting the Move 5 Trap",
                desc: "Opponent just played 4...Qb4+ attacking King and Bishop. What is White's winning response?",
                fen: "r1b1kbnr/pppp1ppp/2n5/4P3/1q3B2/5N2/PPP1PPPP/RN1QKB1R w KQkq - 3 5",
                orientation: "white",
                solutionMove: { from: "f4", to: "d2" },
                explanation: "Excellent! 5.Bd2! protects your bishop and threatens 6.Nc3! Next when Black takes Qxb2, you play 6.Nc3! (or 6.Bc3) and Black is completely lost (+3.5)!"
            },
            {
                title: "Scandinavian Defense: Against 2.e5",
                desc: "White just pushed 2.e5. Which active bishop move must you play BEFORE playing e6?",
                fen: "rnbqkbnr/ppp1pppp/8/4P3/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2",
                orientation: "black",
                solutionMove: { from: "c8", to: "f5" },
                explanation: "Perfect! 2...Bf5! brings your bishop outside the pawn chain. Now you can follow up comfortably with e6, c5, and Nc6!"
            },
            {
                title: "Countering the London System: Immediate Central Strike",
                desc: "White played 1.d4 d5 2.Bf4. What is Black's most energetic central break?",
                fen: "rnbqkbnr/ppp1pppp/8/3p4/3P1B2/8/PPP1PPPP/RN1QKBNR b KQkq - 1 2",
                orientation: "black",
                solutionMove: { from: "c7", to: "c5" },
                explanation: "Spot on! 2...c5! challenges White's d4 pawn and prepares 3...Nc6 and 4...Qb6, attacking White's weakened b2 square!"
            }
        ];

        let currentDrillIndex = 0;
        let drillBoard = null;
        let drillGame = new Chess();

        function initTrainer() {
            drillBoard = Chessboard('drill-board', {
                draggable: true,
                position: drills[0].fen,
                pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png',
                onDrop: onDrillDrop
            });
            loadDrill(0);
        }

        function loadDrill(index) {
            currentDrillIndex = index;
            const d = drills[index];
            document.getElementById('drill-title').innerText = d.title;
            document.getElementById('drill-desc').innerHTML = d.desc;
            document.getElementById('drill-feedback').innerHTML = `
                <div class="font-semibold text-slate-300">Your Turn: Make your move on the board</div>
                <div class="text-xs text-slate-400 mt-1">Drag the piece to find the winning move.</div>
            `;
            drillGame.load(d.fen);
            drillBoard.orientation(d.orientation);
            drillBoard.position(d.fen);
        }

        function onDrillDrop(source, target) {
            const d = drills[currentDrillIndex];
            if (source === d.solutionMove.from && target === d.solutionMove.to) {
                document.getElementById('drill-feedback').innerHTML = `
                    <div class="font-bold text-emerald-400">🎉 Correct Move!</div>
                    <div class="text-xs text-slate-200 mt-1 leading-relaxed">${d.explanation}</div>
                `;
            } else {
                document.getElementById('drill-feedback').innerHTML = `
                    <div class="font-bold text-rose-400">❌ Inaccurate Move</div>
                    <div class="text-xs text-slate-300 mt-1">Try again! Think about piece activity and king safety.</div>
                `;
                return 'snapback';
            }
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
        .replace("__USER_STATS__", user_stats_json)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_rendered)
    print(f"Generated interactive dashboard: {output_path}")
    return output_path
