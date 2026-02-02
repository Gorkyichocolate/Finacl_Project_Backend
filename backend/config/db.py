from pymongo import MongoClient
import os

def get_database():
    db_url = os.getenv("MONGODB_URL")
    
    if not db_url:
        raise ValueError("MONGODB_URL error")
    
    client = MongoClient(db_url)
    return client["final_project_db"]

if __name__ == "__main__":
    
    database = get_database()
    print("DB work:", database)