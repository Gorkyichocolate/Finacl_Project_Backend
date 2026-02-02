from pymongo import MongoClient

def get_database():
    db= "MONGODB_URL"
    
    client = MongoClient(db)
    return client['final_project_db']

if __name__ == "__main__":
    database = get_database()
    print("Database connection established:", database)