import requests
from database2 import get_elixir_username, update_user_rank, get_elixir_rank

API_URL = "https://api.points.elixir.xyz/api/scores"
CHUNK_SIZE = 3000
MAX_LIMIT = 250000
SEARCH_RANGE = 1000  

def fetch_scores(offset, first):
    params = {"offset": offset, "first": first}
    response = requests.get(API_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("ranks", [])
    
    print(f"\u274c Error: {response.status_code}, {response.text}")
    return []

def find_user_rank(username, start_offset=0):
    while start_offset < MAX_LIMIT:
        scores = fetch_scores(start_offset, CHUNK_SIZE)
        if not scores:
            break
        for i, user in enumerate(scores):
            if user.get("name") == username:
                return start_offset + i + 1
        start_offset += CHUNK_SIZE  
    return None  

def update_elixir_rank(user_id):
    username = get_elixir_username(user_id)

    if not username:
        return "❌ Elixir username not set. Please set it first."
    
    
    current_rank = get_elixir_rank(user_id)


    if current_rank and current_rank != "null":
        start_offset = max(0, current_rank - SEARCH_RANGE)
        new_rank = find_user_rank(username, start_offset)
        
        if new_rank:
            if new_rank != current_rank:
                update_user_rank(user_id, new_rank)
            return f"{new_rank}"
    
    new_rank = find_user_rank(username)
    if new_rank:
        update_user_rank(user_id, new_rank)
        return f"{new_rank}"
    
    return f"❌ {username} not found in the top {MAX_LIMIT}"
