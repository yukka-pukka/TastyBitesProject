import json
from math import radians, sin, cos, sqrt, asin
from pathlib import Path
import requests
from config import YELP_API_KEY
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

_cache = {}
CACHE_TTL = 3600  # 1 hour

# Paths 
DATA_DIR = Path(__file__).parent / "data"

# Distance Calculation 
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two lat/lon points in kilometers.
    """
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    return 2 * 6371 * asin(sqrt(a))


#  Ranking 
def compute_score(distance_km, rating):
    """
    Combine rating and distance into a ranking score.
    """
    return (rating * 0.7) + (1 / (1 + distance_km)) * 0.3


# Name Normalization
def normalize(name: str):
    return name.lower().replace("&", "and").strip()


# Load Minority-Owned Dataset
try:
    with open(DATA_DIR / "minority_owned_seattle.json") as f:
        data = json.load(f)
except FileNotFoundError:
    print("⚠️ WARNING: minority_owned_seattle.json not found in /data")
    data = []

# Convert to set for fast lookup
MINORITY_SET = {normalize(r["name"]) for r in data}


# Check Function
def is_minority_owned(restaurant_name: str) -> bool:
    return normalize(restaurant_name) in MINORITY_SET


#  Yelp API Integration 
YELP_URL = "https://api.yelp.com/v3/businesses/search"

def fetch_yelp_restaurants(lat, lon, term="restaurant", limit=20):
    """
    Fetch restaurants from Yelp API.
    """
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    params = {"latitude": lat, "longitude": lon, "term": term, "limit": limit}

    response = requests.get(YELP_URL, headers=headers, params=params)
    data = response.json()

    restaurants = []

    for b in data.get("businesses", []):
        restaurants.append({
            "name": b["name"],
            "lat": b["coordinates"]["latitude"],
            "lon": b["coordinates"]["longitude"],
            "rating": b.get("rating", 0),
            "category": b["categories"][0]["title"] if b.get("categories") else "N/A"
        })

    return restaurants

DATA_DIR = Path(__file__).parent / "data"

try:
    with open(DATA_DIR / "minority_owned_seattle.json") as f:
        MINORITY_LIST = json.load(f)
except FileNotFoundError:
    print("⚠️ WARNING: minority_owned_seattle.json not found")
    MINORITY_LIST = []

def fetch_one(entry, lat, lon, radius_m, headers):
    params = {
        "term": entry["name"],
        "latitude": lat,
        "longitude": lon,
        "radius": int(radius_m),
        "limit": 1
    }
    try:
        response = requests.get(YELP_URL, headers=headers, params=params)
        response.raise_for_status()
        businesses = response.json().get("businesses", [])
        if businesses:
            b = businesses[0]
            yelp_name = normalize(b["name"])
            entry_name = normalize(entry["name"])
            if yelp_name in entry_name or entry_name in yelp_name:
                return {
                    "name": b["name"],
                    "address": ", ".join(b["location"]["display_address"]),
                    "minority_owned": entry["minority_owned"],
                    "category": b["categories"][0]["title"] if b.get("categories") else "N/A",
                    "rating": b.get("rating", 0),
                    "distance_mi": round(b.get("distance", 0) / 1609, 2),
                    "score": round(compute_score(
                        b.get("distance", 0) / 1609,
                        b.get("rating", 0)
                    ), 4)
                }
    except Exception as e:
        print(f"ERROR fetching {entry['name']}:", e)
    return None


def get_nearby_ranked(lat, lon, radius_m=3219, minority_owned=None):
     # Check cache first
    cache_key = f"{lat}_{lon}_{radius_m}_{minority_owned}"
    if cache_key in _cache:
        timestamp, results = _cache[cache_key]
        if time.time() - timestamp < CACHE_TTL:
            print("DEBUG: returning cached results")
            return results

    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}

    search_list = MINORITY_LIST
    if minority_owned:
        search_list = [e for e in MINORITY_LIST if e["minority_owned"].lower() == minority_owned.lower()]

    filtered = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(fetch_one, entry, lat, lon, radius_m, headers): entry
            for entry in search_list
        }
        for future in as_completed(futures):
            result = future.result()
            if result:
                filtered.append(result)
        
    # Sort by score best first
    filtered.sort(key=lambda x: x["score"], reverse=True)

    # Store in cache
    _cache[cache_key] = (time.time(), filtered)

    print("debug: filtered results", filtered)
    return filtered