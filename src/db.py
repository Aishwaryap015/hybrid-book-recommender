from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")


db = client["book_recommender_db"]


users_collection = db["users"]

books_collection = db["books"]

ratings_collection = db["ratings"]