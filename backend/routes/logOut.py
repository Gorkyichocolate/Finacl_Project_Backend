from typing import Annotated

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from models.user_model import User
from services.auth import get_current_user

router = APIRouter(tags=["authentication"])


class LogoutResponse(BaseModel):
    message: str
    username: str


@router.post("/logout", response_model=LogoutResponse, status_code=status.HTTP_200_OK)
async def logout(
    current_user: Annotated[User, Depends(get_current_user)]
) -> LogoutResponse:
    
    return LogoutResponse(
        message="Выход выполнен успешно. Удалите токен на клиенте.",
        username=current_user.username
    )


@router.post("/logout/all", response_model=LogoutResponse)
async def logout_all_devices(
    current_user: Annotated[User, Depends(get_current_user)]
) -> LogoutResponse:
    return LogoutResponse(
        message="Выход со всех устройств. Функция в разработке.",
        username=current_user.username
    )


class SessionInfo(BaseModel):
    username: str
    email: str | None
    full_name: str | None
    is_active: bool
    message: str


@router.get("/session", response_model=SessionInfo)
async def check_session(
    current_user: Annotated[User, Depends(get_current_user)]
) -> SessionInfo:
    return SessionInfo(
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=not current_user.disabled,
        message="Сессия активна"
    )
