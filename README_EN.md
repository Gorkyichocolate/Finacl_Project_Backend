# Weather Forecast Service API

## 📋 Project Description

Weather Forecast Service API is a full-featured web service for obtaining weather forecasts with a user authentication system. The project uses a modern technology stack and follows REST API development best practices.

---

## 🛠️ Technologies

### Backend
- **FastAPI** — modern, fast web framework for building APIs
- **MongoDB** — NoSQL database for storing users
- **Motor** — asynchronous MongoDB driver for Python
- **PyMongo** — synchronous MongoDB driver
- **Pydantic** — data validation and settings management
- **JWT (PyJWT)** — authentication tokens
- **PWDLib (Argon2)** — secure password hashing
- **HTTPX** — asynchronous HTTP client for external APIs
- **Uvicorn** — ASGI server for running the application

### Frontend
- **HTML/CSS/JavaScript** — client-side application

### External APIs
- **OpenWeatherMap API** — retrieving weather data
- **Google Geocoding API** — converting city names to coordinates

---

## 📁 Project Structure

```
Final_Project_Backend/
│
├── backend/                          # Backend application
│   ├── main.py                       # Application entry point, FastAPI setup
│   ├── requirements.txt              # Project dependencies
│   │
│   ├── configs/                      # Configuration files
│   │   ├── __init__.py
│   │   ├── auth_config.py            # Authentication settings (JWT, tokens)
│   │   └── db.py                     # MongoDB connection
│   │
│   ├── handlers/                     # Request and error handlers
│   │   ├── __init__.py
│   │   ├── exceptions.py             # Global exception handlers
│   │   ├── middleware.py             # Middleware (logging, security)
│   │   ├── response.py               # Response formatting utilities
│   │   └── validators.py             # Data validators
│   │
│   ├── models/                       # Pydantic models
│   │   ├── __init__.py
│   │   ├── user_model.py             # User model
│   │   ├── token_model.py            # Token model
│   │   ├── response_model.py         # Base response models
│   │   ├── rate_limit_model.py       # Rate limiting model
│   │   ├── weatherCurrent.py         # Current weather model
│   │   ├── weatherHourly.py          # Hourly forecast model
│   │   └── weatherDaily.py           # Daily forecast model
│   │
│   ├── repository/                   # Data Access Layer
│   │   ├── __init__.py
│   │   ├── user.py                   # CRUD operations for users
│   │   └── weather.py                # Weather caching operations
│   │
│   ├── routes/                       # API routes (endpoints)
│   │   ├── __init__.py
│   │   ├── signUp.py                 # User registration
│   │   ├── logIn.py                  # User login
│   │   ├── logOut.py                 # User logout
│   │   ├── token.py                  # Token retrieval (OAuth2)
│   │   ├── user.py                   # User operations
│   │   └── weather.py                # Weather forecast retrieval
│   │
│   └── services/                     # Application business logic
│       ├── __init__.py
│       ├── auth.py                   # Authentication and authorization logic
│       ├── geocoding.py              # Google Geocoding API integration
│       └── weather.py                # OpenWeatherMap API integration
│
├── frontend/                         # Frontend application
│   ├── html/                         # HTML pages
│   │   ├── login.html                # Login page
│   │   ├── signup.html               # Registration page
│   │   └── main.html                 # Main page
│   ├── css/
│   │   └── style.css                 # Styles
│   └── javascript/
│       └── script.js                 # Client-side logic
│
├── init_db.py                        # Database initialization script
└── README.md                         # Project documentation
```

---

## 📦 Component Responsibilities

### 🔧 `configs/`
- **auth_config.py** — stores secret keys, JWT encryption algorithms, token lifetime
- **db.py** — manages MongoDB connection, creates database client

### 🛡️ `handlers/`
- **exceptions.py** — intercepts and handles all application errors
- **middleware.py** — processes each request (logging, security headers)
- **response.py** — standardizes API response format
- **validators.py** — validates incoming data for correctness

### 📊 `models/`
Define data structure using Pydantic:
- Type validation
- JSON serialization/deserialization
- API schema documentation

### 💾 `repository/`
Abstraction layer for database operations:
- **user.py** — create, find, update users
- **weather.py** — cache weather query results

### 🌐 `routes/`
Define API endpoints and connect HTTP requests to business logic:
- Handle incoming requests
- Call services to perform operations
- Return structured responses

### 🎯 `services/`
Contain core business logic:
- **auth.py** — authentication, user creation, access rights verification
- **geocoding.py** — retrieve city coordinates via Google API
- **weather.py** — retrieve weather data via OpenWeatherMap API

---

## 🔐 API Endpoints

### Base URL
```
http://localhost:8000
```

---

### 🔑 Authentication

#### 1. **User Registration**
```http
POST /signup
```

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

---

#### 2. **Login (Get Token)**
```http
POST /login
```

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "SecurePassword123!",
  "scopes": ["me", "items", "weather"]
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "disabled": false
  }
}
```

---

#### 3. **OAuth2 Token (for Swagger UI)**
```http
POST /token
Content-Type: application/x-www-form-urlencoded
```

**Form Parameters:**
```
username=john_doe
password=SecurePassword123!
scope=me weather
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

#### 4. **Logout**
```http
POST /logout
Authorization: Bearer <your_token>
```

**Response:**
```json
{
  "message": "Logged out successfully. Delete token on client side.",
  "username": "john_doe"
}
```

---

#### 5. **Check Session**
```http
GET /session
Authorization: Bearer <your_token>
```

**Response:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "message": "Session is active"
}
```

---

### 👤 User

#### 6. **Get Current User Information**
```http
GET /users/me
Authorization: Bearer <your_token>
```

**Response:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

---

#### 7. **Get System Status**
```http
GET /users/status
Authorization: Bearer <your_token>
```

**Response:**
```json
{
  "status": "ok",
  "user": "john_doe"
}
```

---

### 🌦️ Weather

> **⚠️ All weather endpoints require a token with `weather` scope**

#### 8. **Get Current Weather**
```http
GET /weather/current?city=London
Authorization: Bearer <your_token>
```

**Response:**
```json
{
  "city": "London",
  "country": "GB",
  "timestamp": 1644840000,
  "datetime": "2022-02-14T12:00:00Z",
  "temperature": 8.5,
  "feels_like": 6.2,
  "temp_min": 7.0,
  "temp_max": 10.0,
  "pressure": 1013,
  "humidity": 75,
  "description": "partly cloudy",
  "icon": "02d",
  "wind_speed": 4.5,
  "wind_deg": 240,
  "clouds": 40,
  "visibility": 10000
}
```

---

#### 9. **Get Hourly Forecast (12 Hours)**
```http
GET /weather/hourly-12?city=London
Authorization: Bearer <your_token>
```

**Response:** Array of 12 hourly forecasts
```json
[
  {
    "timestamp": 1644840000,
    "datetime": "2022-02-14T12:00:00Z",
    "temperature": 8.5,
    "feels_like": 6.2,
    "description": "cloudy",
    "icon": "03d",
    "wind_speed": 4.5,
    "humidity": 75,
    "pop": 0.2
  },
  ...
]
```

---

#### 10. **Get Tomorrow's Weather**
```http
GET /weather/tomorrow?city=London
Authorization: Bearer <your_token>
```

**Response:**
```json
{
  "date": "2022-02-15",
  "temp_day": 10.5,
  "temp_min": 7.0,
  "temp_max": 12.0,
  "temp_night": 6.5,
  "temp_eve": 9.0,
  "temp_morn": 7.5,
  "feels_like_day": 9.0,
  "feels_like_night": 5.0,
  "pressure": 1015,
  "humidity": 70,
  "description": "clear",
  "icon": "01d",
  "wind_speed": 3.5,
  "wind_deg": 200,
  "clouds": 10,
  "pop": 0.1
}
```

---

#### 11. **Get 3-Day Forecast**
```http
GET /weather/forecast-3days?city=London
Authorization: Bearer <your_token>
```

**Response:** Array of 3 daily forecasts

---

#### 12. **Get 7-Day Forecast**
```http
GET /weather/forecast-7days?city=London
Authorization: Bearer <your_token>
```

**Response:** Array of 7 daily forecasts

---

### 🗺️ Geocoding

#### 13. **Get City Coordinates**
```http
GET /coordinates?city=London
```

**Response:**
```json
{
  "city": "London",
  "country": "UK",
  "lat": 51.5074,
  "lon": -0.1278
}
```

---

## 🚀 Installation and Setup

### 1. Clone Repository
```bash
git clone <repository_url>
cd Finacl_Project_Backend
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=weather_db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenWeatherMap API
OPENWEATHER_API_KEY=your-openweather-api-key

# Google Geocoding API
GOOGLE_API_KEY=your-google-api-key
```

### 5. Initialize Database
```bash
python init_db.py
```

### 6. Start Server
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Open API Documentation
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📝 Usage Examples

### Using cURL

#### Registration
```bash
curl -X POST "http://localhost:8000/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "full_name": "Test User"
  }'
```

#### Login and Get Token
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!",
    "scopes": ["me", "weather"]
  }'
```

#### Get Current Weather
```bash
TOKEN="your_access_token_here"

curl -X GET "http://localhost:8000/weather/current?city=Moscow" \
  -H "Authorization: Bearer $TOKEN"
```

---

### Using Python (httpx)

```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        # Registration
        signup_response = await client.post(
            "http://localhost:8000/signup",
            json={
                "username": "pythonuser",
                "email": "python@example.com",
                "password": "PythonPass123!",
                "full_name": "Python User"
            }
        )
        print(signup_response.json())
        
        # Login
        login_response = await client.post(
            "http://localhost:8000/login",
            json={
                "username": "pythonuser",
                "password": "PythonPass123!",
                "scopes": ["me", "weather"]
            }
        )
        token = login_response.json()["access_token"]
        
        # Get Weather
        weather_response = await client.get(
            "http://localhost:8000/weather/current",
            params={"city": "Paris"},
            headers={"Authorization": f"Bearer {token}"}
        )
        print(weather_response.json())

asyncio.run(main())
```

---

## 🔒 Security

### Implemented Mechanisms:
- ✅ **JWT tokens** for authentication
- ✅ **Argon2** for password hashing
- ✅ **OAuth2 with scopes** for granular authorization
- ✅ **CORS middleware** for access control
- ✅ **Security Headers** (CSP, X-Frame-Options, etc.)
- ✅ **Request Logging** for monitoring
- ✅ **Data validation** via Pydantic

### Scopes:
- `me` — access to user information
- `items` — access to user items
- `weather` — access to weather data

---

## 🧪 Testing

### Via Swagger UI
1. Open http://localhost:8000/docs
2. Click "Authorize" in the top right corner
3. Use the `/token` endpoint to get a token
4. Enter the token in the authorization form
5. Test endpoints through the interface

---

## 📊 Architectural Decisions

### Layered Architecture:
```
Routes (API Layer)
    ↓
Services (Business Logic)
    ↓
Repository (Data Access)
    ↓
Database (MongoDB)
```

### Benefits:
- **Separation of concerns** — each layer has its own responsibility
- **Easy testing** — each layer can be tested independently
- **Flexibility** — easy to replace database or external API
- **Scalability** — new features can be added without changing existing code

---

## 🐛 Error Handling

All errors are returned in a standardized format:

```json
{
  "detail": "Error description",
  "status_code": 404
}
```

### Status Codes:
- `200` — Successful request
- `201` — Resource created
- `400` — Bad request
- `401` — Unauthorized
- `403` — Forbidden
- `404` — Resource not found
- `500` — Internal server error

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [JWT.io](https://jwt.io/)

---

## 👨‍💻 Author

Project developed as part of a final web development course project.

---

## 📄 License

MIT License
