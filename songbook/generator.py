import json
import pandas
import requests

from OutputFormatter import SongbookPDF
from song import Song


TITLE_MARKER = ' - '


def getSongData(ID):
    # TODO: Hide these keys somewhere
    head = {
        "Authorization": "Basic MmVhYTc2NTVkYzExZDFjNzFhODI5NmQ2ODkyMmE0MTAwOTkxZDQ2NmNjYzM1ZmJhOWZjOGMxZWQyZDI5MWUxZjphMmZhZWEyNDc1MmZhMTRjYzEzM2UzNjRlMmFjM2IzMzEyYmI5OWEzYWY0ZTEyNTEzODg2NzJjZTQ4ZTNlZmYy"
    }
    songReq = requests.get(
        'https://api.planningcenteronline.com/services/v2/songs/{0}/arrangements'.format(ID), headers=head)
    songObj = json.loads(songReq.text)

    return songObj["data"][0]["attributes"]["chord_chart"]


def main():
    # TODO: Clarify input method and retrieve as command line argument
    songsCSV = pandas.read_csv('sample/songs5.csv')

    # Retreive and ingest the song data
    songbook = {}
    for song in songsCSV.itertuples():
        ID = int(song[1])
        title_data = str(song[2]).split(TITLE_MARKER)

        # TODO: Get publishing company somehow
        songbook[ID] = Song(title_data[0], title_data[1], getSongData(ID))

    # Output the songdata
    book = SongbookPDF()
    for ID, song in songbook.items():
        book.print_song(song)
    book.output('songbook.pdf')

main()
