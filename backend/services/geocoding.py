import httpx
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


async def get_coordinates(city: str):
    if not GOOGLE_API_KEY:
        raise ValueError("Google API key is not configured. Please set GOOGLE_API_KEY in .env file")

    params = {
        "address": city,
        "key": GOOGLE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(GEOCODE_URL, params=params)

    data = response.json()

    if data.get("status") != "OK":
        error_msg = data.get("error_message", data.get("status", "Unknown error"))
        raise ValueError(f"Geocoding API error: {error_msg}")

    if not data.get("results"):
        raise ValueError(f"City '{city}' not found")

    location = data["results"][0]["geometry"]["location"]

    return {
        "latitude": location["lat"],
        "longitude": location["lng"]
    }
