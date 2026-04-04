import secrets

# DATABASE_URL = "postgresql://tasty_user:password123@localhost:5432/tastybites"

# Yelp API
YELP_API_KEY = 'unksOTGmrK1Je7maJwHNmXehQnchaSCCZwKyn-lx_u5dkj_DVfKayIqL6vyWxCo7PD4oJZoJOyVfFHoFo9gPGm1axz9j2EuNyBZtfx338Q4eUHWsWHW6bjHyzgjQaXYx'

# Auth / JWT
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"  # standard JWT algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # optional, if using JWT


