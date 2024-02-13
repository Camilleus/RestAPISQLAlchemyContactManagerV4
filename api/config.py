from fastapi.security import OAuth2PasswordBearer
import os 


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


"""
Konfiguracja aplikacji.

Zawiera informacje dotyczące klucza sekretnego, algorytmu uwierzytelniania
i schematu uwierzytelniania OAuth2.

Attributes:
    SECRET_KEY (str): Klucz sekretny aplikacji.
    ALGORITHM (str): Algorytm uwierzytelniania.
    oauth2_scheme (OAuth2PasswordBearer): Schemat uwierzytelniania OAuth2.
"""
