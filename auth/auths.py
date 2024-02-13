from fastapi import HTTPException, Depends, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models import Token, User
from auth.jwts import create_jwt_token, decode_jwt_token
from api.config import SECRET_KEY, ALGORITHM, oauth2_scheme


ACCESS_TOKEN_EXPIRE_MINUTES = 30


EMAIL_ADDRESS = "email@example.com"  #TODO
EMAIL_PASSWORD = "email_password"   #TODO


def authenticate_user(username: str, password: str):
    """
    Funkcja do autentykacji użytkownika.

    Args:
        username (str): Nazwa użytkownika.
        password (str): Hasło użytkownika.

    Returns:
        User: Zwraca obiekt użytkownika, jeśli autentykacja zakończyła się sukcesem, w przeciwnym razie None.
    """
    if username == "test" and password == "testpassword":
        return User(username="test", email="test@example.com", hashed_password="testpassword")
    return None


def create_access_token(data: dict, expires_delta: timedelta):
    """
    Funkcja tworząca token dostępu.

    Args:
        data (dict): Dane do zakodowania w tokenie.
        expires_delta (timedelta): Okres czasu ważności tokenu.

    Returns:
        str: Zakodowany token JWT.
    """
    return create_jwt_token(data, expires_delta)


def login_for_access_token(form_data: OAuth2PasswordBearer = Depends()):
    """
    Endpoint do logowania użytkownika i uzyskiwania tokena dostępu.

    Args:
        form_data (OAuth2PasswordBearer): Dane logowania użytkownika.

    Returns:
        dict: Zwraca token dostępu i typ tokenu.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


def refresh_access_token(current_token: str = Depends(oauth2_scheme)):
    """
    Endpoint odświeżający token dostępu.

    Args:
        current_token (str): Obecny token dostępu.

    Returns:
        dict: Zwraca odświeżony token dostępu i typ tokenu.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_jwt_token(current_token)
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
    except:
        raise credentials_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refreshed_token = create_jwt_token(data={"sub": sub}, expires_delta=access_token_expires)

    return {"access_token": refreshed_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Funkcja uzyskująca aktualnego użytkownika na podstawie tokena dostępu.

    Args:
        token (str): Token dostępu.

    Returns:
        User: Zwraca obiekt użytkownika na podstawie tokenu.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = Token(username=username)
    except JWTError:
        raise credentials_exception
    
    
def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Funkcja uzyskująca aktualnego aktywnego użytkownika.

    Args:
        current_user (User): Obecny użytkownik.

    Raises:
        HTTPException: Wyjątek HTTP w przypadku nieaktywnego użytkownika.

    Returns:
        User: Zwraca aktualnego aktywnego użytkownika.
    """
    if current_user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def send_email(email: str, token: str):
    """
    Funkcja wysyłająca e-mail weryfikacyjny.

    Args:
        email (str): Adres e-mail odbiorcy.
        token (str): Token weryfikacyjny.
    """
    subject = "Weryfikacja konta"
    message = f"Witaj! Twój token weryfikacyjny to: {token}"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, email, msg.as_string())