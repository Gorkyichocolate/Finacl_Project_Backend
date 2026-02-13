import re
from typing import Optional
from fastapi import HTTPException, status


def validate_city_name(city: str) -> str:

    if not city or len(city.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City name cannot be empty"
        )
    
    city = city.strip()
    
    if len(city) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City name must contain at least 2 characters"
        )
    
    if len(city) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City name is too long (maximum 100 characters)"
        )
    
    if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s\-]+$', city):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City name contains invalid characters"
        )
    
    return city


def validate_username(username: str) -> str:
    if not username or len(username.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username cannot be empty"
        )
    
    username = username.strip()
    
    if len(username) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must contain at least 3 characters"
        )
    
    if len(username) > 30:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is too long (maximum 30 characters)"
        )
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username can only contain letters, numbers and underscore"
        )
    
    return username


def validate_email(email: str) -> str:
    
    if not email or len(email.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email cannot be empty"
        )
    
    email = email.strip().lower()
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email address format"
        )
    
    return email


def validate_password(password: str) -> str:

    if not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password cannot be empty"
        )
    
    if len(password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least 6 characters"
        )
    
    if len(password) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too long (maximum 100 characters)"
        )
    
    has_digit = any(char.isdigit() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    
    if not (has_digit and has_upper and has_lower):
        pass
    
    return password


def validate_coordinates(latitude: float, longitude: float) -> tuple[float, float]:
    if not -90 <= latitude <= 90:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid latitude: {latitude}. Must be in range [-90, 90]"
        )
    
    if not -180 <= longitude <= 180:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid longitude: {longitude}. Must be in range [-180, 180]"
        )
    
    return latitude, longitude


def validate_pagination(page: int, page_size: int) -> tuple[int, int]:
    
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page number must be >= 1"
        )
    
    if page_size < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page size must be >= 1"
        )
    
    if page_size > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page size cannot exceed 100 items"
        )
    
    return page, page_size
