from typing import Annotated

from fastapi import APIRouter, Depends, Security

from models.user_model import User
from services.auth import get_current_active_user, get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    
    return current_user


@router.get("/me/items")
async def read_own_items(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])],
):
    
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.get("/status")
async def read_system_status(
    current_user: Annotated[User, Depends(get_current_user)]
):
    
    return {"status": "ok", "user": current_user.username}
