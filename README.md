# Weather Forecast Service

## 🚀 Quick Start (One Command!)

```bash
cd backend && fastapi dev main.py
```

**That's it!** Both backend and frontend start together on **http://localhost:8000**

## 🌐 Access URLs

- **Frontend (Login)**: http://localhost:8000/static/html/login.html
- **Frontend (Main)**: http://localhost:8000/static/html/main.html  
- **API Documentation**: http://localhost:8000/docs
- **API Base**: http://localhost:8000

## 🎯 Features

### Backend (FastAPI)
- ✅ OAuth2 + JWT authentication
- ✅ MongoDB with async motor
- ✅ Weather API integration (Google Geocoding + Weather API)
- ✅ 11 API endpoints
- ✅ Password hashing (Argon2)
- ✅ Request logging middleware
- ✅ Security headers middleware
- ✅ Global exception handling
- ✅ CORS configured
- ✅ Static files serving

### Frontend
- ✅ Responsive design
- ✅ Authentication flow (login/signup/logout)
- ✅ Dynamic weather-based themes (10 variants)
- ✅ Real-time weather data
- ✅ 3 pages: login, signup, main dashboard

## 🔑 Test Credentials

```
Username: johndoe
Password: secret

Username: alice
Password: secret2
```

## 📁 Project Structure

```
Finacl_Project_Backend/
├── backend/
│   ├── main.py              # Application entry point
│   ├── configs/             # Configuration files
│   ├── handlers/            # Exception handlers, middleware, validators
│   ├── models/              # Pydantic models
│   ├── repository/          # Database operations
│   ├── routes/              # API routes
│   ├── services/            # Business logic
│   └── requirements.txt     # Python dependencies
└── frontend/
    ├── html/                # HTML pages (login, signup, main)
    ├── css/                 # Styles with dynamic themes
    └── javascript/          # Frontend logic
```

## 📡 API Endpoints

### Authentication
- `POST /token` - Get access token (OAuth2)
- `POST /signup` - Register new user
- `POST /login` - Alternative login endpoint
- `POST /logout` - Logout endpoint
- `GET /session` - Check session status

### User
- `GET /users/me` - Get current user info (protected)

### Weather (Protected)
- `GET /weather/current?city=...` - Current weather
- `GET /weather/hourly-12?city=...` - 12-hour forecast  
- `GET /weather/tomorrow?city=...` - Tomorrow's weather
- `GET /weather/forecast-3days?city=...` - 3-day forecast
- `GET /weather/forecast-7days?city=...` - 7-day forecast

### Public
- `GET /` - API info
- `GET /coordinates?city=...` - Get city coordinates

## ⚙️ Environment Variables

Create `.env` file in `backend/` directory:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=weather_db
GOOGLE_API_KEY=your_google_api_key_here
SECRET_KEY=your_secret_jwt_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🛠️ Installation

1. **Clone repository**
   ```bash
   git clone <repo_url>
   cd Finacl_Project_Backend
   ```

2. **Install Python dependencies**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Start MongoDB**
   ```bash
   sudo systemctl start mongodb
   # or use Docker: docker run -d -p 27017:27017 mongo
   ```

4. **Create .env file** (see Environment Variables section)

5. **Run application**
   ```bash
   fastapi dev main.py
   ```

6. **Open browser**: http://localhost:8000/static/html/login.html

## 🎨 Dynamic Weather Themes

The frontend automatically changes theme based on weather:
- ☀️ Clear Day/Night
- ⛅ Partly Cloudy
- ☁️ Cloudy
- 🌧️ Rain
- 🌨️ Snow
- 🌫️ Fog
- ⛈️ Storm

## 🔧 Development

The application uses:
- **FastAPI** with Uvicorn (auto-reload enabled)
- **MongoDB** for data storage (users, weather cache with TTL)
- **StaticFiles** for serving frontend
- **JWT tokens** with 30-minute expiration
- **Middleware** for logging and security headers

All changes to backend or frontend files will **auto-reload**!

## 📦 Dependencies

Main packages:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `motor` - Async MongoDB driver
- `pydantic` - Data validation
- `pwdlib[argon2]` - Password hashing
- `python-jose` - JWT handling
- `python-multipart` - Form data support
- `httpx` - HTTP client for external APIs

## 🚀 Production Deployment

For production:
1. ✅ Set specific CORS origins (not "*")
2. ✅ Use environment-specific configs
3. ✅ Enable rate limiting (already implemented)
4. ✅ Set up proper logging
5. ✅ Use HTTPS/reverse proxy (nginx)
6. ✅ Deploy MongoDB separately
7. ✅ Add monitoring/alerting
8. ✅ Use production ASGI server (uvicorn workers)

## 📝 Notes

- **No separate frontend server needed** - frontend served from FastAPI
- **Single port (8000)** - all requests through same server
- **Handlers fully integrated** - logging, security, exceptions
- **MongoDB auto-creates collections** on first use
- **TTL indexes** - weather data expires automatically after 24h
- **Scopes implemented** - `me`, `weather`, `items`

## 🐛 Troubleshooting

**MongoDB connection error?**
- Check if MongoDB is running: `sudo systemctl status mongodb`
- Verify MONGODB_URL in .env

**Google API error?**  
- Check GOOGLE_API_KEY in .env
- Verify API is enabled in Google Cloud Console

**Frontend not loading?**
- Check path: http://localhost:8000/static/html/login.html
- Verify frontend directory exists relative to backend/

**Token expired?**
- Default expiration: 30 minutes
- Just login again to get new token

## 📊 Project Status

**Completion: 95%**

✅ Backend API (100%)
✅ Frontend UI (100%)  
✅ Authentication (100%)
✅ Weather Integration (100%)
✅ Handlers Integration (100%)
✅ Documentation (95%)
⬜ Unit Tests (0%)
⬜ Docker Setup (0%)

## 👨‍💻 Author

Final Project - Weather Forecast Service
FastAPI + MongoDB + Weather API