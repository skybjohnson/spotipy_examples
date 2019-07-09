import spotipy
import spotipy.util as util
import csv

## Authentication
# Register an app with https://developer.spotify.com/dashboard/ and paste your Client ID and Client Secret on the line below
token = util.oauth2.SpotifyClientCredentials(client_id='##', client_secret='##')
cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)

## Track Lookup
# Purpose: Given a list of artist-song pairs, use the Spotify API to return best matched track

# Open input and output csv files
with open('text_input.csv') as csv_file, open('text_uri.csv', mode='w') as output_file:

    # setup csv readers and writers
    csv_reader = csv.reader(csv_file, delimiter=',')
    spotify_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # write the first title row
    spotify_writer.writerow(['String','Uri'])

    # for each line in input file,
    for row in csv_reader:

        # use Search endpoint in Spotify API
        result = spotify.search(row, type="track")['tracks']['items']

        # if no results, show error
        if len(result) == 0:
            print('!!!!!! Did not find ',row)
            spotify_writer.writerow([row, "not found"])

        # otherwise record the results in the output file
        else:
            print('Found ',row,' -> ',result[0]['name'],' by ',result[0]['artists'][0]['name'])
            spotify_writer.writerow([row,result[0]['uri']])
    print("-- Complete --")
