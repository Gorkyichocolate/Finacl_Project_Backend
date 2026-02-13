from typing import Annotated, List

from fastapi import APIRouter, Depends, Security, HTTPException

from models.user_model import User
from models.weatherCurrent import CurrentWeatherResponse
from models.weatherHourly import HourlyWeatherResponse
from models.weatherDaily import DailyWeatherResponse
from services.auth import get_current_active_user
from services.weather import weather_service

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/current", response_model=CurrentWeatherResponse)
async def get_current_weather(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["weather"])],
    city: str,
):
    
    try:
        weather = await weather_service.get_current_weather(city)
        return weather
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения погоды: {str(e)}")


@router.get("/hourly-12", response_model=List[HourlyWeatherResponse])
async def get_hourly_12_hours(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["weather"])],
    city: str,
):
    try:
        forecast = await weather_service.get_hourly_12_hours(city)
        return forecast
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения прогноза: {str(e)}")


@router.get("/tomorrow", response_model=DailyWeatherResponse)
async def get_tomorrow_weather(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["weather"])],
    city: str,
):

    try:
        weather = await weather_service.get_tomorrow_weather(city)
        return weather
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения прогноза: {str(e)}")


@router.get("/forecast-3days", response_model=List[DailyWeatherResponse])
async def get_3_days_forecast(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["weather"])],
    city: str,
):

    try:
        forecast = await weather_service.get_3_days_forecast(city)
        return forecast
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения прогноза: {str(e)}")


@router.get("/forecast-7days", response_model=List[DailyWeatherResponse])
async def get_7_days_forecast(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["weather"])],
    city: str,
):
    try:
        forecast = await weather_service.get_7_days_forecast(city)
        return forecast
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения прогноза: {str(e)}")
