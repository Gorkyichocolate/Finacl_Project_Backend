import httpx
import os
from typing import List
from dotenv import load_dotenv

from models.weatherCurrent import CurrentWeather, CurrentWeatherResponse, map_current
from models.weatherHourly import HourlyWeather, HourlyWeatherResponse, map_hour
from models.weatherDaily import DailyWeather, DailyWeatherResponse, map_day
from services.geocoding import get_coordinates
from repository.weather import weather_repository

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
WEATHER_API_BASE = "https://weather.googleapis.com/v1"


class WeatherService:
    
    def __init__(self):
        self.api_key = GOOGLE_API_KEY
    
    def _check_api_key(self):
        """Проверка наличия API ключа"""
        if not self.api_key or self.api_key == "your-google-api-key-here":
            raise ValueError(
                "Google API Key не настроен. "
                "Получите ключ на https://console.cloud.google.com/ "
                "и добавьте в .env файл"
            )
    
    async def _get_current_conditions(
        self, 
        latitude: float, 
        longitude: float
    ) -> dict:
        """
        Получить текущие погодные условия
        Эндпоинт: https://weather.googleapis.com/v1/currentConditions:lookup
        """
        self._check_api_key()
        url = f"{WEATHER_API_BASE}/currentConditions:lookup"
        
        params = {
            "key": self.api_key,
            "location.latitude": latitude,
            "location.longitude": longitude,
        }
        headers = {"X-Goog-Api-Key": self.api_key}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
    
    async def _get_hourly_forecast(
        self, 
        latitude: float, 
        longitude: float,
        hours: int = 12
    ) -> dict:
        """
        Получить почасовой прогноз
        Эндпоинт: https://weather.googleapis.com/v1/forecast/hours:lookup
        """
        self._check_api_key()
        url = f"{WEATHER_API_BASE}/forecast/hours:lookup"
        
        params = {
            "key": self.api_key,
            "location.latitude": latitude,
            "location.longitude": longitude,
            "hours": hours,
        }
        headers = {"X-Goog-Api-Key": self.api_key}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
    
    async def _get_daily_forecast(
        self, 
        latitude: float, 
        longitude: float,
        days: int = 7
    ) -> dict:
        """
        Получить дневной прогноз
        Эндпоинт: https://weather.googleapis.com/v1/forecast/days:lookup
        """
        self._check_api_key()
        url = f"{WEATHER_API_BASE}/forecast/days:lookup"
        
        params = {
            "key": self.api_key,
            "location.latitude": latitude,
            "location.longitude": longitude,
            "days": days,
        }
        headers = {"X-Goog-Api-Key": self.api_key}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
    
    def _parse_current_weather(self, data: dict) -> CurrentWeatherResponse:
        current = CurrentWeather(**data)
        return map_current(current)
    
    def _parse_hourly_forecast(self, data: dict, limit: int = 12) -> List[HourlyWeatherResponse]:
        hourly = HourlyWeather(**data)
        return [map_hour(hour) for hour in hourly.forecastHours[:limit]]
    
    def _parse_daily_forecast(self, data: dict, limit: int = 7) -> List[DailyWeatherResponse]:
        daily = DailyWeather(**data)
        return [map_day(day) for day in daily.forecastDays[:limit]]
    
    async def get_current_weather(self, city: str) -> CurrentWeatherResponse:
        
        coords = await get_coordinates(city)
        
        data = await self._get_current_conditions(
            latitude=coords["latitude"],
            longitude=coords["longitude"]
        )
        
        result = self._parse_current_weather(data)
        
        await self._save_weather_to_db(city, result, "current")
        
        return result
    
    async def get_hourly_12_hours(self, city: str) -> List[HourlyWeatherResponse]:
        
        coords = await get_coordinates(city)
        
        data = await self._get_hourly_forecast(
            latitude=coords["latitude"],
            longitude=coords["longitude"],
            hours=12
        )
        
        results = self._parse_hourly_forecast(data, limit=12)
        
        for result in results:
            await self._save_weather_to_db(city, result, "hourly")
        
        return results
    
    async def get_tomorrow_weather(self, city: str) -> DailyWeatherResponse:
        
        coords = await get_coordinates(city)
        
        data = await self._get_daily_forecast(
            latitude=coords["latitude"],
            longitude=coords["longitude"],
            days=2  
        )
        
        results = self._parse_daily_forecast(data, limit=2)
        
        if len(results) < 2:
            raise ValueError("Прогноз на завтра недоступен")
        
        result = results[1]
        
        await self._save_weather_to_db(city, result, "daily")
        
        return result
    
    async def get_3_days_forecast(self, city: str) -> List[DailyWeatherResponse]:
       
        coords = await get_coordinates(city)
        
        data = await self._get_daily_forecast(
            latitude=coords["latitude"],
            longitude=coords["longitude"],
            days=3
        )
        
        results = self._parse_daily_forecast(data, limit=3)
        
        for result in results:
            await self._save_weather_to_db(city, result, "daily")
        
        return results
    
    async def get_7_days_forecast(self, city: str) -> List[DailyWeatherResponse]:
        
        coords = await get_coordinates(city)
        
        data = await self._get_daily_forecast(
            latitude=coords["latitude"],
            longitude=coords["longitude"],
            days=7
        )
        
        results = self._parse_daily_forecast(data, limit=7)
        
        for result in results:
            await self._save_weather_to_db(city, result, "daily")
        
        return results
    
    async def _save_weather_to_db(
        self, 
        city: str, 
        weather_data: any, 
        forecast_type: str
    ) -> None:
        
        try:
            weather_dict = weather_data.dict() if hasattr(weather_data, 'dict') else weather_data
            
            weather_dict["city"] = city
            weather_dict["forecast_type"] = forecast_type
            
            await weather_repository.save_weather(weather_dict)
        except Exception as e:
            print(f"Ошибка сохранения погоды в БД: {e}")

weather_service = WeatherService()
