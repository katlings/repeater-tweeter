import json

from apiclient.discovery import build
import tweepy

from play_detect import look_for_repeats

def authenticate():
    with open('creds.json') as f:
        creds = json.loads(f.read())

    return tweepy.Client(
        consumer_key=creds['tw_api_key'],
        consumer_secret=creds['tw_api_secret'],
        access_token=creds['tw_account_token'],
        access_token_secret=creds['tw_account_secret']
    )


def youtube_search_for_song(song, artist):
    with open('creds.json') as f:
        creds = json.loads(f.read())
    api_key = creds['yt_api_key']

    youtube = build('youtube', 'v3', developerKey=api_key)
    results = youtube.search().list(q=song + ' ' + artist, part='snippet', type='video').execute()
    top_result_id = results['items'][0]['id']['videoId']
    return f'https://www.youtube.com/watch?v={top_result_id}'


def tweet_about_song_repeat():
    client = authenticate()
    song, artists, plays = look_for_repeats()

    if plays > 10:
        url = youtube_search_for_song(song, artists)
        message = f"""Let's play "what song is stuck in Kat's head?"\n\nIt's {song} by {artist}! {url}"""

        client.create_tweet(text=message)
