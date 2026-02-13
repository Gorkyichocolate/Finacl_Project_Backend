from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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
    direction: Optional[Direction] = None
    speed: Optional[WindSpeed] = None


class Interval(CustomBaseModel):
    startTime: datetime


class ForecastHour(CustomBaseModel):
    interval: Interval
    isDaytime: bool

    weatherCondition: WeatherCondition

    temperature: Temperature
    feelsLikeTemperature: Optional[Temperature] = None

    relativeHumidity: Optional[int] = None
    precipitation: Optional[Precipitation] = None

    wind: Optional[Wind] = None


class HourlyWeather(CustomBaseModel):
    forecastHours: List[ForecastHour]


class HourlyWeatherResponse(CustomBaseModel):
    time: datetime
    temperature: float
    feels_like: Optional[float]

    condition: str
    icon: str

    precipitation_probability: Optional[int]

    wind_speed: Optional[float]
    wind_direction: Optional[str]

    humidity: Optional[int]

    is_day: bool


def build_icon_url(icon_base: str, is_day: bool) -> str:
    suffix = ".svg" if is_day else "_dark.svg"
    return f"{icon_base}{suffix}"


def map_hour(hour: ForecastHour) -> HourlyWeatherResponse:
    return HourlyWeatherResponse(
        time=hour.interval.startTime,
        temperature=hour.temperature.degrees,
        feels_like=(
            hour.feelsLikeTemperature.degrees
            if hour.feelsLikeTemperature else None
        ),
        condition=hour.weatherCondition.description.text,
        icon=build_icon_url(
            hour.weatherCondition.iconBaseUri,
            hour.isDaytime
        ),
        precipitation_probability=(
            hour.precipitation.probability.percent
            if hour.precipitation else None
        ),
        wind_speed=(
            hour.wind.speed.value
            if hour.wind and hour.wind.speed else None
        ),
        wind_direction=(
            hour.wind.direction.cardinal
            if hour.wind and hour.wind.direction else None
        ),
        humidity=hour.relativeHumidity,
        is_day=hour.isDaytime,
    )
