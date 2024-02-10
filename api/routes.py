from fastapi import APIRouter, Depends, Request
from auth.auths import refresh_access_token
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Token


router = APIRouter()


templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello, world!"})


@router.post("/refresh-token/", response_model=Token)
async def refresh_token(current_token: str = Depends(refresh_access_token)):
    return current_token