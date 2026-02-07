from fastapi import FastAPI, HTTPException, Depends, Response
from pydantic import BaseModel, EmailStr
from authx import AuthX, AuthXConfig
from services import geocoding


app = FastAPI()
print(geocoding.GOOGLE_API_KEY)
    

    
@app.get("/coordinates")
async def coordinates(city: str):

    result = await geocoding.get_coordinates(city)

    if not result:
        raise HTTPException(404, "City not found")

    return result