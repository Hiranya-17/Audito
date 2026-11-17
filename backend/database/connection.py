import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()  # reads MONGODB_URI / MONGODB_DB from the .env file in the repo root

_client = None


def get_db():
    """Return the Audito database. The connection is created once and reused."""
    global _client
    if _client is None:
        uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
        _client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    return _client[os.environ.get("MONGODB_DB", "audito")]
