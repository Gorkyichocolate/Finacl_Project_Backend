from pydantic import BaseModel
from typing import Optional
from datetime import datetime


def build_icon_url(icon_base: str, is_day: bool) -> str:
    suffix = ".svg" if is_day else "_dark.svg"
    return f"{icon_base}{suffix}"

class CustomBaseModel(BaseModel):
    class Config:
        extra = "ignore"


class Description(CustomBaseModel):
    text: str


class WeatherCondition(CustomBaseModel):
    iconBaseUri: str
    description: Description
    type: str


class Temperature(CustomBaseModel):
    degrees: float


class Probability(CustomBaseModel):
    percent: int


class Precipitation(CustomBaseModel):
    probability: Probability


class Direction(CustomBaseModel):
    degrees: int
    cardinal: str


class WindSpeed(CustomBaseModel):
    value: float


class Wind(CustomBaseModel):
    direction: Direction
    speed: WindSpeed


class AirPressure(CustomBaseModel):
    meanSeaLevelMillibars: float


class SunEvents(CustomBaseModel):
    sunriseTime: datetime
    sunsetTime: datetime


class CurrentWeather(CustomBaseModel):
    currentTime: datetime
    isDaytime: bool
    
    weatherCondition: WeatherCondition
    
    temperature: Temperature
    feelsLikeTemperature: Optional[Temperature] = None
    
    precipitation: Optional[Precipitation] = None
    wind: Optional[Wind] = None
    relativeHumidity: Optional[int] = None
    airPressure: Optional[AirPressure] = None
    
    sunEvents: Optional[SunEvents] = None

class CurrentWeatherResponse(CustomBaseModel):
    temperature: float
    feels_like: Optional[float]
    condition: str
    condition_type: Optional[str]
    is_day: bool
    icon: str
    precipitation_probability: Optional[int]
    humidity: Optional[int]
    pressure: Optional[float]
    wind_direction: Optional[str]
    wind_speed: Optional[float]
    sunrise: Optional[datetime]
    sunset: Optional[datetime]
    
    
def map_current(weather: CurrentWeather) -> CurrentWeatherResponse:
    return CurrentWeatherResponse(
        temperature=weather.temperature.degrees,
        feels_like=(
            weather.feelsLikeTemperature.degrees
            if weather.feelsLikeTemperature else None
        ),
        condition=weather.weatherCondition.description.text,
        condition_type=weather.weatherCondition.type,
        is_day=weather.isDaytime,
        precipitation_probability=(
            weather.precipitation.probability.percent
            if weather.precipitation else None
        ),
        humidity=weather.relativeHumidity,
        pressure=(
            weather.airPressure.meanSeaLevelMillibars
            if weather.airPressure else None
        ),
        wind_direction=(
            weather.wind.direction.cardinal
            if weather.wind else None
        ),
        wind_speed=(
            weather.wind.speed.value
            if weather.wind else None
        ),
        sunrise=weather.sunEvents.sunriseTime if weather.sunEvents else None,
        sunset=weather.sunEvents.sunsetTime if weather.sunEvents else None,
        icon=build_icon_url(
            weather.weatherCondition.iconBaseUri,
            weather.isDaytime
        ), 
)
