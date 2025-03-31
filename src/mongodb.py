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
        {"$match": {"Revenue (Millions)": {"$type": "double"} }},
        {"$sort": {"Revenue (Millions)": -1}},
        {"$limit": 1
         }
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


# Question 8 

def getGenreWithHighestAvgRevenue():
    collection = getCollection()
    pipeline = [
        {"$match": {"Revenue (Millions)": {"$type": "double"}}},
        {"$project": {
            "genre": {"$split": ["$genre", ","]},
            "Revenue (Millions)": 1
        }},
        {"$unwind": "$genre"},
        {"$group": {
            "_id": {"$trim": {"input": "$genre"}},
            "avg_revenue": {"$avg": "$Revenue (Millions)"}
        }},
        {"$sort": {"avg_revenue": -1
                   }},
        {"$limit": 1}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0] if result else None

#Question 9

def getTop3RatedMoviesByDecade():
    collection = getCollection()
    pipeline = [
        {"$match": {"rating": {"$exists": True, "$ne": "unrated"}, "year": {"$type": "int"}}},
        {"$project": {
            "title": 1,
            "rating": 1,
            "year": 1,
            "decade": {"$subtract": ["$year", {"$mod": ["$year", 10]}]}
        }},
        {"$sort": {"decade": 1, "rating": -1}},
        {"$group": {
            "_id": "$decade",
            "topMovies": {
                "$push": {
                    "title": "$title",
                    "rating": "$rating",
                    "year": "$year"
                }
            }
        }},
        {"$project": {
            "decade": "$_id",
            "topMovies": {"$slice": ["$topMovies", 3]},
            "_id": 0
        }},
        {"$sort": {
            "decade": 1
            }
            }
    ]
    return list(collection.aggregate(pipeline))


# QUestion 10

def getLongestMovieByGenre():
    collection = getCollection()
    pipeline = [
        {"$match": {"Runtime (Minutes)": {"$type": "int"}}},
        {"$project": {
            "title": 1,
            "Runtime (Minutes)": 1,
            "genre": {"$split": ["$genre", ","]}
        }},
        {"$unwind": "$genre"},
        {"$set": {"genre": {"$trim": {"input": "$genre"}}}},
        {"$sort": {"Runtime (Minutes)": -1}},
        {"$group": {
            "_id": "$genre",
            "title": {"$first": "$title"},
            "runtime": {"$first": "$Runtime (Minutes)"}
        }},
        {"$sort": {"_id": 1}}
    ]
    return list(collection.aggregate(pipeline))

#Question 11

def getHighRatedAndProfitableMovies():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    view = db["highRatedAndProfitableMovies"]
    return list(view.find())

#Question 12

def getRuntimesAndRevenues():
    collection = getCollection()
    return list(collection.find(
        {
        "Runtime (Minutes)": {"$type": "int"},
        "Revenue (Millions)": {"$type": "double"}
    }, {
        "Runtime (Minutes)": 1,
        "Revenue (Millions)": 1,
        "_id": 0
    }))


#question 13
def getAverageRuntimeByDecade():
    collection = getCollection()
    pipeline = [
        {"$match": {
            "Runtime (Minutes)": {"$type": "int"},
            "year": {"$type": "int"}
        }},
        {"$project": {
            "decade": {"$subtract": ["$year", {"$mod": ["$year", 10]}]},
            "Runtime (Minutes)": 1
        }},
        {"$group": 
         {
            "_id": "$decade",
            "average_runtime": {"$avg": "$Runtime (Minutes)"}
        }},
        {"$sort": {"_id": 1}}
    ]
    return list(collection.aggregate(pipeline))
