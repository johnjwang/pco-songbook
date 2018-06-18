import csv
import json
import requests

import output
from song import Song


def get_song_data(ID):
    # TODO: Hide these keys somewhere
    head = {
        "Authorization": "Basic MmVhYTc2NTVkYzExZDFjNzFhODI5NmQ2ODkyMmE0MTAwOTkxZDQ2NmNjYzM1ZmJhOWZjOGMxZWQyZDI5MWUxZjphMmZhZWEyNDc1MmZhMTRjYzEzM2UzNjRlMmFjM2IzMzEyYmI5OWEzYWY0ZTEyNTEzODg2NzJjZTQ4ZTNlZmYy"
    }
    song_req = requests.get(
        'https://api.planningcenteronline.com/services/v2/songs/{0}/arrangements'.format(ID), headers=head)
    song_obj = json.loads(song_req.text)

    return song_obj["data"][0]["attributes"]["chord_chart"]

def import_csv(infilename):
    songs = []

    with open(infilename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile)

        # Skip first row header
        csvreader.next()

        for row in csvreader:
            ID = int(row[0])
            key = None
            title = row[1]
            lyrics = row[15] if row[15] else get_song_data(ID)

            songs.append(Song(key, title, lyrics))

    return songs

def generate_pdf(infilename, outfilename):
    # Retreive and ingest the song data
    songs = import_csv(infilename)

    # Output the songdata
    book = output.SongbookPDF()
    for song in songs:
        book.print_song(song)
    book.output(outfilename)
