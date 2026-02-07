from fastapi import FastAPI, HTTPException, Depends, Response
from pydantic import BaseModel, EmailStr
from authx import AuthX, AuthXConfig
from services import geocoding


app = FastAPI()
print(geocoding.GOOGLE_API_KEY)
    

@app.get("/")
async def root():
    return {"message": "Hello, World!"}



@app.get("/coordinates")
async def coordinates(city: str):

    result = await geocoding.get_coordinates(city)

    if not result:
        raise HTTPException(404, "City not found")

    return result

@app.post("/login")
async def login(email: EmailStr, password: str):
    await logIn(email, password)
    return {"message": "Logged in successfully"}



@app.post("/register")
async def register(email: EmailStr, password: str):
    await signUp(email, password)
    return {"message": "User registered successfully"}
    
    
    
@app.get("/protected")
async def protected_route(user=Depends(AuthX())):
    return {"message": f"Hello, {user['email']}! This is a protected route."}



@app.post("/logout")
async def logout(response: Response, user=Depends(AuthX())):
    await logOut(response, user)
    return {"message": "Logged out successfully"}

