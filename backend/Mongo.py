import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
Connection_String = os.getenv("Mongo_uri")

if not Connection_String:
  raise ValueError("Mongo URI not found. Check .env file.")

client = MongoClient(Connection_String, tlsCAFile=certifi.where())
db = client["audito"]
reviews_collection = db["reviews"]
songs_collection = db["songs"]
users_collection = db["users"]