from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from microservices.user_service.configs.db import close_mongodb_connection, connect_to_mongodb
from microservices.user_service.handlers.exceptions import (
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from microservices.user_service.handlers.middleware import (
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
)
from microservices.user_service.routes import user


@asynccontextmanager
async def lifespan(app):
    await connect_to_mongodb()
    yield
    await close_mongodb_connection()


app = FastAPI(
    title="User Service",
    description="User profile microservice",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)


@app.get("/")
async def root():
    return {"service": "user", "status": "ok"}
