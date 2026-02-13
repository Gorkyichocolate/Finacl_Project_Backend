"""
Handlers модуль
Содержит обработчики исключений, middleware, валидаторы и утилиты для ответов
"""
from .exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
    weather_api_exception_handler,
    WeatherAPIException,
    CityNotFoundException,
    WeatherServiceException,
)
from .middleware import (
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
    RateLimitMiddleware,
)
from .response import (
    success_response,
    error_response,
    paginated_response,
    SuccessResponse,
    ErrorResponse,
    PaginatedResponse,
)
from .validators import (
    validate_city_name,
    validate_username,
    validate_email,
    validate_password,
    validate_coordinates,
    validate_pagination,
)

__all__ = [
    "http_exception_handler",
    "validation_exception_handler",
    "general_exception_handler",
    "weather_api_exception_handler",
    "WeatherAPIException",
    "CityNotFoundException",
    "WeatherServiceException",
    "RequestLoggingMiddleware",
    "SecurityHeadersMiddleware",
    "RateLimitMiddleware",
    "success_response",
    "error_response",
    "paginated_response",
    "SuccessResponse",
    "ErrorResponse",
    "PaginatedResponse",
    "validate_city_name",
    "validate_username",
    "validate_email",
    "validate_password",
    "validate_coordinates",
    "validate_pagination",
]
