import os
import dotenv
dotenv.load_dotenv()

Api = os.getenv("WEATHER_API_KEY")

current_weather_api_url = f"https://weather.googleapis.com/v1/currentConditions:lookup?key={Api}&location.latitude={Latitude}&location.longitude={Longitude}"

daily_weather_api_url = f"https://weather.googleapis.com/v1/forecast/days:lookup?key={Api}&location.latitude={Latitude}&location.longitude={Longitude}&days={days}"

hourly_weather_api_url = f"https://weather.googleapis.com/v1/forecast/hours:lookup?key={Api}&location.latitude={Latitude}&location.longitude={Longitude}&hours={hours}"
