import re

CHORD_MARKER = r'\[([^]]*)\]'
VALID_PARTS = [
    'intro',
    'verse',
    'pre-chorus',
    'prechorus',
    'chorus',
    'bridge',
    'tag',
    'interlude',
    'instrumental',
    'outro'
]
IGNORE_LINES = [
    'column_break',
]

# A single line of lyrics and chords in a song


class ChordLyric:

    # Assuming monospaced font to match width of chords and lyrics
    def __init__(self, line):
        # Correct PCO format should have n chords and n+1 lyric segments
        self.chords = re.findall(CHORD_MARKER, line)
        self.lyrics = re.sub(CHORD_MARKER, '\n', line).split('\n')

    def is_empty(self):
        return not self.chords and self.lyrics == ['']


class Song:

    def __init__(self, pco_id, title, chordpro):
        self.pco_id = pco_id
        self.title = title
        self.chord_chart = Song.chordpro_to_lines(chordpro)
        self.key = None
        self.admin = None
        self.author = None
        self.copyright = None

    def get_lyric_lines(self):
        lines = 0
        for part, lyrics in self.chord_chart:
            lines += len(lyrics)
        return lines

    def get_chord_lines(self):
        lines = 0
        for party, chord_lyrics in self.chord_chart:
            for line in chord_lyrics:
                if line.chords:
                    lines += 1
        return lines

    @staticmethod
    def contains_label(line):
        for label in VALID_PARTS:
            if len(label) <= len(line) and label == line[:len(label)].lower():
                return True
        return False

    @staticmethod
    def chordpro_to_lines(chordpro):
        lines = chordpro.splitlines()

        chord_data = []
        label = ''
        chord_lyrics = []
        for line in lines:
            # replace curly single/double quotes
            line = line.replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", '"').replace(u"\u201d", '"')

            line = ''.join((c for c in line if ord(c) < 128))
            if Song.contains_label(line.strip()):
                if chord_lyrics or label:
                    chord_data.append((label, chord_lyrics))
                chord_lyrics = []
                label = line
            elif any(tag not in line.lower() for tag in IGNORE_LINES):
                chord_lyrics.append(ChordLyric(line))
        chord_data.append((label, chord_lyrics))

        return chord_data
