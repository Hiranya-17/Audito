from datetime import datetime, timezone
from bson import ObjectId
from Mongo import reviews_collection, songs_collection

def rate(user_id, track_id, rating):
  # 1. Verify the song exists in songs_collection
  song = songs_collection.find_one({"_id": track_id})
  if not song:
    raise ValueError(f"Track '{track_id}' not found in songs collection.")

  # 2. Ensure user_id is a valid MongoDB ObjectId (required by your schema)
  user_oid = ObjectId(user_id) if isinstance(user_id, str) else user_id
  now = datetime.now(timezone.utc)

  # 3. Save or update the review with all 5 required schema fields
  reviews_collection.update_one(
      {"user_id": user_oid, "track_id": track_id},
      {
          "$set": {"rating": rating, "updated_at": now},
          "$setOnInsert": {"created_at": now},
      },
      upsert=True,
  )

  # 4. Calculate the new average across all reviews for this track
  all_ratings = list(reviews_collection.find({"track_id": track_id}))
  num_reviews = len(all_ratings)
  total_score = sum(doc["rating"] for doc in all_ratings)
  average_rating = total_score / num_reviews

  # 5. Update the song document with the new rating stats
  songs_collection.update_one(
      {"_id": track_id},
      {
          "$set": {
              "average_rating": average_rating,
              "num_reviews": num_reviews,
              "updated_at": now,
          }
      },
  )

  return {
      "track_id": track_id,
      "track_name": song["track_name"],
      "average_rating": round(average_rating, 2),
      "num_reviews": num_reviews,
  }

def delete_rating(user_id, track_id):
  # 1. Verify the song exists in songs_collection
  song = songs_collection.find_one({"_id": track_id})
  if not song:
    raise ValueError(f"Track '{track_id}' not found in songs collection.")

  # 2. Convert user_id to ObjectId and delete their review
  user_oid = ObjectId(user_id) if isinstance(user_id, str) else user_id
  delete_result = reviews_collection.delete_one(
      {"user_id": user_oid, "track_id": track_id}
  )

  if delete_result.deleted_count == 0:
    raise ValueError("No rating found for this user and track.")

  # 3. Recalculate remaining reviews for this track
  all_ratings = list(reviews_collection.find({"track_id": track_id}))
  num_reviews = len(all_ratings)
  now = datetime.now(timezone.utc)

  if num_reviews > 0:
    total_score = sum(doc["rating"] for doc in all_ratings)
    average_rating = total_score / num_reviews

    songs_collection.update_one(
        {"_id": track_id},
        {
            "$set": {
                "average_rating": average_rating,
                "num_reviews": num_reviews,
                "updated_at": now,
            }
        },
    )
  else:
    # 4. If 0 reviews remain, reset stats cleanly so you don't divide by zero
    average_rating = 0.0
    songs_collection.update_one(
        {"_id": track_id},
        {
            "$set": {
                "average_rating": 0.0,
                "num_reviews": 0,
                "updated_at": now,
            }
        },
    )

  return {
      "track_id": track_id,
      "track_name": song["track_name"],
      "average_rating": round(average_rating, 2),
      "num_reviews": num_reviews,
  }
