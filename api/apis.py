from fastapi import FastAPI, HTTPException, Query, Depends, APIRouter, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from datetime import date, timedelta
from models import Contact, User, Token
from db.dbs import get_db, database
from typing import List
from auth.auths import get_current_active_user, login_for_access_token, get_current_user
from auth.jwts import create_jwt_token, decode_jwt_token
from models import Contact
from schemas import ContactCreateUpdate, ContactResponse
import cloudinary.uploader


app = FastAPI()


router = APIRouter()


limiter = FastAPILimiter([RateLimiter(second=60, max_calls=5)])


app.add_middleware(limiter)


# CRUD operations

@router.post("/contacts/", response_model=ContactResponse)
async def create_contact(contact: ContactCreateUpdate, current_user: User = Depends(get_current_active_user)):
    """
    Create a new contact.

    Args:
        contact (ContactCreateUpdate): Data of the new contact.
        current_user (User): Current authenticated user.

    Returns:
        dict: Details of the created contact.
    """
    await limiter.check(f"user:{current_user.username}", increment=True)

    query = Contact.__table__.insert().values(**contact.dict())
    contact_id = await database.execute(query)
    return {"id": contact_id, **contact.dict()}


@router.get("/contacts/", response_model=List[ContactResponse])
def get_all_contacts(
    q: str = Query(None, alias="search", description="Search contacts by first name, last name, or email"),
    db: Session = Depends(get_db)
):
    """
    Get all contacts or search contacts by name or email.

    Args:
        q (str, optional): Search query. Defaults to None.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        List[ContactResponse]: List of contacts.
    """
    if q:
        contacts = db.query(Contact).filter(
            Contact.first_name.ilike(f"%{q}%")
            | Contact.last_name.ilike(f"%{q}%")
            | Contact.email.ilike(f"%{q}%")
        ).all()
    else:
        contacts = db.query(Contact).all()
    return contacts


@router.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    Get a contact by ID.

    Args:
        contact_id (int): ID of the contact.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current authenticated user. Defaults to Depends(get_current_active_user).

    Returns:
        ContactResponse: Details of the contact.
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactCreateUpdate, db: Session = Depends(get_db)):
    """
    Update a contact by ID.

    Args:
        contact_id (int): ID of the contact to update.
        contact (ContactCreateUpdate): New data for the contact.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        ContactResponse: Updated details of the contact.
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.delete("/contacts/{contact_id}", response_model=ContactResponse)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Delete a contact by ID.

    Args:
        contact_id (int): ID of the contact to delete.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        ContactResponse: Details of the deleted contact.
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return contact


@router.get("/contacts/birthdays/", response_model=list[ContactResponse])
def get_birthdays_within_7_days(db: Session = Depends(get_db)):
    """
    Get contacts with birthdays within the next 7 days.

    Args:
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        list[ContactResponse]: List of contacts with birthdays within the next 7 days.
    """
    today = date.today()
    next_week = today + timedelta(days=7)

    contacts = db.query(Contact).filter(
        Contact.birth_date.between(today, next_week)
    ).all()

    return contacts


@router.post("/token/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordBearer = Depends()):
    """
    Login to get an access token.

    Args:
        form_data (OAuth2PasswordBearer, optional): Form data with username and password. Defaults to Depends().

    Returns:
        Token: Access token.
    """
    return login_for_access_token(form_data)


#cloudinary

@router.post("/users/avatar/upload/")
async def upload_avatar(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    """
    Upload avatar for the user.

    Args:
        file (UploadFile): Avatar file to upload.
        current_user (User): Current authenticated user.

    Returns:
        dict: Details of the uploaded avatar.
    """
    response = cloudinary.uploader.upload(file.file)
    current_user.avatar_url = response["secure_url"]
    return {"avatar_url": current_user.avatar_url}


app.include_router(router)
