import re

CHORD_MARKER = r'\[([^]]*)\]'


# A single line of lyrics and chords in a song
class ChordLyric:

    # Assuming monospaced font to match width of chords and lyrics
    def __init__(self, line):
        # Correct PCO format should have n chords and n+1 lyric segments
        self.chords = re.findall(CHORD_MARKER, line)
        self.lyrics = re.sub(CHORD_MARKER, '\n', line).split('\n')


class Song:

    def __init__(self, key, title, chordpro):
        self.key = key
        self.title = title
        self.chord_chart = Song.chordpro_to_lines(chordpro)

    @staticmethod
    def chordpro_to_lines(chordpro):
        sections = chordpro.split('\n\n')

        chord_data = []
        for section in sections:
            lines = section.split('\n')
            part = lines[0]
            chord_lyrics = [ChordLyric(line) for line in lines[1:]]
            chord_data.append((part, chord_lyrics))

        return chord_data
