import fpdf

CHORD_SIZE = 8
CHORD_FONT = 'Arial'
LYRIC_SIZE = 12
LYRIC_FONT = 'Arial'


class SongbookPDF(fpdf.FPDF):

    def __init__(self):
        super(SongbookPDF, self).__init__()

        self.set_font(CHORD_FONT, '', CHORD_SIZE)
        self.cho_height = self.font_size

        self.set_font(LYRIC_FONT, '', LYRIC_SIZE)
        self.lyr_height = self.font_size

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'B', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def print_title(self, num, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, num + ' - ' + title, 0, 1, 'L', 0)

    def get_chord_width(self, chord):
        self.set_font(CHORD_FONT, '', CHORD_SIZE)
        return self.get_string_width(chord)

    def get_lyric_width(self, lyric):
        self.set_font(LYRIC_FONT, '', LYRIC_SIZE)
        return self.get_string_width(lyric)

    def print_line(self, left_margin, line):
        self.set_x(left_margin)

        # Print out first lyric segment, may be empty
        if line.lyrics[0]:
            self.set_y(self.get_y() + self.cho_height)

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

            self.set_y(self.get_y() - self.cho_height)
            x_next = lyric_x if lyric_x > chord_x else chord_x

        self.ln(self.cho_height + self.lyr_height)

    def print_part(self, lines):
        for line in lines:
            self.print_line(self.l_margin, line)
        self.ln(self.cho_height)

    def print_song(self, song):
        self.add_page()
        self.print_title(song.key, song.title)

        for part, lines in song.chord_chart.items():
            self.print_part(lines)
