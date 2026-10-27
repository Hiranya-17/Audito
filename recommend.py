import pandas as pd
from sklearn.preprocessing import MinMaxScaler

features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
songs = pd.read_csv('songs.csv', usecols=['track_id', 'track_name', 'artists', 'album_name','track_genre', 'popularity'] + features)

# choose popular songs
songs = songs.sort_values('popularity', ascending=False)
songs = songs.drop_duplicates(subset=['track_name', 'artists'])

# known songs
songs = songs[songs['popularity'] >= 50].reset_index(drop=True)

# scale every feature for equal weighting
X = MinMaxScaler().fit_transform(songs[features])

# pick a random popular song
given_idx = songs[songs['popularity'] >= 70].sample(1).index[0]
given_song = songs.loc[given_idx]

print('Given song:', given_song['track_name'], '-', given_song['artists'] + "\n" + f"{given_song['track_genre']}")
print(given_song[features].to_string())

# smaller = more similar
songs['distance'] = ((X - X[given_idx]) ** 2).sum(axis=1) ** 0.5

# remove songs sharing any artist
given_artists = set(given_song['artists'].split(';'))
exploded = songs['artists'].str.split(';').explode()
shares_artist = exploded.isin(given_artists).groupby(level=0).any()
different_artist = ~shares_artist
similar = songs[different_artist].sort_values('distance').head(5)

print('\nSimilar songs:')
print(similar[['track_name', 'artists', 'track_genre', 'popularity', 'distance']])