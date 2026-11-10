import pandas as pd
from sklearn.preprocessing import MinMaxScaler

features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
info = ['track_id', 'track_name', 'artists', 'album_name', 'track_genre', 'popularity']

all_songs = pd.read_csv('songs.csv', usecols=info + features)

# fit on every row so any track_id can be looked up
scaler = MinMaxScaler().fit(all_songs[features])

# Pool of songs that can be returned 
pool = all_songs.sort_values('popularity', ascending=False)
pool = pool.drop_duplicates(subset=['track_name', 'artists']).reset_index(drop=True)
X = scaler.transform(pool[features])


def recommend(track_id=None, artist=None, genre=None, n=5, min_popularity=None, **targets):
    if min_popularity is None:
        min_popularity = 0 if artist else 50

    candidates = pool['popularity'] >= min_popularity   # which pool songs are allowed
    exclude_artists = set()
    target = None                          
    cols = list(range(len(features)))         # which features to compare 

    if genre:
        candidates &= pool['track_genre'] == genre

    # Only songs by this artist
    if artist:
        by_artist = pool['artists'].str.split(';').explode().eq(artist).groupby(level=0).any()
        if not by_artist.any():
            raise ValueError(f'No songs found for artist {artist}')
        candidates &= by_artist

    if track_id:
        rows = all_songs[all_songs['track_id'] == track_id]
        if rows.empty:
            raise ValueError(f'No song with track_id {track_id}')
        given = rows.iloc[0]
        target = scaler.transform(rows[features])[0]

        # don't return the given song itself
        candidates &= ~((pool['track_name'] == given['track_name']) & (pool['artists'] == given['artists']))

        # exclude the given song's artists 
        if not artist:
            exclude_artists = set(given['artists'].split(';'))

    elif targets:
        unknown = set(targets) - set(features)
        if unknown:
            raise ValueError(f'Unknown feature(s): {unknown}. Choose from {features}')
        cols = [features.index(f) for f in targets]
        # convert each value to 0-1 scale
        target = [(v - scaler.data_min_[c]) / scaler.data_range_[c]
            for c, v in zip(cols, targets.values())]

    # remove songs sharing any artist with the given song
    if exclude_artists:
        shares = pool['artists'].str.split(';').explode().isin(exclude_artists).groupby(level=0).any()
        candidates &= ~shares

    allowed = pool[candidates]

    # random songs from whatever is allowed
    if target is None:
        return allowed.sample(frac=1).head(n)['track_id'].tolist()

    # closest songs
    dist = ((X[:, cols] - target) ** 2).sum(axis=1) ** 0.5
    allowed = allowed.assign(distance=dist[candidates.values])
    return allowed.sort_values('distance').head(n)['track_id'].tolist()


# Examples
# print(recommend(n=2))                                     # random
# print(recommend(track_id='5SuOikwiRyPMVoIQDJUgSV'))        # related to specific song
# print(recommend(artist='Drake'))                     # related songs to artist
# print(recommend(energy=0.9))                              # same energy
# print(recommend(genre='jazz'))                       # same genre