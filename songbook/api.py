import json
import re
import requests

import song

# TODO: Hide these keys somewhere
API_KEY = 'Basic MmVhYTc2NTVkYzExZDFjNzFhODI5NmQ2ODkyMmE0MTAwOTkxZDQ2NmNjYzM1ZmJhOWZjOGMxZWQyZDI5MWUxZjphMmZhZWEyNDc1MmZhMTRjYzEzM2UzNjRlMmFjM2IzMzEyYmI5OWEzYWY0ZTEyNTEzODg2NzJjZTQ4ZTNlZmYy'


def get_song_lyrics(ID):
    req = requests.get(
            'https://api.planningcenteronline.com/services/v2/songs/{0}/arrangements'.format(ID),
            headers={'Authorization': API_KEY})
    song_obj = json.loads(req.text)

    return song_obj['data'][0]['attributes']['chord_chart']

def get_all_song_metadata():
    url = 'https://api.planningcenteronline.com/services/v2/songs?per_page=100'

    metadata = {}
    while url is not None:
        req = requests.get(url, headers={'Authorization': API_KEY})
        response = json.loads(req.text)

        for song in response['data']:
            ID = int(song['id'])
            metadata[ID] = song['attributes']

        # The API can only fetch 100 records at a time
        # Is there a next page to load?
        url = response['links']['next'] if 'next' in response['links'] else None

    return metadata

def get_all_band_songs():
    # only retrieve non-archived songs
    url = 'https://api.planningcenteronline.com/services/v2/songs?per_page=100&where[hidden]=false'

    songs = []
    while url is not None:
        req = requests.get(url, headers={'Authorization': API_KEY})
        response = json.loads(req.text)

        for song_data in response['data']:
            # only allow those with song codes assigned in title
            m = re.match('[A-Z][0-9]+.*', song_data['attributes']['title'])
            if not m:
                continue

            ID = int(song_data['id'])
            chords = get_song_lyrics(ID)

            song_obj = song.Song(ID, song_data['attributes']['title'], chords)
            song_obj.admin = song_data['attributes']['admin']
            song_obj.author = song_data['attributes']['author']
            song_obj.copyright = song_data['attributes']['copyright']
            songs.append(song_obj)

        # The API can only fetch 100 records at a time
        # Is there a next page to load?
        url = response['links']['next'] if 'next' in response['links'] else None

    return songs
