from sqlalchemy.orm import Session
import models
from auth import hash_password
from models import Favorite


def create_user(db: Session, username: str, password: str):
    hashed = hash_password(password)
    user = models.User(username=username, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_restaurant(db: Session, data):
    restaurant = models.Restaurant(**data.dict())
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant

def get_restaurants(db: Session):
    return db.query(models.Restaurant).all()
from models import Favorite

def get_favorites(db: Session, username: str):
    return db.query(Favorite).filter(Favorite.username == username).all()

def add_favorite(db: Session, username: str, restaurant: dict):
    fav = Favorite(
        username=username,
        restaurant_name=restaurant["name"],
        category=restaurant.get("category"),
        address=restaurant.get("address"),
        rating=restaurant.get("rating"),
        minority_owned=restaurant.get("minority_owned")
    )
    db.add(fav)
    db.commit()

def remove_favorite(db: Session, username: str, restaurant_name: str):
    db.query(Favorite).filter(
        Favorite.username == username,
        Favorite.restaurant_name == restaurant_name
    ).delete()
    db.commit()

def is_favorite(db: Session, username: str, restaurant_name: str) -> bool:
    return db.query(Favorite).filter(
        Favorite.username == username,
        Favorite.restaurant_name == restaurant_name
    ).first() is not None
