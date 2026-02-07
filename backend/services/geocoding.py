import httpx
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


async def get_coordinates(city: str):

    params = {
        "address": city,
        "key": GOOGLE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(GEOCODE_URL, params=params)

    data = response.json()

    if not data["results"]:
        return None

    location = data["results"][0]["geometry"]["location"]

    return {
        "latitude": location["lat"],
        "longitude": location["lng"]
    }
