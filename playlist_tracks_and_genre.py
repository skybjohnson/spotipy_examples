import spotipy
import spotipy.util as util
import csv

## Authentication
# Register an app with https://developer.spotify.com/dashboard/ and paste your Client ID and Client Secret on the line below
token = spotipy.SpotifyClientCredentials(client_id='xxxxx', client_secret='xxxxx')
cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)

## Playlist Track Data
# Purpose: Given a Spotify Playlist, get detailed track information for every song

# Get the first 100 (max) songs in the playlist
results = spotify.playlist_items('spotify:playlist:49y804nbrvW4a0ElnUWvoY', limit=100, offset=0)

# Store results in a tracks array
tracks = results['items']

# Continue paginating through until all results are returned
while results['next']:
    results = spotify.next(results)
    tracks.extend(results['items'])


## create a csv of track->genre mappings
with open('irish_tracks_genres.csv', mode='w') as genre_file:
    spotify_writer = csv.writer(genre_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    spotify_writer.writerow(['Track URI', 'Genre'])

    for item in (tracks):
        track = item['track']

        if "local" in track['uri']:
            continue

        artist = spotify.artist(track['artists'][0]['uri'])

        for g in (artist['genres']):
            # print(g)
            spotify_writer.writerow([track['uri'], g])



# Open and configure output csv
with open('irish_tracks.csv', mode='w') as track_file:
    spotify_writer = csv.writer(track_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Write csv headers
    spotify_writer.writerow(['Index','Track URI', 'Artist Name', 'Track Name', 'Release Date','Danceability','Energy','Key','Loudness','Mode','Speechiness','Accousticness','Instrumentalness','Liveness','Valence','Tempo','Duration MS','Time Signature','genres','popularity'])

    # index
    i = 0

    # for each track in the playlist, gather more information and write to csv
    for item in (tracks):
        i = i + 1
        track = item['track']

        # if the track is a local file, skip it
        if "local" in track['uri']:
            continue


        # Three more API calls to get more track-related information
        audio_features = spotify.audio_features(track['uri'])[0]
        release_date = spotify.track(track['uri'])['album']['release_date']
        artist = spotify.artist(track['artists'][0]['uri'])


        # popularity
        popularity = track['popularity']
        # print(popularity)
        # print("|".join(artist['genres']))

        # print to console for debugging
        print("   %d %32.32s %s %s" % (i, track['artists'][0]['name'], track['name'],release_date))

        # write to csv
        spotify_writer.writerow([i, track['uri'], track['artists'][0]['name'], track['name'], release_date
                                , audio_features['danceability']
                                , audio_features['energy']
                                , audio_features['key']
                                , audio_features['loudness']
                                , audio_features['mode']
                                , audio_features['speechiness']
                                , audio_features['acousticness']
                                , audio_features['instrumentalness']
                                , audio_features['liveness']
                                , audio_features['valence']
                                , audio_features['tempo']
                                , audio_features['duration_ms']
                                , audio_features['time_signature'],
                                 "|".join(artist['genres']),popularity]
                                )