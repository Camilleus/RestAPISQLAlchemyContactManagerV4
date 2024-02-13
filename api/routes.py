from fastapi import APIRouter, Depends, Request
from auth.auths import refresh_access_token
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Token


router = APIRouter()


templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    """
    Read the root endpoint.

    Args:
        request (Request): The request object.

    Returns:
        TemplateResponse: Response with the index.html template.
    """
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello, world!"})


@router.post("/refresh-token/", response_model=Token)
async def refresh_token(current_token: str = Depends(refresh_access_token)):
    """
    Refresh access token.

    Args:
        current_token (str): The current access token.

    Returns:
        Token: Response with the new access token.
    """
    return current_token
