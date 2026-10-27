import pandas as pd

songs = pd.read_csv('songs.csv', usecols=['track_id', 'track_name', 'artists', 'album_name', 'track_genre', 'popularity'])
songs = songs.sort_values('popularity', ascending=False)
songs = songs.drop_duplicates(subset=['track_name', 'artists'])

songs = songs[songs['popularity'] >= 85]

print(songs.sample(frac=1).head(5)[['track_name', 'artists', 'album_name', 'track_genre', 'popularity']])