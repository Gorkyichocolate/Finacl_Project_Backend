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
    

def success_response(data: Any, message: Optional[str] = None) -> dict:
    response = {
        "success": True,
        "data": data
    }
    
    if message:
        response["message"] = message
    
    return response


def error_response(
    message: str,
    code: int = 400,
    details: Optional[Any] = None
) -> dict:
    
    error_dict = {
        "code": code,
        "message": message
    }
    
    if details:
        error_dict["details"] = details
    
    return {
        "success": False,
        "error": error_dict
    }


def paginated_response(
    data: list[Any],
    page: int,
    page_size: int,
    total: int,
    message: Optional[str] = None
) -> dict:
    
    total_pages = (total + page_size - 1) // page_size
    
    response = {
        "success": True,
        "data": data,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }
    
    if message:
        response["message"] = message
    
    return response
