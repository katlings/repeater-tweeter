#!/usr/bin/env python3

import json
import os
import random

from apiclient.discovery import build
import tweepy

from play_detect import look_for_repeats


dir_path = os.path.dirname(os.path.realpath(__file__))


def authenticate():
    with open(os.path.join(dir_path, 'creds.json')) as f:
        creds = json.loads(f.read())

    return tweepy.Client(
        consumer_key=creds['tw_api_key'],
        consumer_secret=creds['tw_api_secret'],
        access_token=creds['tw_account_token'],
        access_token_secret=creds['tw_account_secret']
    )


def youtube_search_for_song(song, artist):
    with open(os.path.join(dir_path, 'creds.json')) as f:
        creds = json.loads(f.read())
    api_key = creds['yt_api_key']

    youtube = build('youtube', 'v3', developerKey=api_key)
    results = youtube.search().list(q=song + ' ' + artist, part='snippet', type='video').execute()
    top_result_id = results['items'][0]['id']['videoId']
    return f'https://www.youtube.com/watch?v={top_result_id}'


def tweet_about_song_repeat():
    client = authenticate()
    song, artists, plays, delta = look_for_repeats()

    with open(os.path.join(dir_path, 'last_song.txt')) as f:
        last_song = f.read().strip()

    if last_song != song and plays >= 5 and delta >= 3:
        rfactor = random.random()
        threshold = ((plays - 4) * 0.1)**2
        if rfactor > threshold:
            print(f"Not tweeting; random {rfactor} > {threshold} says not now!")
            return
        print(f"Tweeting; random {rfactor} < {threshold} says now!")
        url = youtube_search_for_song(song, artists)
        message = f"""Let's play "what song is stuck in Kat's head?"\n\nIt's {song} by {artists}! {url}"""

        client.create_tweet(text=message)

        with open(os.path.join(dir_path, 'last_song.txt'), 'w') as f:
            f.write(song)


if __name__ == '__main__':
    tweet_about_song_repeat()
