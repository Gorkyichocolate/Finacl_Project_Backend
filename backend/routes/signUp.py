from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

from services.auth import create_user
from models.user_model import User

router = APIRouter(tags=["authentication"])


class SignUpRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str | None = None


@router.post("/signup", response_model=User)
async def sign_up(request: SignUpRequest) -> User:
    
    try:
        user = await create_user(
            username=request.username,
            email=request.email,
            password=request.password,
            full_name=request.full_name
        )
        
        return User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            disabled=user.disabled
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании пользователя: {str(e)}"
        ) 
    