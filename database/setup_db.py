"""Creates the collections, their validation rules, and indexes.

Run once per database (safe to re-run after changing a rule):
    python -m database.setup_db
"""

from pymongo import ASCENDING, DESCENDING, TEXT, IndexModel
from pymongo.collation import Collation

from database.connection import get_db

# MongoDB rejects any insert/update that doesn't match these rules.
VALIDATORS = {
    # One document per Spotify track. _id is the Spotify track_id string.
    "songs": {
        "bsonType": "object",
        "required": ["_id", "track_name", "artists", "genres", "popularity"],
        "properties": {
            "_id": {"bsonType": "string"},
            "track_name": {"bsonType": "string"},
            "artists": {"bsonType": "array", "items": {"bsonType": "string"}},
            "album_name": {"bsonType": "string"},
            "genres": {"bsonType": "array", "items": {"bsonType": "string"}},
            "popularity": {"bsonType": "int", "minimum": 0, "maximum": 100},
        },
    },
    "users": {
        "bsonType": "object",
        "required": ["username", "email", "password_hash", "created_at"],
        "properties": {
            "username": {"bsonType": "string", "minLength": 1},
            "email": {"bsonType": "string", "pattern": "^[^@\\s]+@[^@\\s]+$"},
            # Hash only, never the plain password. Hashing happens in the auth code.
            "password_hash": {"bsonType": "string"},
            "created_at": {"bsonType": "date"},
        },
    },
    "reviews": {
        "bsonType": "object",
        "required": ["user_id", "track_id", "rating", "created_at", "updated_at"],
        "properties": {
            "user_id": {"bsonType": "objectId"},  # users._id
            "track_id": {"bsonType": "string"},   # songs._id
            "rating": {"bsonType": "int", "minimum": 1, "maximum": 5},
            "text": {"bsonType": "string"},       # optional written review
            "created_at": {"bsonType": "date"},
            "updated_at": {"bsonType": "date"},
        },
    },
}

INDEXES = {
    "songs": [
        # Powers the search bar: matches song title, artist, or album.
        IndexModel([("track_name", TEXT), ("artists", TEXT), ("album_name", TEXT)],
                   weights={"track_name": 10, "artists": 5, "album_name": 1},
                   name="song_search"),
        IndexModel([("popularity", DESCENDING)]),
        IndexModel([("genres", ASCENDING)]),
    ],
    "users": [
        # Case-insensitive: "Maya" and "maya" count as the same username.
        IndexModel([("username", ASCENDING)], unique=True,
                   collation=Collation(locale="en", strength=2)),
        IndexModel([("email", ASCENDING)], unique=True),
    ],
    "reviews": [
        # One review per user per song; saving again edits it.
        IndexModel([("user_id", ASCENDING), ("track_id", ASCENDING)], unique=True),
        IndexModel([("track_id", ASCENDING), ("updated_at", DESCENDING)]),  # Song Info page
        IndexModel([("user_id", ASCENDING), ("updated_at", DESCENDING)]),   # Profile page
    ],
}


def setup(db=None):
    db = db if db is not None else get_db()
    existing = set(db.list_collection_names())
    for name, schema in VALIDATORS.items():
        if name in existing:
            db.command("collMod", name, validator={"$jsonSchema": schema})
        else:
            db.create_collection(name, validator={"$jsonSchema": schema})
        db[name].create_indexes(INDEXES[name])
        print(f"  {name}: ok")


if __name__ == "__main__":
    print(f"Setting up database '{get_db().name}'...")
    setup()
    print("Done.")
