import re

CHORD_MARKER = r'\[([^]]*)\]'
VALID_PARTS = [
    'intro',
    'verse',
    'pre-chorus',
    'chorus',
    'bridge',
    'tag',
    'interlude',
    'instrumental'
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
        for chord_data in self.chord_chart:
            lines += len(chord_data[1])
        return lines

    def get_chord_lines(self):
        lines = 0
        for chord_data in self.chord_chart:
            for line in chord_data[1]:
                if line.chords:
                    lines += 1
        return lines

    @staticmethod
    def chordpro_to_lines(chordpro):
        lines = chordpro.splitlines()

        chord_data = []
        label = ''
        chord_lyrics = []
        for i in range(len(lines)):
            if lines[i].isspace() or not lines[i]:
                continue

            if lines[i].split(' ')[0].lower() in VALID_PARTS:
                if label:
                    chord_data.append((label, chord_lyrics))
                    chord_lyrics = []
                label = lines[i]
            elif any(tag not in lines[i].lower() for tag in IGNORE_LINES):
                chord_lyrics.append(ChordLyric(lines[i]))
        chord_data.append((label, chord_lyrics))

        return chord_data
