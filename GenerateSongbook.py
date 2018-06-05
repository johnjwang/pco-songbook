import json
import pandas
import requests
import re

from OutputFormatter import Songbook


TITLE_MARKER = ' - '
CHORD_MARKER = r'\[([^]]*)\]'


def getSongData(ID):
    # TODO: Hide these keys somewhere
    head = {
        "Authorization": "Basic MmVhYTc2NTVkYzExZDFjNzFhODI5NmQ2ODkyMmE0MTAwOTkxZDQ2NmNjYzM1ZmJhOWZjOGMxZWQyZDI5MWUxZjphMmZhZWEyNDc1MmZhMTRjYzEzM2UzNjRlMmFjM2IzMzEyYmI5OWEzYWY0ZTEyNTEzODg2NzJjZTQ4ZTNlZmYy"
    }
    songReq = requests.get(
        'https://api.planningcenteronline.com/services/v2/songs/{0}/arrangements'.format(ID), headers=head)
    songObj = json.loads(songReq.text)

    return songObj["data"][0]["attributes"]["chord_chart"]


# A single line of lyrics and chords in a song
class ChordLyric:

    # Assuming monospaced font to match width of chords and lyrics
    def __init__(self, line):
        # Correct PCO format should have n chords and n+1 lyric segments
        self.chords = re.findall(CHORD_MARKER, line)
        lyr_seg = re.sub(CHORD_MARKER, '\n', line).split('\n')

        cho_seg = [' ' * len(lyr_seg[0])]
        for i in range(1, len(lyr_seg)):
            if len(lyr_seg[i]) < len(self.chords[i - 1]):
                lyr_seg[i] += ' ' * (len(self.chords[i - 1]) - len(lyr_seg[i]))
                cho_seg.append(self.chords[i - 1])
            else:
                whitespace = ' ' * (len(lyr_seg[i]) - len(self.chords[i - 1]))
                cho_seg.append(self.chords[i - 1] + whitespace)

        self.chord_segments = cho_seg
        self.lyric_segments = lyr_seg

    def getTwoline(self):
        if not self.chords:
            return ''.join(self.lyric_segments)
        else:
            return ''.join(self.chord_segments) + '\n' + ''.join(self.lyric_segments)


# Takes in chord_chart format from PCO and creates array of Lines
def chordproToTwoline(chordpro):
    sections = chordpro.split('\r\n\r\n')

    chord_data = {}
    for section in sections:
        lines = section.split('\r\n')
        part = lines[0]
        chord_lyrics = [ChordLyric(line) for line in lines[1:]]
        chord_data[part] = chord_lyrics

    return chord_data


def main():
    # TODO: Clarify input method and retrieve as command line argument
    songsCSV = pandas.read_csv('sample/songs5.csv')

    # Retreive and ingest the song data
    songbook = {}
    for song in songsCSV.itertuples():
        ID = int(song[1])
        title_data = str(song[2]).split(TITLE_MARKER)

        # TODO: Get publishing company somehow
        songbook[ID] = {
            'key': title_data[0],
            'title': title_data[1],
            'chord_chart': chordproToTwoline(getSongData(ID))
        }

    # Output the songdata
    book = Songbook()
    for ID, song in songbook.items():
        book.print_song(song['key'], song['title'], song['chord_chart'])
    book.output('songbook.pdf')

main()
