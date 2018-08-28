import fpdf
import layout

TITLE_SIZE = 12
TITLE_FONT = 'Arial'
START_MARGIN = 2

PART_TITLE_SIZE = 7
PART_TITLE_FONT = 'Arial'
PART_TITLE_MARGIN = 1

CHORD_SIZE = 8
CHORD_FONT = 'Arial'

LYRIC_SIZE = 11
LYRIC_FONT = 'Arial'

META_SIZE = 6
META_FONT = 'Arial'

FOOTER_SIZE = 8
FOOTER_FONT = 'Arial'

GUTTER_SIZE = 15
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
        self.printing_songs = False
        self.current_page = 0

    def footer(self):
        self.set_y(-15)

        if self.printing_songs:
            self.set_font(FOOTER_FONT, 'B', FOOTER_SIZE)
            self.cell(0, self.font_size, 'Page ' +
                      str(self.current_page), align='C')

            permission = 'Used by permission CCLI#1194926'
            self.cell(0, self.font_size, permission, align='R')

    def add_page_with_gutter(self):
        self.add_page()
        next_page_odd = self.page_no() % 2 == 1
        if next_page_odd:
            self.set_margins(MARGIN_SIZE + GUTTER_SIZE, MARGIN_SIZE, MARGIN_SIZE - GUTTER_SIZE)
        else:
            self.set_margins(MARGIN_SIZE - GUTTER_SIZE, MARGIN_SIZE, MARGIN_SIZE + GUTTER_SIZE)

    def print_table_of_contents(self):
        pages = self.organizer.pages
        self.add_page_with_gutter()

        self.set_font(TITLE_FONT, 'B', TITLE_SIZE)
        self.cell(0, TITLE_SIZE, 'Table of Contents', border='B', align='C')
        self.cell(0, TITLE_SIZE, 'Page', align='R')
        self.ln(LYRIC_SIZE * 1.5)

        self.set_auto_page_break(True, MARGIN_SIZE)
        self.set_font(LYRIC_FONT, '', LYRIC_SIZE)
        for pid in range(len(pages)):
            for quad in range(len(pages[pid])):
                if pages[pid][quad]:
                    self.cell(0, LYRIC_SIZE, pages[pid][quad].title)
                    self.cell(0, LYRIC_SIZE, str(pid + 1), align='R')
                    self.dashed_line(self.l_margin, self.get_y() + LYRIC_SIZE,
                                     self.w - self.r_margin, self.get_y() + LYRIC_SIZE, 1, 5)
                    self.ln(LYRIC_SIZE * 1.5)

        self.set_auto_page_break(False, MARGIN_SIZE)
        self.add_page_with_gutter()

    def get_start_point(self, quadrant):
        odd = self.page_no() % 2 == 1
        left_edge = None
        if odd:
            left_edge = MARGIN_SIZE + GUTTER_SIZE
        else:
            left_edge = MARGIN_SIZE - GUTTER_SIZE

        if quadrant is 0:  # top left
            return (left_edge, MARGIN_SIZE)
        elif quadrant is 1:  # top right
            return (self.w / 2, MARGIN_SIZE)
        elif quadrant is 2:  # bottom left
            return (left_edge, self.h / 2)
        elif quadrant is 3:  # bottom right
            return (self.w / 2, self.h / 2)
        else:
            raise ValueError('Invalid quadrant: ' + str(self.quadrant))

    # Overestimate height of songs
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
        metadata_height = 0
        if song.author or song.copyright:
            self.set_font(META_FONT, '', META_SIZE)
            meta_text = None
            if song.author and song.copyright:
                meta_text = song.author if len(song.author) > len(
                    song.copyright) else song.copyright
            else:
                meta_text = song.author if song.author else song.copyright
            meta_width = ((self.w / 2) - MARGIN_SIZE) / 2
            metadata_height = (self.get_string_width(
                meta_text) / meta_width) * META_SIZE

        song_height = (song.get_chord_lines() * CHORD_SIZE) + \
            (len(song.chord_chart) * (PART_TITLE_SIZE + PART_TITLE_MARGIN)) + \
            (song.get_lyric_lines() * size) + \
            metadata_height + TITLE_SIZE + START_MARGIN

        half_height = (self.h / 2) - MARGIN_SIZE - INNER_BORDER
        overflow = song_height > half_height

        max_height = self.h - (2 * MARGIN_SIZE) - INNER_BORDER
        if overflow and song_height > max_height:
            size *= max_height / song_height

        return (size, overflow)

    def print_title(self, title):
        size = TITLE_SIZE
        title_width = (self.w / 2) - MARGIN_SIZE - INNER_BORDER

        self.set_font(TITLE_FONT, 'B', TITLE_SIZE)
        if self.get_string_width(title) > title_width:
            size *= title_width / self.get_string_width(title)

        self.set_font(TITLE_FONT, 'B', size)
        self.cell(self.get_string_width(title), self.font_size, title, ln=2)

        self.set_fill_color(173, 216, 230)
        self.cell(self.w / 2.5, CHORD_SIZE / 4, '', ln=2, fill=True)

        self.set_y(self.get_y() + START_MARGIN)

    def print_metadata(self, title, author, copyright):
        self.set_font(META_FONT, '', META_SIZE)
        x_start = self.get_x()
        y_start = self.get_y()
        meta_width = ((self.w / 2) - MARGIN_SIZE) / 2

        if author:
            author_text = 'By ' + author
            self.multi_cell(meta_width, self.font_size, author_text, align='L')

        self.set_xy(x_start + meta_width, y_start)

        if copyright:
            copyright_text = '@ ' + copyright
            self.multi_cell(meta_width, self.font_size,
                            copyright_text, align='R')

    def print_line(self, line, size):
        x_start = self.get_x()

        # No chords, only lyrics
        if not line.chords:
            self.set_font(LYRIC_FONT, '', size)
            self.cell(self.get_string_width(
                line.lyrics[0]), self.font_size, line.lyrics[0], ln=2)
            return

        # Chords exist, but no lyrics
        if not ''.join(line.lyrics).strip():
            self.set_font(CHORD_FONT, 'B', CHORD_SIZE)
            for chord in line.chords:
                self.cell(self.get_string_width(chord + ' '),
                          self.font_size, chord + ' ')
            self.set_xy(x_start, self.get_y() + CHORD_SIZE)
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

        self.set_xy(x_start, self.get_y() + CHORD_SIZE + size)

    def print_part_title(self, start, title):
        title = title.upper()
        self.set_x(start)
        self.set_font(PART_TITLE_FONT, 'B', PART_TITLE_SIZE)
        self.cell(self.get_string_width(title), self.font_size, title)
        self.set_xy(0, self.get_y() + PART_TITLE_SIZE + PART_TITLE_MARGIN)
        return

    def print_part(self, start, part, lines, size):
        if all((line.is_empty() for line in lines)):
            self.set_x(start)
            self.set_font(CHORD_FONT, 'B', CHORD_SIZE)
            self.cell(self.get_string_width(part), self.font_size, part, ln=2)
        else:
            for line in lines:
                self.set_x(start)
                self.print_line(line, size)

    def print_song(self, song, quadrant, size, part_titles=False):
        x_start, y_start = self.get_start_point(quadrant)
        self.set_xy(x_start, y_start)

        self.print_title(song.title)
        indents = 0
        for part, lines in song.chord_chart:
            if part_titles:
                self.print_part_title(x_start, part)
                self.print_part(x_start, part, lines, size)
            else:
                if any(tag in part.lower() for tag in INDENT_PARTS):
                    indents += 1
                    self.print_part(
                        x_start + (indents * INDENT_SIZE), part, lines, size)
                else:
                    self.print_part(x_start, part, lines, size)

        self.set_xy(x_start, self.get_y() + size)
        self.print_metadata(song.title, song.author, song.copyright)

    def print_songbook(self, songs):
        # Assign songs to locations
        song_sizes = {}
        for song in songs:
            size, overflow = self.get_size_and_overflow(song)
            song_sizes[song.pco_id] = size
            self.organizer.insert_song(song, overflow)

        self.print_table_of_contents()
        self.printing_songs = True

        # Print songs in respective locations
        for page in self.organizer.pages:
            self.current_page += 1
            for i in range(4):
                if page[i]:
                    self.print_song(page[i], i, song_sizes[page[i].pco_id])
            self.add_page_with_gutter()

    def print_songbook_by_letter(self, songs):
        # Assign songs to locations
        song_sizes = {}
        last_song_letter = None
        for song in songs:
            letter_changed = last_song_letter is not None and song.title[0] != last_song_letter
            if letter_changed:
                self.organizer.add_until_odd_page()
            size, overflow = self.get_size_and_overflow(song)
            song_sizes[song.pco_id] = size
            self.organizer.insert_song(song, overflow)

            last_song_letter = song.title[0]

        self.add_page_with_gutter()
        self.printing_songs = True

        # Print songs in respective locations
        for page in self.organizer.pages:
            self.current_page += 1
            for i in range(4):
                if page[i]:
                    self.print_song(page[i], i, song_sizes[page[i].pco_id], part_titles=True)
            self.add_page_with_gutter()
