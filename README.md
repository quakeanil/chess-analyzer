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

* **Total Games:** 2,073
* **Peak Tactics Rating:** 1,736 (strong tactical foundation)
* **Main Rating Bottlenecks:**
  1. **White vs Englund Gambit (`1. d4 e5`)**: 65% loss rate due to falling for `4...Qb4+`. (Fixed by `5.Bd2! Qxb2 6.Nc3!`).
  2. **Black vs Scandinavian `2.e5`**: 65.6% loss rate when playing passive French-like pawn structures. (Fixed by `2...Bf5!` before `e6`).
  3. **Black vs London System (`1.d4 d5 2.Bf4`)**: 72.7% loss rate. (Fixed by `2...c5!` and `4...Qb6!`).
  4. **White Passive Queen's Pawn (`1.d4 d5 2.Nf3`)**: 70% loss rate. (Fixed by playing active `2.c4!` Queen's Gambit or `2.Bf4!` London).
