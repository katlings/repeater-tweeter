import json
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth


dir_path = os.path.dirname(os.path.realpath(__file__))


def authenticate():
    try:
        with open(os.path.join(dir_path, 'creds.json')) as f:
            creds = json.loads(f.read())
    except FileNotFoundError:
        print('Could not find Spotify credentials; they should be in creds.json')

    spauth = SpotifyOAuth(client_id=creds['sp_client_id'], client_secret=creds['sp_client_secret'], scope='user-read-recently-played', redirect_uri='https://www.katlings.net/repeat')
    return spotipy.Spotify(auth_manager=spauth)


def look_for_repeats():
    sp = authenticate()
    resp = sp.current_user_recently_played(limit=50)
    last_played = resp['items']

    sorter = {}
    for play in last_played:
        track_uri = play['track']['uri']
        if track_uri not in sorter:
            sorter[track_uri] = 0
        sorter[track_uri] += 1

    sorted_plays = sorted(sorter.items(), key=lambda kv: -kv[1])
    track_uri, plays = sorted_plays[0]
    b_track_uri, b_plays = sorted_plays[1]
    track = sp.track(track_uri)
    track_name = track['name']
    track_artists = ' & '.join(artist['name'] for artist in track['artists'])

    print(f"Most played recent track for {sp.current_user()['display_name']}: {track_name} by {track_artists}, played {plays} times, {plays - b_plays} more than the next most played recent track {sp.track(b_track_uri)['name']}.")

    return track_name, track_artists, plays, plays - b_plays
