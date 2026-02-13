from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
import os

from services import geocoding
from routes import token, user, weather, signUp, logIn, logOut
from configs.db import connect_to_mongodb, close_mongodb_connection
from handlers.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from handlers.middleware import (
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    await connect_to_mongodb()
    yield
    await close_mongodb_connection()


app = FastAPI(
    title="Weather Forecast Service API",
    description="Weather forecast API with OAuth2 authentication and MongoDB",
    version="2.0.0",
    lifespan=lifespan
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

app.include_router(token.router)
app.include_router(signUp.router)
app.include_router(logIn.router)
app.include_router(logOut.router)
app.include_router(user.router)
app.include_router(weather.router)

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
    print(f"✓ Frontend mounted at /static")
    print(f"  → Login: http://localhost:8000/static/html/login.html")
    print(f"  → Main: http://localhost:8000/static/html/main.html")
else:
    print(f"⚠ Frontend directory not found at {frontend_path}")

print(f"Google API Key loaded: {bool(geocoding.GOOGLE_API_KEY)}")


@app.get("/")
async def root():
    return {
        "message": "Weather Forecast Service API",
        "docs": "/docs",
        "version": "2.0.0"
    }


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/static/favicon.svg")


@app.get("/coordinates")
async def get_coordinates(city: str):
    result = await geocoding.get_coordinates(city)

    if not result:
        raise HTTPException(status_code=404, detail="City not found")

    return result

