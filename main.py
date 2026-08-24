"""
Main entry point for Chess Diagnostic Copilot
"""
import os
import sys
import argparse
import webbrowser

# Reconfigure stdout for utf-8 if possible
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.fetcher import fetch_all_games, fetch_user_stats
from src.analyzer import analyze_player_games
from src.dashboard_builder import generate_html_dashboard

def run_diagnostic(username="0kanil", force_refresh=False, open_browser=True):
    print("=" * 60)
    print(f"CHESS DIAGNOSTIC COPILOT - ANALYZING: {username}")
    print("=" * 60)
    
    # 1. Fetch user stats
    print("\n[1/4] Fetching player stats from Chess.com...")
    stats = fetch_user_stats(username)
    if stats:
        blitz = stats.get("chess_blitz", {}).get("last", {}).get("rating", "N/A")
        bullet = stats.get("chess_bullet", {}).get("last", {}).get("rating", "N/A")
        rapid = stats.get("chess_rapid", {}).get("last", {}).get("rating", "N/A")
        tactics = stats.get("tactics", {}).get("highest", {}).get("rating", "N/A")
        print(f"      Ratings: Blitz: {blitz} | Bullet: {bullet} | Rapid: {rapid} | Tactics Peak: {tactics}")

    # 2. Fetch games
    print("\n[2/4] Syncing game archives...")
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    games = fetch_all_games(username, data_dir=data_dir, force_refresh=force_refresh)
    print(f"      Total games in dataset: {len(games)}")

    if not games:
        print("[!] No games found to analyze. Please check username or internet connection.")
        return

    # 3. Analyze games
    print("\n[3/4] Running opening tree & early disaster analysis...")
    analysis_results = analyze_player_games(username, games)
    
    print(f"      Analyzed: {analysis_results['total_games']} games")
    print(f"      Wins: {analysis_results['total_wins']} | Losses: {analysis_results['total_losses']} | Draws: {analysis_results['total_draws']}")
    print(f"      Early Disasters (<= 15 moves): {analysis_results['early_disasters_count']} games")

    # 4. Generate Dashboard
    print("\n[4/4] Generating Interactive HTML Dashboard...")
    dashboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard.html")
    generate_html_dashboard(analysis_results, stats, output_path=dashboard_path)
    
    print("\n" + "=" * 60)
    print("[+] ANALYSIS COMPLETE!")
    print(f"[+] Dashboard generated at: {dashboard_path}")
    print("=" * 60)

    if open_browser:
        print("\nOpening dashboard in your web browser...")
        webbrowser.open(f"file:///{os.path.abspath(dashboard_path)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Chess.com games and diagnose early mistakes.")
    parser.add_argument("--username", "-u", default="0kanil", help="Chess.com username (default: 0kanil)")
    parser.add_argument("--refresh", "-r", action="store_true", help="Force refresh all archives from Chess.com")
    parser.add_argument("--no-open", action="store_true", help="Do not automatically open browser")
    
    args = parser.parse_args()
    run_diagnostic(username=args.username, force_refresh=args.refresh, open_browser=not args.no_open)
