# Weather Forecast Service API

## Описание

Проект переведен на микросервисную архитектуру. Backend разделен на 3 сервиса:

- `auth_service` — регистрация, логин, токены, сессия
- `user_service` — профиль пользователя и защищенные user-эндпоинты
- `weather_service` — погодные эндпоинты и геокодинг

## Технологии

- FastAPI
- MongoDB + Motor
- Pydantic
- JWT (PyJWT)
- pwdlib (Argon2)
- HTTPX
- Uvicorn

## Актуальная структура

```text
Final_Project_Backend/
├── backend/
│   ├── microservices/
│   │   ├── auth_service/
│   │   │   ├── main.py
│   │   │   ├── routes/
│   │   │   ├── services/
│   │   │   ├── repository/
│   │   │   ├── models/
│   │   │   ├── configs/
│   │   │   └── handlers/
│   │   ├── user_service/
│   │   │   ├── main.py
│   │   │   ├── routes/
│   │   │   ├── services/
│   │   │   ├── repository/
│   │   │   ├── models/
│   │   │   ├── configs/
│   │   │   └── handlers/
│   │   └── weather_service/
│   │       ├── main.py
│   │       ├── routes/
│   │       ├── services/
│   │       ├── repository/
│   │       ├── models/
│   │       ├── configs/
│   │       └── handlers/
│   ├── Procfile
│   ├── requirements.txt
│   └── runtime.txt
├── frontend/
├── init_db.py
├── README.md
└── README_EN.md
```

## Локальный запуск

Из каталога `backend`:

```bash
uvicorn microservices.auth_service.main:app --host 0.0.0.0 --port 8001 --reload
uvicorn microservices.user_service.main:app --host 0.0.0.0 --port 8002 --reload
uvicorn microservices.weather_service.main:app --host 0.0.0.0 --port 8003 --reload
```

## Render

Текущий `Procfile` настроен на запуск auth-сервиса:

```text
web: uvicorn microservices.auth_service.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

## Примечание

Старый монолитный backend (`main.py`, `routes/`, `services/`, `models/`, `repository/`, `configs/`, `handlers/`) удален как неиспользуемый.
