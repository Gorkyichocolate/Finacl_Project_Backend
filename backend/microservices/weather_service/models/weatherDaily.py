from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CustomBaseModel(BaseModel):
    class Config:
        extra = "ignore"

class DisplayDate(CustomBaseModel):
    year: int
    month: int
    day: int


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


class SunEvents(CustomBaseModel):
    sunriseTime: datetime
    sunsetTime: datetime


class PartOfDayForecast(CustomBaseModel):
    weatherCondition: WeatherCondition
    relativeHumidity: Optional[int] = None
    uvIndex: Optional[int] = None
    precipitation: Optional[Precipitation] = None
    cloudCover: Optional[int] = None


class ForecastDay(CustomBaseModel):
    displayDate: DisplayDate
    daytimeForecast: PartOfDayForecast
    nighttimeForecast: PartOfDayForecast
    maxTemperature: Temperature
    minTemperature: Temperature
    sunEvents: SunEvents


class DailyWeather(CustomBaseModel):
    forecastDays: List[ForecastDay]


class DailyWeatherResponse(CustomBaseModel):
    date: str
    
    max_temp: float
    min_temp: float
    
    condition_day: str
    condition_night: str
    
    icon_day: str
    icon_night: str
    
    precipitation_probability: Optional[int]
    
    humidity_day: Optional[int]
    humidity_night: Optional[int]
    
    sunrise: datetime
    sunset: datetime


def build_icon_url(icon_base: str, is_day: bool) -> str:
    suffix = ".svg" if is_day else "_dark.svg"
    return f"{icon_base}{suffix}"

def map_day(day: ForecastDay) -> DailyWeatherResponse:
    return DailyWeatherResponse(
        date=f"{day.displayDate.year}-{day.displayDate.month}-{day.displayDate.day}",

        max_temp=day.maxTemperature.degrees,
        min_temp=day.minTemperature.degrees,

        condition_day=day.daytimeForecast.weatherCondition.description.text,
        condition_night=day.nighttimeForecast.weatherCondition.description.text,

        icon_day=build_icon_url(
            day.daytimeForecast.weatherCondition.iconBaseUri,
            True
        ),
        icon_night=build_icon_url(
            day.nighttimeForecast.weatherCondition.iconBaseUri,
            False
        ),

        precipitation_probability=(
            day.daytimeForecast.precipitation.probability.percent
            if day.daytimeForecast.precipitation else None
        ),

        humidity_day=day.daytimeForecast.relativeHumidity,
        humidity_night=day.nighttimeForecast.relativeHumidity,

        sunrise=day.sunEvents.sunriseTime,
        sunset=day.sunEvents.sunsetTime,
    )
