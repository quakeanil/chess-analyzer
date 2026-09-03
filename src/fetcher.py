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
    
    recent_archives = set(archive_urls[-2:]) if len(archive_urls) >= 2 else set(archive_urls)
    existing_games_map = {g.get("url"): g for g in cached_games if g.get("url")}
    new_games_count = 0
    
    for url in archive_urls:
        if not force_refresh and url in cached_archives and url not in recent_archives:
            continue
            
        print(f"Fetching: {url} ...")
        month_data = fetch_json(url)
        if month_data and "games" in month_data:
            for g in month_data["games"]:
                g_url = g.get("url")
                if g_url:
                    if g_url not in existing_games_map:
                        new_games_count += 1
                    existing_games_map[g_url] = g
            cached_archives.add(url)
            
    all_games = list(existing_games_map.values())
    print(f"Total games ready for analysis: {len(all_games)} (New: {new_games_count})")
    
    # Save cache
    os.makedirs(data_dir, exist_ok=True)
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump({
            "username": username,
            "archives": list(cached_archives),
            "games": all_games
        }, f)
        
    return all_games
