from authx import AuthX 
from fastapi import Depends, Response

async def logOut(response: Response, user=Depends(AuthX())):
    ... 