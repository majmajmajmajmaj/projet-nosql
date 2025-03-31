from pymongo import MongoClient
from src.config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME

def getCollection():
    client = MongoClient(MONGO_URI)
    database = client[MONGO_DB_NAME]
    return database[MONGO_COLLECTION_NAME]

def getGetYearWithMostMovies():
    collection = getCollection()
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0] if result else None