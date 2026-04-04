from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    rating = Column(Float, default=0)
    minority_owned = Column(String) 

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    rating = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    user = relationship("User")
    restaurant = relationship("Restaurant")