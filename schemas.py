from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True

class RestaurantCreate(BaseModel):
    name: str
    category: str
    lat: float
    lon: float
    minority_owned: str | None = None

class RestaurantOut(BaseModel):
    id: int
    name: str
    category: str
    lat: float
    lon: float
    rating: float
    distance_km: float = None
    score: float = None
    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    rating: float
    user_id: int
    restaurant_id: int