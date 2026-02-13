from typing import Optional
from datetime import datetime
from bson import ObjectId

from configs.db import get_database
from models.user_model import User, UserInDB


class UserRepository:
    
    def __init__(self):
        pass
        
    def _get_collection(self):
        db = get_database()
        if db is None:
            raise Exception("База данных не подключена")
        return db.users
    
    async def create_user(self, user_data: dict) -> UserInDB:
        collection = self._get_collection()
        
        user_data["created_at"] = datetime.utcnow()
        user_data["updated_at"] = datetime.utcnow()
        
        result = await collection.insert_one(user_data)
        
        created_user = await collection.find_one({"_id": result.inserted_id})
        
        return UserInDB(**self._convert_mongo_document(created_user))
    
    async def get_user_by_username(self, username: str) -> Optional[UserInDB]:
        
        collection = self._get_collection()
        user = await collection.find_one({"username": username})
        
        if user:
            return UserInDB(**self._convert_mongo_document(user))
        return None
    
    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        
        collection = self._get_collection()
        user = await collection.find_one({"email": email})
        
        if user:
            return UserInDB(**self._convert_mongo_document(user))
        return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        
        collection = self._get_collection()
        
        try:
            user = await collection.find_one({"_id": ObjectId(user_id)})
            if user:
                return UserInDB(**self._convert_mongo_document(user))
        except Exception:
            return None
        
        return None
    
    async def update_user(self, username: str, update_data: dict) -> Optional[UserInDB]:
        
        collection = self._get_collection()
        
        update_data["updated_at"] = datetime.utcnow()
        
        result = await collection.find_one_and_update(
            {"username": username},
            {"$set": update_data},
            return_document=True
        )
        
        if result:
            return UserInDB(**self._convert_mongo_document(result))
        return None
    
    async def delete_user(self, username: str) -> bool:
        
        collection = self._get_collection()
        result = await collection.delete_one({"username": username})
        return result.deleted_count > 0
    
    async def user_exists(self, username: str) -> bool:
        
        collection = self._get_collection()
        count = await collection.count_documents({"username": username})
        return count > 0
    
    async def email_exists(self, email: str) -> bool:
        
        collection = self._get_collection()
        count = await collection.count_documents({"email": email})
        return count > 0
    
    def _convert_mongo_document(self, doc: dict) -> dict:
        
        if doc and "_id" in doc:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
        
        doc.pop("created_at", None)
        doc.pop("updated_at", None)
        
        return doc


user_repository = UserRepository()
