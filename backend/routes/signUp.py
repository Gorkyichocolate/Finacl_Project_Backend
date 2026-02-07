from authx import AuthX 
from fastapi import Depends, Response
from pydantic import EmailStr

async def signUp(email: EmailStr, password: str):
    ... 
    