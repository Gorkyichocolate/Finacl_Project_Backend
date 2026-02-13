import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client: AsyncIOMotorClient = None
db = None


async def connect_to_mongodb():
    global client, db
    try:
        client = AsyncIOMotorClient(MONGO_URL)
        await client.admin.command('ping')
        db = client[DATABASE_NAME]
        print(f"✅ Подключено к MongoDB: {DATABASE_NAME}")
        
        await create_indexes()
    except ConnectionFailure as e:
        print(f"Ошибка подключения к MongoDB: {e}")
        raise


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
