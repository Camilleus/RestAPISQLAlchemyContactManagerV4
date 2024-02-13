from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
from pydantic import BaseModel
import cloudinary

# Konfiguracja cloudinary
cloudinary.config( 
  cloud_name = "dfqqteqmv", 
  api_key = "724751544977486", 
  api_secret = "***************************" 
)

# Utwórz obiekt bazowy dla modeli SQLAlchemy
Base = declarative_base()


class Contact(BaseModel):
    """
    Model danych dla kontaktu.
    """
    __tablename__ = "contacts"

    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: Date
    additional_data: str = None

    class Config:
        arbitrary_types_allowed = True
        

class Token(BaseModel):
    """
    Model danych dla tokena dostępu.
    """
    __tablename__ = "tokens"

    id: int 
    access_token: str
    token_type: str

    class Config:
        arbitrary_types_allowed = True
        
        
class User(Base):
    """
    Model danych dla użytkownika.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)  
    avatar_url: str = None

    class Config:
        arbitrary_types_allowed = True
        

# Inicjalizacja kontekstu hashowania
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
