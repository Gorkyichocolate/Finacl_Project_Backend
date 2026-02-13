from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from configs.auth_config import ACCESS_TOKEN_EXPIRE_MINUTES
from models.token_model import Token
from services.auth import authenticate_user, create_access_token

router = APIRouter(tags=["authentication"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Неверное имя пользователя или пароль"
        )
    
    print(f"[DEBUG] Login for user: {user.username}")
    print(f"[DEBUG] Requested scopes: {form_data.scopes}")
    print(f"[DEBUG] Scopes type: {type(form_data.scopes)}")
    
    scopes = form_data.scopes if form_data.scopes else ["me", "weather"]
    scope_str = " ".join(scopes)
    print(f"[DEBUG] Final scope string: '{scope_str}'")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scope": scope_str},
        expires_delta=access_token_expires,
    )
    
    return Token(access_token=access_token, token_type="bearer")
