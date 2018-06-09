import fpdf

CHORD_SIZE = 8
CHORD_FONT = 'Courier'
LYRIC_SIZE = 12
LYRIC_FONT = 'Arial'


class SongbookPDF(fpdf.FPDF):

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'B', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def print_title(self, num, title):
        # Arial 12
        self.set_font('Arial', 'B', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, num + ' - ' + title, 0, 1, 'L', 0)

    def print_part(self, lines):
        for line in lines:
            self.set_font(CHORD_FONT, '', CHORD_SIZE)
            self.set_xy(self.l_margin, self.get_y() + self.font_size)
            for i in range(len(line.chords)):
                # Print out lyric in place
                if line.lyrics[i]:
                    self.set_font(LYRIC_FONT, '', LYRIC_SIZE)
                    self.cell(self.get_string_width(
                        line.lyrics[i]), self.font_size, line.lyrics[i])

                # Print out chord above lyric
                self.set_font(CHORD_FONT, '', CHORD_SIZE)
                self.set_xy(self.get_x(), self.get_y() - self.font_size)
                self.cell(self.get_string_width(
                    line.chords[i]), self.font_size, line.chords[i], ln=2)
            self.set_font(LYRIC_FONT, '', LYRIC_SIZE)
            self.cell(self.get_string_width(
                line.lyrics[-1]), self.font_size, line.lyrics[-1], ln=1)
        self.ln()

    def print_song(self, song):
        self.add_page()
        self.print_title(song.key, song.title)

        for part, lines in song.chord_chart.items():
            self.print_part(lines)
