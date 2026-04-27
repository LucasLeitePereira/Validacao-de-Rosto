from pymongo import MongoClient
from config import MONGO_CONFIG

def get_db_connection():
    """Establishes and returns a MongoDB client and collection."""
    try:
        client = MongoClient(MONGO_CONFIG["uri"])
        db = client[MONGO_CONFIG["db_name"]]
        collection = db[MONGO_CONFIG["collection_name"]]
        print("MongoDB connection established.")
        return client, collection
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None, None

def close_db_connection(client):
    """Closes the MongoDB connection."""
    if client:
        client.close()
    print("MongoDB connection closed.")
