from typing import List, Optional
from datetime import datetime, timedelta
from bson import ObjectId

from configs.db import get_database


class WeatherRepository:
    
    def __init__(self):
        pass
        
    def _get_collection(self):
        db = get_database()
        if db is None:
            raise Exception("База данных не подключена")
        return db.weather
    
    async def save_weather(self, weather_data: dict) -> dict:
        
        collection = self._get_collection()
        
        weather_data["timestamp"] = datetime.utcnow()
        weather_data["created_at"] = datetime.utcnow()
        
        result = await collection.insert_one(weather_data)
        
        saved_weather = await collection.find_one({"_id": result.inserted_id})
        
        return self._convert_mongo_document(saved_weather)
    
    async def get_weather_by_city(
        self, 
        city: str, 
        limit: int = 1
    ) -> List[dict]:
        
        collection = self._get_collection()
        
        cursor = collection.find({"city": city}).sort("timestamp", -1).limit(limit)
        weather_list = await cursor.to_list(length=limit)
        
        return [self._convert_mongo_document(w) for w in weather_list]
    
    async def get_recent_weather(
        self, 
        city: str, 
        hours: int = 24
    ) -> List[dict]:
        
        collection = self._get_collection()
        
        since = datetime.utcnow() - timedelta(hours=hours)
        
        cursor = collection.find({
            "city": city,
            "timestamp": {"$gte": since}
        }).sort("timestamp", -1)
        
        weather_list = await cursor.to_list(length=None)
        
        return [self._convert_mongo_document(w) for w in weather_list]
    
    async def get_weather_by_id(self, weather_id: str) -> Optional[dict]:
        
        collection = self._get_collection()
        
        try:
            weather = await collection.find_one({"_id": ObjectId(weather_id)})
            if weather:
                return self._convert_mongo_document(weather)
        except Exception:
            return None
        
        return None
    
    async def delete_old_weather(self, days: int = 7) -> int:
        
        collection = self._get_collection()
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        result = await collection.delete_many({
            "timestamp": {"$lt": cutoff_date}
        })
        
        return result.deleted_count
    
    async def get_cities_with_data(self) -> List[str]:
        
        collection = self._get_collection()
        
        cities = await collection.distinct("city")
        return cities
    
    async def get_weather_statistics(self, city: str, days: int = 7) -> dict:
        
        collection = self._get_collection()
        
        since = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {
                "$match": {
                    "city": city,
                    "timestamp": {"$gte": since}
                }
            },
            {
                "$group": {
                    "_id": "$city",
                    "avg_temperature": {"$avg": "$temperature"},
                    "min_temperature": {"$min": "$temperature"},
                    "max_temperature": {"$max": "$temperature"},
                    "count": {"$sum": 1}
                }
            }
        ]
        
        cursor = collection.aggregate(pipeline)
        result = await cursor.to_list(length=1)
        
        if result:
            return {
                "city": city,
                "avg_temperature": result[0].get("avg_temperature"),
                "min_temperature": result[0].get("min_temperature"),
                "max_temperature": result[0].get("max_temperature"),
                "records_count": result[0].get("count"),
                "period_days": days
            }
        
        return {
            "city": city,
            "message": "Нет данных за указанный период"
        }
    
    def _convert_mongo_document(self, doc: dict) -> dict:
        
        if doc and "_id" in doc:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
        
        if "timestamp" in doc and isinstance(doc["timestamp"], datetime):
            doc["timestamp"] = doc["timestamp"].isoformat()
        
        if "created_at" in doc and isinstance(doc["created_at"], datetime):
            doc["created_at"] = doc["created_at"].isoformat()
        
        return doc

weather_repository = WeatherRepository()
