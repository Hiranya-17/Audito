# Audito database (MongoDB)

## Setup

1. Install the Python packages (Python 3.9+):
   ```
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` in the repo root. Leave the default local
   connection string, or paste the team's Atlas one (see below). `.env` is
   gitignored. Never commit it, because it holds the database password.
3. Start a database:
   - **Shared team database:** use the Atlas connection string in `.env`.
     Nothing to start.
   - **Local database on your laptop:** install Docker Desktop, then run
     `docker compose up -d` from the repo root. Stop it with `docker compose down`.
4. Create the collections and load the songs (run from the repo root):
   ```
   python -m database.setup_db
   python -m database.import_songs
   ```
   Both commands are safe to run again.

## Setting up the shared Atlas database (one person, once)

1. Create a free M0 cluster at https://cloud.mongodb.com.
2. Database Access: add a database user with a password.
3. Network Access: add your IP addresses, or `0.0.0.0/0` while developing.
4. Connect → Drivers → Python: copy the `mongodb+srv://...` string and send it
   to teammates privately, not through GitHub.
5. Run step 4 above once against Atlas.

## Collections

**songs**: one document per Spotify track, imported from `songs.csv`.
```
{ _id: "5SuOikwiRyPMVoIQDJUgSV",          // Spotify track_id
  track_name, album_name,
  artists: ["Gen Hoshino"], genres: ["acoustic", "j-pop"],
  popularity, duration_ms, explicit, key, mode, time_signature,
  danceability, energy, loudness, speechiness, acousticness,
  instrumentalness, liveness, valence, tempo }
```

**users**
```
{ _id: ObjectId, username, email, password_hash, created_at }
```
`username` and `email` are unique. Username uniqueness ignores case.

**reviews**: all reviews in one collection.
```
{ _id: ObjectId, user_id: ObjectId,   // users._id
  track_id: "5SuOikwiRyPMVoIQDJUgSV", // songs._id
  rating: 1-5, text: "optional", created_at, updated_at }
```
A user can review a song only once. Saving again edits that review.

## Using it from Python / Django

```python
from database import get_db
from database.reviews import save_review, reviews_for_song, rating_summary

db = get_db()
db.songs.find_one({"_id": track_id})
db.songs.find({"$text": {"$search": "blinding lights"}}).limit(10)  # search bar

save_review(user_id, track_id, 5, "Great song")
reviews_for_song(track_id)   # includes each reviewer's username
rating_summary(track_id)     # {"average": 4.5, "count": 2}
```

To give the recommendation code the same table it got from `songs.csv`:
```python
import pandas as pd
songs = pd.DataFrame(get_db().songs.find()).rename(columns={"_id": "track_id"})
```
Note that `artists` and `genres` are lists here, not `;`-separated strings.
