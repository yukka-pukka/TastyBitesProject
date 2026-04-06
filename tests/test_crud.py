import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Favorite
import crud

# test database
TEST_DB_URL = "postgresql://postgres:postgres@localhost:5432/tastybites_test"

@pytest.fixture
def db():
    engine = create_engine(TEST_DB_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user(db):
    user = crud.create_user(db, "testuser", "testpassword")
    assert user.username == "testuser"
    assert user.hashed_password != "testpassword"  # should be hashed

def test_get_user(db):
    crud.create_user(db, "testuser", "testpassword")
    user = crud.get_user(db, "testuser")
    assert user is not None
    assert user.username == "testuser"

def test_get_nonexistent_user(db):
    user = crud.get_user(db, "nobody")
    assert user is None

def test_add_favorite(db):
    crud.create_user(db, "testuser", "testpassword")
    restaurant = {
        "name": "Cafe Selam",
        "category": "Ethiopian",
        "address": "2404 S. McClellan St, Seattle",
        "rating": 4.5,
        "minority_owned": "Black"
    }
    crud.add_favorite(db, "testuser", restaurant)
    favs = crud.get_favorites(db, "testuser")
    assert len(favs) == 1
    assert favs[0].restaurant_name == "Cafe Selam"

def test_is_favorite(db):
    crud.create_user(db, "testuser", "testpassword")
    restaurant = {
        "name": "Cafe Selam",
        "category": "Ethiopian",
        "address": "2404 S. McClellan St, Seattle",
        "rating": 4.5,
        "minority_owned": "Black"
    }
    crud.add_favorite(db, "testuser", restaurant)
    assert crud.is_favorite(db, "testuser", "Cafe Selam") == True
    assert crud.is_favorite(db, "testuser", "McDonald's") == False

def test_remove_favorite(db):
    crud.create_user(db, "testuser", "testpassword")
    restaurant = {
        "name": "Cafe Selam",
        "category": "Ethiopian",
        "address": "2404 S. McClellan St, Seattle",
        "rating": 4.5,
        "minority_owned": "Black"
    }
    crud.add_favorite(db, "testuser", restaurant)
    crud.remove_favorite(db, "testuser", "Cafe Selam")
    assert crud.is_favorite(db, "testuser", "Cafe Selam") == False

def test_get_favorites_empty(db):
    crud.create_user(db, "testuser", "testpassword")
    favs = crud.get_favorites(db, "testuser")
    assert favs == []