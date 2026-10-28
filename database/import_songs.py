"""Loads songs.csv into the songs collection.

    python -m database.import_songs            # uses songs.csv in the repo root
    python -m database.import_songs other.csv

The CSV lists a song once per genre (114k rows, ~90k songs), so rows with the
same track_id are merged into one document with a list of genres. Safe to
re-run: existing songs are replaced, not duplicated.
"""

import csv
import sys

from pymongo import ReplaceOne

from database.connection import get_db

FEATURES = ["danceability", "energy", "loudness", "speechiness", "acousticness",
            "instrumentalness", "liveness", "valence", "tempo"]


def read_songs(path):
    songs = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            track_id = row["track_id"]
            popularity = int(row["popularity"])
            if track_id in songs:
                song = songs[track_id]
                if row["track_genre"] not in song["genres"]:
                    song["genres"].append(row["track_genre"])
                song["popularity"] = max(song["popularity"], popularity)
                continue

            song = {
                "_id": track_id,
                "track_name": row["track_name"],
                "artists": [a for a in row["artists"].split(";") if a],
                "album_name": row["album_name"],
                "genres": [row["track_genre"]],
                "popularity": popularity,
                "duration_ms": int(row["duration_ms"]),
                "explicit": row["explicit"] == "True",
                "key": int(row["key"]),
                "mode": int(row["mode"]),
                "time_signature": int(row["time_signature"]),
            }
            for feature in FEATURES:
                song[feature] = float(row[feature])
            songs[track_id] = song
    return list(songs.values())


def import_songs(path="songs.csv", db=None, batch_size=1000):
    db = db if db is not None else get_db()
    songs = read_songs(path)
    for start in range(0, len(songs), batch_size):
        batch = songs[start:start + batch_size]
        db.songs.bulk_write([ReplaceOne({"_id": s["_id"]}, s, upsert=True) for s in batch],
                            ordered=False)
    return len(songs)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "songs.csv"
    count = import_songs(path)
    print(f"Imported {count} songs into '{get_db().name}.songs'.")
