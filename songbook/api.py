import json
import requests


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

        for metadatum in response['data']:
            ID = int(metadatum['id'])
            metadata[ID] = metadatum

        # The API can only fetch 100 records at a time
        # Is there a next page to load?
        url = response['links']['next'] if 'next' in response['links'] else None

    return metadata
