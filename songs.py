import pandas as pd

songs = pd.read_csv('songs.csv', usecols = ['track_id', 'track_name', 'artists', 'album_name', 'track_genre'])
print(songs.iloc[0:10])