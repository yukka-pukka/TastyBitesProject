from sqlalchemy.orm import Session
import models
from auth import hash_password


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
