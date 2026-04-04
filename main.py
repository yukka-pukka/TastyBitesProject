import os
from fastapi import FastAPI, Request, Form, Response, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import crud, auth, models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="TastyBites API")

current_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")


@app.get("/")
def index(request: Request):
    username = request.cookies.get("username")
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "username": username}
    )


@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(request=request,name="register.html", context={"request": request}
)

@app.post("/register")
def register_user(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if crud.get_user(db, username):
        return templates.TemplateResponse(request=request, name="register.html",context={"request": request, "error": "Username exists!"}
)
    crud.create_user(db, username, password)
    res = RedirectResponse("/", status_code=303)
    res.set_cookie("username", username, httponly=True)
    return res

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(request=request,name="login.html", context={"request": request}
)

@app.post("/login")
def login_user(response: Response, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = crud.get_user(db, username)
    if not user or not auth.verify_password(password, user.hashed_password):
        return {"error": "Invalid credentials"}
    res = RedirectResponse("/", status_code=303)
    res.set_cookie("username", username, httponly=True)
    return res

@app.get("/logout")
def logout():
    res = RedirectResponse("/", status_code=303)
    res.delete_cookie("username")
    return res

@app.get("/search")
def search_results(request: Request, lat: float = 47.6062, lon: float = -122.3321, minority_owned: str = None):
    from utils import get_nearby_ranked  
    print("🔥 SEARCH ENDPOINT HIT")
    results = get_nearby_ranked(lat, lon, radius_m=5000, minority_owned=minority_owned)
    return templates.TemplateResponse(request=request,name="search_results.html", context={"request": request, "restaurants": results, "minority_owned": minority_owned}
)
