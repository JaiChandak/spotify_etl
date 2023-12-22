import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import json
import s3fs
from datetime import datetime

# My API keys are saved and brough over from a file called consts.py
from consts import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

# Connect to spotify by creating an API object
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

def run_spotify_etl():
    # Search for an artist and get the artist's uri
    artist_name = input("Which artist do you want to search?: ")
    results = sp.search(q=artist_name, type='artist')

    track_list = []

    if results['artists']['items']:
        artist = results['artists']['items'][0]
        artist_uri = artist['uri']
        # Use artist's uri to pull all their albums
        album_search = sp.artist_albums(artist_uri, album_type='album')

        for album in album_search['items']:
            album_uri = album['uri']

            # Get tracks for the current album
            tracks = sp.album_tracks(album_uri)
            for track in tracks['items']:
                artist_tracks = {"Track Name": track['name'],
                                "Album": album['name'],
                                "Track Number": track['track_number'],
                                "Release date": album['release_date']
                }
                track_list.append(artist_tracks)

    # Convert results to a dataframe and save to a csv file
    df = pd.DataFrame(track_list)
    df.to_csv("Artist_tracks.csv")