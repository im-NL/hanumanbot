import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.request
import re
from .auth import client, secret

client_credentials_manager = SpotifyClientCredentials(client_id=client, client_secret=secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlist_names(url):
    results = spotify.playlist_tracks(url)
    result = []
    for i in range(len(results['items'])):
        result.append(results['items'][i]['track']['name'] + ' ' + results['items'][i]['track']['artists'][0]['name'])    
    
    return result


def get_playlist_tracks(url):
    results = spotify.playlist_tracks(url)
    result = []
    links = []
    for i in range(len(results['items'])):
        result.append(results['items'][i]['track']['name'] + ' ' + results['items'][i]['track']['artists'][0]['name'])

    for song in result:
        song = song.encode('utf-8')
        print(song)
        html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(song).replace(' ', '+'))
        all_links = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = (f'https://www.youtube.com/watch?v={all_links[0]}')
        links.append(url)
    return links

def get_spotify_track(url):
    song = spotify.track(url)
    song = f"{song['name']} {song['artists'][0]['name']}"
    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + song.replace(' ', '+'))
    links = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = (f'https://www.youtube.com/watch?v={links[0]}')
    
    return url
