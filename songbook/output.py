import fpdf
import layout

TITLE_SIZE = 12
TITLE_FONT = 'Arial'
CHORD_SIZE = 8
CHORD_FONT = 'Arial'
LYRIC_SIZE = 11
LYRIC_FONT = 'Arial'
FOOTER_SIZE = 8
FOOTER_FONT = 'Arial'

MARGIN_SIZE = 22.6772
INNER_BORDER = 11.3386
INDENT_SIZE = 8.50394
INDENT_PARTS = [
    'pre-chorus',
    'chorus',
    'bridge',
]


class SongbookPDF(fpdf.FPDF):

    def __init__(self):
        super(SongbookPDF, self).__init__(unit='pt')

        self.set_margins(MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE)
        self.set_auto_page_break(False, MARGIN_SIZE)

        self.organizer = layout.SongbookOrganizer()

    def footer(self):
        self.set_y(-15)
        self.set_font(FOOTER_FONT, 'B', FOOTER_SIZE)
        self.cell(0, self.font_size, 'Page ' + str(self.page_no()), align='C')

    def get_start_point(self, quadrant):
        if quadrant is 0:  # top left
            return (MARGIN_SIZE, MARGIN_SIZE)
        elif quadrant is 1:  # top right
            return (self.w / 2, MARGIN_SIZE)
        elif quadrant is 2:  # bottom left
            return (MARGIN_SIZE, self.h / 2)
        elif quadrant is 3:  # bottom right
            return (self.w / 2, self.h / 2)
        else:
            raise ValueError('Invalid quadrant: ' + str(self.quadrant))

    def get_size_and_overflow(self, song):
        self.set_font(LYRIC_FONT, '', LYRIC_SIZE)

        # Adjust for song width
        song_width = 0
        index_count = 0
        for part, chord_lyrics in song.chord_chart:
            indenting = False
            if any(tag in part.lower() for tag in INDENT_PARTS):
                index_count += 1
                indenting = True

            for line in chord_lyrics:
                lyrics_size = self.get_string_width(''.join(line.lyrics))
                if indenting:
                    lyrics_size += (index_count * INDENT_SIZE)
                if lyrics_size > song_width:
                    song_width = lyrics_size

        size = LYRIC_SIZE
        max_width = (self.w / 2) - MARGIN_SIZE - INNER_BORDER
        if song_width > max_width:
            size *= max_width / song_width

        # Determine overflow and adjust for song height
        song_height = (song.get_chord_lines() * CHORD_SIZE) + \
            (song.get_lyric_lines() * size) + \
            ((len(song.chord_chart) - 1) * (CHORD_SIZE))

        half_height = (self.h / 2) - MARGIN_SIZE - INNER_BORDER
        overflow = song_height > half_height

        max_height = self.h - (2 * MARGIN_SIZE) - INNER_BORDER
        if overflow and song_height > max_height:
            size *= max_height / song_height

        return (size, overflow)

    def print_title(self, title):
        self.set_font(TITLE_FONT, 'B', TITLE_SIZE)
        self.cell(self.get_string_width(title), self.font_size, title, ln=2)

        self.set_fill_color(173, 216, 230)
        self.cell(self.w / 2.5, CHORD_SIZE / 4, '', ln=2, fill=True)

    def print_line(self, line, size):
        # No chords, only lyrics
        if not line.chords:
            self.set_font(LYRIC_FONT, '', size)
            self.cell(self.get_string_width(
                line.lyrics[0]), self.font_size, line.lyrics[0], ln=2)
            return

        # Print out first lyric segment, may be empty
        if line.lyrics[0]:
            self.set_xy(self.get_x(), self.get_y() + CHORD_SIZE)

            self.set_font(LYRIC_FONT, '', size)
            self.cell(self.get_string_width(
                line.lyrics[0]), self.font_size, line.lyrics[0])

            self.set_xy(self.get_x(), self.get_y() - CHORD_SIZE)

        # Print remaining chords and lyrics
        x_next = self.get_x()
        for i in range(len(line.chords)):
            self.set_x(x_next)

            self.set_font(CHORD_FONT, 'B', CHORD_SIZE)
            chord_x = self.get_x() + \
                self.get_string_width(line.chords[i] + ' ')
            self.cell(self.get_string_width(
                line.chords[i]), self.font_size, line.chords[i], ln=2)

            self.set_font(LYRIC_FONT, '', size)
            lyric_x = self.get_x() + self.get_string_width(line.lyrics[i + 1])
            self.cell(self.get_string_width(
                line.lyrics[i + 1]), self.font_size, line.lyrics[i + 1])

            self.set_xy(self.get_x(), self.get_y() - CHORD_SIZE)
            x_next = lyric_x if lyric_x > chord_x else chord_x

        self.ln(CHORD_SIZE + size)

    def print_part(self, start, part, lines, size):
        if lines:
            for line in lines:
                self.set_x(start)
                self.print_line(line, size)
            self.ln(CHORD_SIZE)
        else:  # Only part label (e.g. Intro)
            self.set_x(start)
            self.set_font(CHORD_FONT, '', CHORD_SIZE)
            self.cell(self.get_string_width(part), self.font_size, part, ln=2)

    def print_song(self, song, quadrant, size):
        x_start, y_start = self.get_start_point(quadrant)
        self.set_xy(x_start, y_start)

        self.print_title(song.title)
        indents = 0
        for part, lines in song.chord_chart:
            if any(tag in part.lower() for tag in INDENT_PARTS):
                indents += 1
                self.print_part(
                    x_start + (indents * INDENT_SIZE), part, lines, size)
            else:
                self.print_part(x_start, part, lines, size)

    def print_songbook(self, songs):
        # Assign songs to locations
        song_sizes = {}
        for song in songs:
            size, overflow = self.get_size_and_overflow(song)
            song_sizes[song.pco_id] = size
            self.organizer.insert_song(song, overflow)

        # Print songs in respective locations
        for page in self.organizer.pages:
            self.add_page()
            for i in range(4):
                if page[i]:
                    self.print_song(page[i], i, song_sizes[page[i].pco_id])
