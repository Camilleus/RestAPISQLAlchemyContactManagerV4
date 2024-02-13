from pydantic import BaseModel
from datetime import date


class ContactCreateUpdate(BaseModel):
    """
    Model Pydantic reprezentujący dane do tworzenia lub aktualizacji kontaktu.
    """
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_data: str = None
    
    
class ContactResponse(BaseModel):
    """
    Model Pydantic reprezentujący odpowiedź zawierającą dane kontaktowe.
    """
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_data: str = None
