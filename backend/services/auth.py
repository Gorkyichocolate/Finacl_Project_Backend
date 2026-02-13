from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import SecurityScopes
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import ValidationError

from configs.auth_config import (
    SECRET_KEY, 
    ALGORITHM, 
    ACCESS_TOKEN_EXPIRE_MINUTES,
    oauth2_scheme
)
from models.user_model import User, UserInDB
from models.token_model import Token, TokenData
from repository.user import user_repository


password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


async def get_user(username: str) -> UserInDB | None:
    return await user_repository.get_user_by_username(username)


async def authenticate_user(username: str, password: str) -> UserInDB | bool:
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def create_user(username: str, email: str, password: str, full_name: str = None) -> UserInDB:

    if await user_repository.user_exists(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )
    
    if await user_repository.email_exists(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже используется"
        )
    
    user_data = {
        "username": username,
        "email": email,
        "hashed_password": get_password_hash(password),
        "full_name": full_name,
        "disabled": False
    }
    
    return await user_repository.create_user(user_data)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes, 
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": authenticate_value},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        scope: str = payload.get("scope", "")
        token_scopes = scope.split(" ") if scope else []
        
        print(f"[DEBUG] Token decoded for user: {username}")
        print(f"[DEBUG] Token scope string: '{scope}'")
        print(f"[DEBUG] Token scopes list: {token_scopes}")
        print(f"[DEBUG] Required scopes: {security_scopes.scopes}")
        
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недостаточно прав доступа",
                headers={"WWW-Authenticate": authenticate_value},
            )
    
    return user


async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Неактивный пользователь")
    return current_user
