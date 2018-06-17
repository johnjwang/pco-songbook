import json
import pandas
import requests

import output
from song import Song


TITLE_MARKER = ' - '


def get_song_data(ID):
    # TODO: Hide these keys somewhere
    head = {
        "Authorization": "Basic MmVhYTc2NTVkYzExZDFjNzFhODI5NmQ2ODkyMmE0MTAwOTkxZDQ2NmNjYzM1ZmJhOWZjOGMxZWQyZDI5MWUxZjphMmZhZWEyNDc1MmZhMTRjYzEzM2UzNjRlMmFjM2IzMzEyYmI5OWEzYWY0ZTEyNTEzODg2NzJjZTQ4ZTNlZmYy"
    }
    song_req = requests.get(
        'https://api.planningcenteronline.com/services/v2/songs/{0}/arrangements'.format(ID), headers=head)
    song_obj = json.loads(song_req.text)

    return song_obj["data"][0]["attributes"]["chord_chart"]

def generate_pdf(infilename, outfilename):
    songs_csv = pandas.read_csv(infilename)

    # Retreive and ingest the song data
    songs = []
    for song in songs_csv.itertuples():
        ID = int(song[1])
        title_data = str(song[2]).split(TITLE_MARKER)

        # TODO: Get publishing company somehow
        songs.append(Song(title_data[0], title_data[1], get_song_data(ID)))

    # Output the songdata
    book = output.SongbookPDF()
    for song in songs:
        book.print_song(song)
    book.output(outfilename)
