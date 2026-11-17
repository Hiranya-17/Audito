"""Review functions the Django views can call."""

from datetime import datetime, timezone

from bson import ObjectId
from pymongo import DESCENDING, ReturnDocument

from database.connection import get_db


def save_review(user_id, track_id, rating, text=None, db=None):
    """Write a review, or update it if this user already reviewed this song."""
    db = db if db is not None else get_db()
    if not 1 <= int(rating) <= 5:
        raise ValueError("Rating must be between 1 and 5")
    user_id = ObjectId(user_id)
    if db.users.count_documents({"_id": user_id}, limit=1) == 0:
        raise ValueError("Unknown user")
    if db.songs.count_documents({"_id": track_id}, limit=1) == 0:
        raise ValueError("Unknown song")

    now = datetime.now(timezone.utc)
    fields = {"rating": int(rating), "updated_at": now}
    if text is not None:
        fields["text"] = text
    return db.reviews.find_one_and_update(
        {"user_id": user_id, "track_id": track_id},
        {"$set": fields, "$setOnInsert": {"created_at": now}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )


def reviews_for_song(track_id, limit=50, db=None):
    """Newest reviews of one song, each with the reviewer's username attached."""
    db = db if db is not None else get_db()
    return list(db.reviews.aggregate([
        {"$match": {"track_id": track_id}},
        {"$sort": {"updated_at": DESCENDING}},
        {"$limit": limit},
        {"$lookup": {"from": "users", "localField": "user_id",
                     "foreignField": "_id", "as": "user"}},
        {"$set": {"username": {"$first": "$user.username"}}},
        {"$unset": "user"},
    ]))


def reviews_by_user(user_id, limit=50, db=None):
    """A user's newest reviews (Profile page -> Recent Reviews)."""
    db = db if db is not None else get_db()
    cursor = db.reviews.find({"user_id": ObjectId(user_id)})
    return list(cursor.sort("updated_at", DESCENDING).limit(limit))


def rating_summary(track_id, db=None):
    """{'average': 4.2, 'count': 17} for a song, or None if nobody rated it."""
    db = db if db is not None else get_db()
    result = list(db.reviews.aggregate([
        {"$match": {"track_id": track_id}},
        {"$group": {"_id": None, "average": {"$avg": "$rating"}, "count": {"$sum": 1}}},
    ]))
    if not result:
        return None
    return {"average": round(result[0]["average"], 2), "count": result[0]["count"]}


def delete_review(user_id, track_id, db=None):
    db = db if db is not None else get_db()
    return db.reviews.delete_one({"user_id": ObjectId(user_id), "track_id": track_id}).deleted_count == 1
