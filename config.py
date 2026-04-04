import secrets

# DATABASE_URL = ""

# Yelp API
YELP_API_KEY = ''

# Auth / JWT
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"  
ACCESS_TOKEN_EXPIRE_MINUTES = 60  

GOOGLE_MAPS_API_KEY = ""
