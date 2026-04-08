# Microservices layout

This folder contains service-specific FastAPI entrypoints.

## Services

- auth_service: authentication and token routes
- user_service: user profile and user status routes
- weather_service: weather and geocoding routes

Each service has its own:

- routes/
- services/
- repository/
- models/
- configs/
- handlers/

## Run commands

Run from backend/ directory:

```bash
uvicorn microservices.auth_service.main:app --host 0.0.0.0 --port 8001 --reload
uvicorn microservices.user_service.main:app --host 0.0.0.0 --port 8002 --reload
uvicorn microservices.weather_service.main:app --host 0.0.0.0 --port 8003 --reload
```

## Notes

- Existing monolith entrypoint remains in main.py.
- Services are isolated at the code package level and import only from their own service namespace.
- Next step for runtime separation is to provision separate databases/collections and deploy each service independently.
