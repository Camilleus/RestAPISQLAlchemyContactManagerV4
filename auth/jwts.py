from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from api.config import SECRET_KEY, ALGORITHM, oauth2_scheme


def create_jwt_token(data: dict, expires_delta: timedelta):
    """
    Tworzy token JWT na podstawie przekazanych danych.

    Args:
        data (dict): Dane do zakodowania w tokenie.
        expires_delta (timedelta): Okres czasu ważności tokenu.

    Returns:
        str: Zakodowany token JWT.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_token(token: str = Depends(oauth2_scheme)):
    """
    Dekoduje token JWT.

    Args:
        token (str): Token JWT do zdekodowania.

    Raises:
        HTTPException: Wyjątek HTTP w przypadku niepowodzenia weryfikacji tokenu.

    Returns:
        dict: Zdekodowane dane z tokenu.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception
