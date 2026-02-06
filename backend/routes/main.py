from fastapi import FastAPI
from database import db

app = FastAPI()


@app.get("/users")
async def get_users():
    users = []
    
    async for user in db.users.find():
        user["_id"] = str(user["_id"])
        users.append(user)

    return users
