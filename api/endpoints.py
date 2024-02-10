from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Dict
from models import User
from auth.auths import send_email


app = FastAPI()


templates = Jinja2Templates(directory="templates")


users_db: Dict[str, Dict[str, str]] = {}


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login")
def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login_user(request: Request):
    return {"message": "Logowanie udane"}


@app.get("/register")
def read_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
def register_user(request: Request):
    return {"message": "Rejestracja udana"}


@app.get("/contacts")
def read_contacts(request: Request):
    return templates.TemplateResponse("contacts.html", {"request": request})


@app.get("/welcome")
def welcome(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@app.post("/register")
def register_user(request: Request, user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Użytkownik już istnieje")

    verification_token = "some_random_token"
    send_email(user.email, verification_token)

    users_db[user.username] = user.dict()

    return RedirectResponse(url="/welcome")


@app.get("/verify/{username}/{verification_token}")
def verify_email(username: str, verification_token: str):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="Użytkownik nie istnieje")

    expected_token = "some_random_token"
    if verification_token != expected_token:
        raise HTTPException(status_code=400, detail="Nieprawidłowy token weryfikacyjny")

    users_db[username]["verified"] = True

    return RedirectResponse(url="/login")