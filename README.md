# ♟️ Chess Diagnostic Copilot

An automated chess diagnostic tool and interactive analysis dashboard designed to help chess players break through rating plateaus by identifying early-game leaks, opening traps, and move 4–8 blunders from their [Chess.com](https://www.chess.com) history.

---

## 🚀 Key Features

* **Direct Chess.com Sync**: Automatically pulls all your games using the public Chess.com API (no password required).
* **Early Disaster Detection**: Flags all games lost in $\le 15$ moves (~18% of typical losses) where early mistakes decided the game.
* **Opening Leak Matrix**: Compares win/loss rates across all openings played as White and Black.
* **Interactive Disaster Replayer**: Replay your short lost games directly on a built-in chessboard with move-by-move notation.
* **Blunder Trainer**: Practice the exact refutations and winning responses for your most common trouble positions.
* **Repertoire Action Blueprint**: Clear, actionable opening plans to fix your worst-performing lines.

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/quakeanil/chess-analyzer.git
   cd chess-analyzer
   ```

2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage

### One-Click Launch (Windows)
Double-click `run.bat` or run:
```bash
python main.py
```

### Analyze Another Username
```bash
python main.py --username <chess_com_username>
```

### Force Refresh Cache
```bash
python main.py --refresh
```

---

## 📊 Summary of Findings for `0kanil`

* **Total Games:** 2,180
* **Peak Tactics Rating:** 1,736 (strong tactical foundation)
* **Main Rating Bottlenecks:**
  1. **White vs Englund Gambit (`1. d4 e5`)**: 65% loss rate due to falling for `4...Qb4+`. (Fixed by `5.Bd2! Qxb2 6.Nc3!`).
  2. **Black vs Scandinavian `2.e5`**: 64.5% loss rate when playing `2...d4?!`. (Fixed by `2...Bf5!` before `e6`).
  3. **Black vs London System (`1.d4 d5 2.Bf4`)**: 72.7% loss rate. (Fixed by `2...c5!` and `4...Qb6!`).
  4. **White Passive Queen's Pawn (`1.d4 d5 2.Nf3`)**: 70% loss rate. (Fixed by playing active `2.c4!` Queen's Gambit or `2.Bf4!` London).

---

## 🎓 Interactive Opening Mentor & Study Sandbox

Launch the live interactive mentor locally:

```bash
start_mentor.bat
# or
python mentor_server.py
```

Then open `http://localhost:5050/mentor` in your browser.

### Key Features:
* **Interactive Study Sandbox:**
  * **Scandinavian Defense (Black):** Pick from White's Top 10 Moves with win rates & Stockfish strength classifications.
  * **Center Game (White - 1.e4 e5 2.d4 exd4 3.Qxd4!):** Scandinavian in reverse with an extra tempo! View Black's Top 10 responses and practice the 4.Qe3 Paulsen Attack.
* **10 Master Lessons:** Guided grandmaster lines with live coaching hints and SVG arrows.
  * Lesson 9: *0kanil's Match Stats & Top 3 Leaks Fixer* (derived from 369 real Scandinavian games).
  * Lesson 10: *The Center Game (1.e4 e5 2.d4 exd4 3.Qxd4!)*.
* **⚡ 0kanil Blunder Quiz:** Real match blunder positions mined directly from Chess.com game history with streak tracking.
* **👑 Guess the Move with Grandmasters:** Play alongside Magnus Carlsen and Sergei Tiviakov.
* **Keyboard Shortcuts:**
  * `B`: 🤖 Bot plays the move for the active side
  * `H`: 💡 Show Stockfish best move recommendation
  * `T`: ⚠️ Null-move opponent threat detection
  * `Z`: ↩️ Take back move

