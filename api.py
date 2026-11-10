from flask import Flask, jsonify
from recommend import recommend, all_songs

app = Flask(__name__)


@app.get("/api/recommendations")
def get_recommendations():
    track_ids = recommend(n=6)
    results = []

    for track_id in track_ids:
        song = all_songs[
            all_songs["track_id"] == track_id
        ].iloc[0]

        results.append({
            "id": str(track_id),
            "title": str(song["track_name"]),
            "artist": str(song["artists"]),
            "genre": str(song["track_genre"]),
            "popularity": int(song["popularity"]),
            "rating": None
        })

    return jsonify(results)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)