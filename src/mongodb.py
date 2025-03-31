from pymongo import MongoClient
from src.config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME

def getCollection():
    client = MongoClient(MONGO_URI)
    database = client[MONGO_DB_NAME]
    return database[MONGO_COLLECTION_NAME]

# Question 1
def getGetYearWithMostMovies():
    collection = getCollection()
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0] if result else None

# Question 2
def countMoviesAfter1999():
    collection = getCollection()
    return collection.count_documents({"year": {"$gt": 1999}})

# Question3
def averageVotes2007():
    collection = getCollection()
    pipeline = [
        {"$match": {"year": 2007}},
        {"$group": {"_id": None, "avg_votes": {"$avg": "$Votes"}}}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0]["avg_votes"] if result else None

#Question4
def getMoviesCountPerYear():
    collection = getCollection()
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    return list(collection.aggregate(pipeline))


#Question 5
def getAllGenres():
    collection = getCollection()
    pipeline = [
        {"$project": {"genre": {"$split": ["$genre", ","]}}},
        {"$unwind": "$genre"},
        {"$group": {"_id": "$genre"}},
        {"$sort": {"_id": 1}}
    ]
    result = list(collection.aggregate(pipeline))
    return [doc["_id"].strip() for doc in result]


# Question 6
def getHighestRevenueMovie():
    collection = getCollection()
    pipeline = [
        {"$match": {"Revenue (Millions)": {"$type": "double"}}},
        {"$sort": {"Revenue (Millions)": -1}},
        {"$limit": 1}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0] if result else None

# Question 7
def getDirectorsWithMoreThan5Movies():
    collection = getCollection()
    pipeline = [
        {"$group": {"_id": "$Director", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 5}}},
        {"$sort": {"count": -1}}
    ]
    return list(collection.aggregate(pipeline))