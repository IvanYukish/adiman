from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.config import settings
from app.core.db import get_db

db = get_db()


def get_password_hash(password: str):
    return settings.pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return settings.pwd_context.verify(plain_password, hashed_password)


async def get_user(id: str):
    if (user := await db["users"].find_one({"_id": id})) is not None:
        return user


async def authenticate_user(id: str, password: str):
    user = await get_user(id)
    if not user:
        return False
    if not verify_password(password, user["hashed_pass"]):
        return False

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encode_jwt


# async def get_current_user(token: str = Depends(settings.oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         # token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = await get_user(username)
#     if user is None:
#         raise credentials_exception
#     return user