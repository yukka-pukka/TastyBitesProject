import json
from math import radians, sin, cos, sqrt, asin
from pathlib import Path
import requests
from config import YELP_API_KEY

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

MINORITY_LIST = [
    {"name": "Meskel", "minority_owned": "Black"},
    {"name": "Fat's Chicken and Waffles", "minority_owned": "Black"},
    {"name": "Habesha Cafe", "minority_owned": "Black"},
    {"name": "Island Soul", "minority_owned": "Black"},
    {"name": "Simply Soulful", "minority_owned": "Black"},
    {"name": "Cafe Selam", "minority_owned": "Black"},
    {"name": "Taste of the Caribbean", "minority_owned": "Black"},
    {"name": "The Comfort Zone", "minority_owned": "Black"},
    {"name": "Mama Sambusa Kitchen", "minority_owned": "Black"},
    {"name": "Osteria la Spiga", "minority_owned": "Black"},
    {"name": "Cafe Campagne", "minority_owned": "Black"},
    {"name": "Boon Boona Coffee", "minority_owned": "Black"},
    {"name": "Lenox", "minority_owned": "Black"},
    {"name": "Métier Brewing Company", "minority_owned": "Black"},
    {"name": "Pizza by Ruffin", "minority_owned": "Black"},
    {"name": "Asadero Prime", "minority_owned": "Latinx"},
    {"name": "Westman’s Bagel & Coffee", "minority_owned": "Latinx"},
    {"name": "Askatu Bakery", "minority_owned": "Latinx"},
    {"name": "Nue", "minority_owned": "Asian"}
]

def get_nearby_ranked(lat, lon, radius_m=5000, minority_owned=None):
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}

    search_list = MINORITY_LIST
    if minority_owned:
        search_list = [e for e in MINORITY_LIST if e["minority_owned"].lower() == minority_owned.lower()]

    filtered = []
    for entry in search_list:
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
                if normalize(b["name"]) == normalize(entry["name"]):
                    filtered.append({
                        "name": b["name"],
                        "address": ", ".join(b["location"]["display_address"]),
                        "minority_owned": entry["minority_owned"],
                        "category": b["categories"][0]["title"] if b.get("categories") else "N/A",
                        "rating": b.get("rating", 0),
                        "distance_km": round(b.get("distance", 0) / 1000, 2),
                        "score": round(compute_score(
                            b.get("distance", 0) / 1000,
                            b.get("rating", 0)
                        ), 4)
                    })
        except Exception as e:
            print(f"ERROR fetching {entry['name']}:", e)

    print("DEBUG: filtered results", filtered)
    return filtered