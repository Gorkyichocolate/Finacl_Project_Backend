import os
import certifi
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = (os.getenv("MONGODB_URL") or os.getenv("MONGODB_URI") or "").strip().strip('"').strip("'")
DATABASE_NAME = (os.getenv("DATABASE_NAME") or "").strip().strip('"').strip("'")

client: AsyncIOMotorClient = None
db = None


async def connect_to_mongodb():
    global client, db
    if not MONGO_URL:
        raise RuntimeError(
            "MONGODB_URL is not set. Add it in Render Environment Variables."
        )

    if not DATABASE_NAME:
        raise RuntimeError(
            "DATABASE_NAME is not set. Add it in Render Environment Variables."
        )

    mongo_options = {
        "serverSelectionTimeoutMS": 30000,
        "connectTimeoutMS": 20000,
        "socketTimeoutMS": 20000,
    }

    if MONGO_URL.startswith("mongodb+srv://"):
        mongo_options["tls"] = True
        mongo_options["tlsCAFile"] = certifi.where()

    last_error = None
    for attempt in range(1, 4):
        try:
            client = AsyncIOMotorClient(MONGO_URL, **mongo_options)
            await client.admin.command('ping')
            db = client[DATABASE_NAME]
            print(f"✅ Подключено к MongoDB: {DATABASE_NAME}")
            await create_indexes()
            return
        except ConnectionFailure as e:
            last_error = e
            print(f"Ошибка подключения к MongoDB (попытка {attempt}/3): {e}")
            if client:
                client.close()
            await asyncio.sleep(2 * attempt)
        except Exception as e:
            last_error = e
            print(f"Ошибка конфигурации/подключения MongoDB (попытка {attempt}/3): {e}")
            if client:
                client.close()
            await asyncio.sleep(2 * attempt)

    raise last_error


async def close_mongodb_connection():
    global client
    if client:
        client.close()
        print("Подключение к MongoDB закрыто")


async def create_indexes():
    await db.users.create_index("username", unique=True)
    await db.users.create_index("email", unique=True)
    
    await db.weather.create_index([("city", 1), ("timestamp", -1)])
    await db.weather.create_index("timestamp", expireAfterSeconds=86400)  
    print("Индексы MongoDB созданы")


def get_database():
    return db
