from __future__ import print_function
import csv

import api
import output
import song


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
            lyrics = row[15] if row[15] else api.get_song_lyrics(ID)
            if lyrics is None:
                print("Skipping song with no lyrics:", title)
                continue

            songs.append(song.Song(key, title, lyrics))

    return songs

def generate_pdf(infilename, outfilename):
    # Retreive and ingest the song data
    songs = import_csv(infilename)

    # Output the songdata
    book = output.SongbookPDF()
    for song in songs:
        book.print_song(song)
    book.output(outfilename)
