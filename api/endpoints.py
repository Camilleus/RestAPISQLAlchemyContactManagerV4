from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Dict
from models import User
from auth.auths import send_email


app = FastAPI()


templates = Jinja2Templates(directory="templates")

# Database to store user information
users_db: Dict[str, Dict[str, str]] = {}


@app.get("/")
def read_root(request: Request):
    """
    Read the root endpoint.

    Args:
        request (Request): The request object.

    Returns:
        TemplateResponse: Response with the index.html template.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    """
    Read the login endpoint.

    Args:
        request (Request): The request object.

    Returns:
        TemplateResponse: Response with the login.html template.
    """
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login_user(request: Request):
    """
    Login a user.

    Args:
        request (Request): The request object.

    Returns:
        dict: Message confirming successful login.
    """
    return {"message": "Logowanie udane"}


@app.get("/register")
def read_register(request: Request):
    """
    Read the register endpoint.

    Args:
        request (Request): The request object.

    Returns:
        TemplateResponse: Response with the register.html template.
    """
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
def register_user(request: Request, user: User):
    """
    Register a new user.

    Args:
        request (Request): The request object.
        user (User): The user information to register.

    Returns:
        RedirectResponse: Redirects to the welcome page.
    """
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Użytkownik już istnieje")

    verification_token = "some_random_token"
    send_email(user.email, verification_token)

    users_db[user.username] = user.dict()

    return RedirectResponse(url="/welcome")


@app.get("/contacts")
def read_contacts(request: Request):
    """
    Read the contacts endpoint.

    Args:
        request (Request): The request object.

    Returns:
        TemplateResponse: Response with the contacts.html template.
    """
    return templates.TemplateResponse("contacts.html", {"request": request})


@app.get("/welcome")
def welcome(request: Request):
    """
    Welcome endpoint.

    Args:
        request (Request): The request object.

    Returns:
        TemplateResponse: Response with the welcome.html template.
    """
    return templates.TemplateResponse("welcome.html", {"request": request})


@app.get("/verify/{username}/{verification_token}")
def verify_email(username: str, verification_token: str):
    """
    Verify user's email.

    Args:
        username (str): Username of the user.
        verification_token (str): Verification token sent to the user's email.

    Returns:
        RedirectResponse: Redirects to the login page.
    """
    if username not in users_db:
        raise HTTPException(status_code=404, detail="Użytkownik nie istnieje")

    expected_token = "some_random_token"
    if verification_token != expected_token:
        raise HTTPException(status_code=400, detail="Nieprawidłowy token weryfikacyjny")

    users_db[username]["verified"] = True

    return RedirectResponse(url="/login")
