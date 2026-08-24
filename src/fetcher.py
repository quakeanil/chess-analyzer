"""
Chess.com Game Fetcher & Cache Manager
"""
import os
import json
import urllib.request
import urllib.error

HEADERS = {
    "User-Agent": "ChessDiagnosticTool/1.0 (contact: chess-diagnostic@project.local)"
}

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code} for URL: {url}")
        return None
    except Exception as e:
        print(f"Network error: {e}")
        return None

def fetch_user_profile(username):
    url = f"https://api.chess.com/pub/player/{username.lower()}"
    return fetch_json(url)

def fetch_user_stats(username):
    url = f"https://api.chess.com/pub/player/{username.lower()}/stats"
    return fetch_json(url)

def fetch_all_games(username, data_dir="data", force_refresh=False):
    username = username.lower()
    cache_file = os.path.join(data_dir, f"{username}_games_cache.json")
    
    cached_games = []
    cached_archives = set()
    
    if os.path.exists(cache_file) and not force_refresh:
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
                cached_games = cache_data.get("games", [])
                cached_archives = set(cache_data.get("archives", []))
                print(f"Loaded {len(cached_games)} cached games from {cache_file}")
        except Exception as e:
            print(f"Could not read cache: {e}")

    print(f"Checking Chess.com archives for {username}...")
    archives_data = fetch_json(f"https://api.chess.com/pub/player/{username}/games/archives")
    if not archives_data:
        print("Failed to fetch archives.")
        return cached_games
    
    archive_urls = archives_data.get("archives", [])
    print(f"Found {len(archive_urls)} monthly archives on Chess.com.")
    
    new_games = []
    # Always re-check the latest month because it may have new games
    latest_archive = archive_urls[-1] if archive_urls else None
    
    for url in archive_urls:
        if not force_refresh and url in cached_archives and url != latest_archive:
            continue
            
        print(f"Fetching: {url} ...")
        month_data = fetch_json(url)
        if month_data and "games" in month_data:
            month_games = month_data["games"]
            if url == latest_archive and cached_games:
                # Deduplicate against existing games by URL
                existing_urls = {g.get("url") for g in cached_games}
                for g in month_games:
                    if g.get("url") not in existing_urls:
                        new_games.append(g)
            else:
                new_games.extend(month_games)
            cached_archives.add(url)
            
    all_games = cached_games + new_games
    print(f"Total games ready for analysis: {len(all_games)} (New: {len(new_games)})")
    
    # Save cache
    os.makedirs(data_dir, exist_ok=True)
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump({
            "username": username,
            "archives": list(cached_archives),
            "games": all_games
        }, f)
        
    return all_games
