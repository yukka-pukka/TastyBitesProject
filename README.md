# 🍽️ TastyBites

**TastyBites** is a restaurant discovery app that helps users find and support minority-owned restaurants in Seattle. Built with FastAPI, PostgreSQL, and integrated with the Yelp and Google Maps APIs.

---

## 🌍 The Problem It Solves

Mainstream restaurant discovery platforms like Yelp and Google Maps rank results by popularity, ads, and review count but not by ownership. This makes it difficult for conscious consumers to find and support minority-owned businesses, and harder for those businesses to compete for visibility against larger, well-funded establishments.

TastyBites fixes this by putting minority-owned restaurants front and center, letting users filter by ownership category and find nearby spots on an interactive map.

---

## 👥 Intended Users

- **Conscious consumers** who want to spend their dining dollars intentionally
- **Seattle locals and tourists** looking to explore diverse, community-rooted restaurants
- **Members of minority communities** who prefer to support businesses that reflect their background or identity
- **LGBTQ+ community members** looking for queer-owned and queer-friendly dining spaces
- **Social justice advocates** who use spending as a form of activism
- **Food lovers** who want to discover authentic cuisine from cultures like Ethiopian, Salvadoran, Colombian, Cuban, and more

---

## ✨ Features

- 🔍 Search for minority-owned restaurants near you using the Yelp API
- 🗂️ Filter by ownership category: Black-owned, Latinx-owned, Asian-owned, LGBTQ+-owned
- 🗺️ View results on an interactive Google Map with clickable pins
- 📍 Click a restaurant name in the list to pan the map to its pin
- ❤️ Save favorite restaurants (requires login)
- 📋 View your saved favorites on a dedicated page
- 👤 User registration and login with secure password hashing

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI |
| Database | PostgreSQL + SQLAlchemy |
| Frontend | Jinja2 HTML Templates + Vanilla JavaScript |
| Auth | Cookie-based sessions + bcrypt password hashing |
| Restaurant Data | Yelp Fusion API |
| Maps | Google Maps JavaScript API |
| Performance | Parallel API calls (ThreadPoolExecutor) + 1-hour in-memory caching |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- Yelp Fusion API key
- Google Maps API key

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/tastybites.git
cd tastybites
```

2. **Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create a `config.py` file** (do not commit this):
```python
YELP_API_KEY = "your_yelp_api_key"
GOOGLE_MAPS_API_KEY = "your_google_maps_api_key"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "tastybites"
```

5. **Create the PostgreSQL database:**
```bash
psql -U postgres
CREATE DATABASE tastybites;
\q
```

6. **Run the app:**
```bash
uvicorn main:app --reload
```

7. **Visit** `http://localhost:8000`

---

## 📁 Project Structure

```
tastybites/
├── main.py              # FastAPI routes
├── models.py            # SQLAlchemy models (User, Restaurant, Favorite)
├── crud.py              # Database operations
├── auth.py              # Password hashing and verification
├── utils.py             # Yelp API integration, scoring, caching
├── schemas.py           # Pydantic schemas
├── database.py          # Database connection
├── config.py            # API keys and DB credentials (not committed)
├── data/
│   └── minority_owned_seattle.json   # Curated minority-owned restaurant list
├── templates/
│   ├── index.html
│   ├── search_results.html
│   ├── favorites.html
│   ├── login.html
│   └── register.html
└── static/
    └── style.css
```

---

## 🔒 Security Notes

- `config.py` is excluded from version control via `.gitignore`
- Passwords are hashed using bcrypt before storage
- Sessions are managed via HTTP-only cookies

---

## 📊 How Restaurants Are Ranked

Each restaurant is assigned a score based on:

```
score = (rating × 0.7) + (1 / (1 + distance_mi)) × 0.3
```

This weights rating more heavily while still rewarding proximity.

---

## 🗺️ Data Sources

- **Yelp Fusion API** — live restaurant data, ratings, and distances
- **`minority_owned_seattle.json`** — a curated, community-sourced list of minority-owned restaurants in Seattle, organized by ownership category

---

## 🧪 Testing

Tests are located in the `tests/` folder.

### Setup

Create a separate test database:
```bash
psql -U postgres
CREATE DATABASE tastybites_test;
\q
```

Install pytest:
```bash
pip install pytest
```

### Running Tests

```bash
pytest tests/ -v
```

### Test Coverage

| File | What It Tests |
|------|--------------|
| `tests/test_auth.py` | Password hashing, verification, uniqueness of hashes |
| `tests/test_utils.py` | Name normalization, scoring algorithm, minority ownership lookup |
| `tests/test_crud.py` | User creation, favorites add/remove/check, database operations |

### Manual JavaScript Tests

Frontend tests are run manually in the browser console. A `runTests()` function in `search_results.html` verifies that restaurant data loads correctly, required functions exist, and the map state is initialized properly.

# Extract JS blocks and execute them with Node.js
sed -n '/```js/,/```/p' test_js_manual.md | sed 's/```js//g;s/```//g' | node


---

## 🤝 Contributing

Know a minority-owned restaurant in Seattle that should be listed? Open a pull request to add it to `data/minority_owned_seattle.json` in the following format:

```json
{"name": "Restaurant Name", "minority_owned": "Black | Latinx | Asian | LGBTQ+"}
```

---

## 📄 License

MIT License

