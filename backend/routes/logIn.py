from authx import AuthX 
from fastapi import Depends, Response
from pydantic import EmailStr

async def logIn(email: EmailStr, password: str):
    ...