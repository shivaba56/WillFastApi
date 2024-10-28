from datetime import datetime, timedelta
from typing import Tuple, Union
from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from .conf import settings

from core.auth.models import User


def create_access_token(user: User, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = {
        "sub": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(user: User, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = {
        "sub": user.username,
        "email": user.email
    }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_REFRESH_EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def create_tokens(user: User) -> Tuple[str, str]:
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRATION_TIME)
    refresh_token_expires = timedelta(days=settings.JWT_REFRESH_EXPIRATION_TIME)

    access_token = create_access_token(user, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(user, expires_delta=refresh_token_expires)

    return access_token, refresh_token

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise JWTError("Could not validate credentials")


async def get_current_user(request: Request) -> User:
    user = getattr(request.state, "user", None)
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user