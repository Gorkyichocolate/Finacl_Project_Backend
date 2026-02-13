from typing import Any, Optional
from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool = True
    data: Any
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: dict[str, Any]


class PaginatedResponse(BaseModel):
    success: bool = True
    data: list[Any]
    pagination: dict[str, Any]
