from __future__ import print_function
import csv
import os
import pickle

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
            title = row[1]
            lyrics = row[15] if row[15] else api.get_song_lyrics(ID)
            if lyrics is None:
                print('Skipping song with no lyrics:', title)
                continue

            songs.append(song.Song(ID, title, lyrics))

    return songs

def generate_from_csv(infilename, outfilename):
    # Retrieve and ingest the song data
    print('Importing songs from CSV...')
    songs = import_csv(infilename)

    # Attach metadata to songs
    print('Importing song metadata...')
    metadata = api.get_all_song_metadata()
    for song in songs:
        if song.pco_id not in metadata:
            print('Song metadata not found:', song.title)
            continue
        datum = metadata[song.pco_id]
        song.admin = datum['admin']
        song.author = datum['author']
        song.copyright = datum['copyright']

    # Output the songdata
    print('Generating output...')
    book = output.SongbookPDF()
    book.print_songbook(songs)
    book.output(outfilename)
    print('Wrote output to', outfilename)

def generate_from_api(outfilename):
    cache_path = 'songs.cache'
    if os.path.exists(cache_path):
        print('Loading all non-archived, code-assigned songs from cache...')
        songs = pickle.load(open(cache_path, 'rb'))
    else:
        print('Importing all non-archived, code-assigned songs from API...')
        songs = api.get_all_band_songs()
        pickle.dump(songs, open(cache_path, 'wb'))
        print('Cached downloaded songs in <{}>.'.format(cache_path))

    songs = sorted(songs, key=lambda s: s.title)

    print('Generating output...')
    book = output.SongbookPDF()
    book.print_songbook_by_letter(songs)
    book.output(outfilename)
    print('Wrote output to', outfilename)
