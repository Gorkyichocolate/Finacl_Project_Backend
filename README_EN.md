# Weather Forecast Service API

## Description

The project has been migrated to a microservices architecture. Backend is split into 3 services:

- `auth_service` — signup, login, token, session
- `user_service` — user profile and protected user endpoints
- `weather_service` — weather endpoints and geocoding

## Tech Stack

- FastAPI
- MongoDB + Motor
- Pydantic
- JWT (PyJWT)
- pwdlib (Argon2)
- HTTPX
- Uvicorn

## Current Structure

```text
Final_Project_Backend/
├── backend/
│   ├── microservices/
│   │   ├── auth_service/
│   │   ├── user_service/
│   │   └── weather_service/
│   ├── Procfile
│   ├── requirements.txt
│   └── runtime.txt
├── frontend/
├── init_db.py
├── README.md
└── README_EN.md
```

## Local Run

From `backend` directory:

```bash
uvicorn microservices.auth_service.main:app --host 0.0.0.0 --port 8001 --reload
uvicorn microservices.user_service.main:app --host 0.0.0.0 --port 8002 --reload
uvicorn microservices.weather_service.main:app --host 0.0.0.0 --port 8003 --reload
```

## Render

Current `Procfile` is configured to run auth service:

```text
web: uvicorn microservices.auth_service.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

## Note

Legacy monolith backend (`main.py`, `routes/`, `services/`, `models/`, `repository/`, `configs/`, `handlers/`) was removed as unused.
