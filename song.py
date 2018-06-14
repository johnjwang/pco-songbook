import re

CHORD_MARKER = r'\[([^]]*)\]'


# A single line of lyrics and chords in a song
class ChordLyric:

    # Assuming monospaced font to match width of chords and lyrics
    def __init__(self, line):
        # Correct PCO format should have n chords and n+1 lyric segments
        self.chords = re.findall(CHORD_MARKER, line)
        self.lyrics = re.sub(CHORD_MARKER, '\n', line).split('\n')

    def getChords(self):
        return self.chords if len(self.chords) > 1 else []


class Song:

    def __init__(self, key, title, chordpro):
        self.key = key
        self.title = title
        self.chord_chart = Song.chordproToLines(chordpro)

    @staticmethod
    def chordproToLines(chordpro):
        sections = chordpro.split('\r\n\r\n')

        chord_data = {}
        for section in sections:
            lines = section.split('\r\n')
            part = lines[0]
            chord_lyrics = [ChordLyric(line) for line in lines[1:]]
            chord_data[part] = chord_lyrics

        return chord_data