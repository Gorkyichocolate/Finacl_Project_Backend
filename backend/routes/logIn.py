from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from configs.auth_config import ACCESS_TOKEN_EXPIRE_MINUTES
from models.token_model import Token
from models.user_model import User
from services.auth import authenticate_user, create_access_token

router = APIRouter(tags=["authentication"])


class LoginRequest(BaseModel):
    username: str
    password: str
    scopes: list[str] = ["me", "items", "weather"]


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: User


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest) -> LoginResponse:
    
    user = await authenticate_user(request.username, request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь отключен"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scope": " ".join(request.scopes)},
        expires_delta=access_token_expires,
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            disabled=user.disabled
        )
    )


@router.post("/login/form", response_model=Token)
async def login_form(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    
    user = await authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь отключен"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scope": " ".join(form_data.scopes)},
        expires_delta=access_token_expires,
    )
    
    return Token(access_token=access_token, token_type="bearer")
