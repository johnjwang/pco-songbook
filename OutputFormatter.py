import fpdf

CHORD_SIZE = 8
CHORD_FONT = 'Arial'
LYRIC_SIZE = 12
LYRIC_FONT = 'Arial'

INDENT_SIZE = 4
INDENT_PARTS = [
    'pre-chorus',
    'chorus',
    'bridge',
]


class SongbookPDF(fpdf.FPDF):

    def __init__(self):
        super(SongbookPDF, self).__init__()

        self.set_font(CHORD_FONT, '', CHORD_SIZE)
        self.cho_height = self.font_size

        self.set_font(LYRIC_FONT, '', LYRIC_SIZE)
        self.lyr_height = self.font_size

        self.quadrant = 1

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'B', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def get_start_point(self):
        if self.quadrant is 1:
            self.quadrant = 2
            return [self.l_margin, self.t_margin]
        elif self.quadrant is 2:
            self.quadrant = 3
            return [self.w / 2, self.t_margin]
        elif self.quadrant is 3:
            self.quadrant = 4
            return [self.l_margin, self.h / 2]
        elif self.quadrant is 4:
            self.quadrant = 1
            return [self.w / 2, self.h / 2]
        else:
            raise ValueError('Invalid quadrant: ' + str(self.quadrant))

    def print_title(self, num, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 6, num + ' - ' + title, ln=2)

        self.set_fill_color(173, 216, 230)
        self.cell(self.w / 3, self.cho_height / 3, '', ln=2, fill=True)

    def get_chord_width(self, chord):
        self.set_font(CHORD_FONT, '', CHORD_SIZE)
        return self.get_string_width(chord)

    def get_lyric_width(self, lyric):
        self.set_font(LYRIC_FONT, '', LYRIC_SIZE)
        return self.get_string_width(lyric)

    def print_line(self, line):
        if not line.chords:
            self.set_font(LYRIC_FONT, '', LYRIC_SIZE)
            self.cell(self.get_string_width(
                line.lyrics[0]), self.font_size, line.lyrics[0], ln=2)
            return

        # Print out first lyric segment, may be empty
        if line.lyrics[0]:
            self.set_xy(self.get_x(), self.get_y() + self.cho_height)

            self.set_font(LYRIC_FONT, '', LYRIC_SIZE)
            self.cell(self.get_string_width(
                line.lyrics[0]), self.font_size, line.lyrics[0])

            self.set_xy(self.get_x(), self.get_y() - self.cho_height)

        x_next = self.get_x()
        for i in range(len(line.chords)):
            self.set_x(x_next)

            self.set_font(CHORD_FONT, '', CHORD_SIZE)
            chord_x = self.get_x() + self.get_string_width(line.chords[i])
            self.cell(self.get_string_width(
                line.chords[i]), self.font_size, line.chords[i], ln=2)

            self.set_font(LYRIC_FONT, '', LYRIC_SIZE)
            lyric_x = self.get_x() + self.get_string_width(line.lyrics[i + 1])
            self.cell(self.get_string_width(
                line.lyrics[i + 1]), self.font_size, line.lyrics[i + 1])

            self.set_xy(self.get_x(), self.get_y() - self.cho_height)
            x_next = lyric_x if lyric_x > chord_x else chord_x

        self.ln(self.cho_height + self.lyr_height)

    def print_part(self, indent, part, lines):
        if lines:
            for line in lines:
                self.set_x(indent)
                self.print_line(line)
            self.ln(self.cho_height)
        else:
            self.set_x(indent)
            self.set_font(CHORD_FONT, '', CHORD_SIZE)
            self.cell(self.get_string_width(part), self.font_size, part, ln=2)

    def print_song(self, song):
        if self.quadrant == 1:
            self.add_page()

        start_xy = self.get_start_point()
        self.set_xy(start_xy[0], start_xy[1])

        self.print_title(song.key, song.title)
        indent_count = 0
        for part, lines in song.chord_chart.items():
            indent = start_xy[0]
            if part.lower() in INDENT_PARTS:
                indent_count += 1
                indent += indent_count * INDENT_SIZE
            self.print_part(indent, part, lines)
