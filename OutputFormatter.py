import fpdf

CHORD_SIZE = 8
CHORD_FONT = 'Arial'
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

    def get_chord_width(self, chord):
        self.set_font(CHORD_FONT, '', CHORD_SIZE)
        return self.get_string_width(chord)

    def get_lyric_width(self, lyric):
        self.set_font(LYRIC_FONT, '', LYRIC_SIZE)
        return self.get_string_width(lyric)

    def print_part(self, lines):
        for l in lines:
            self.set_x(self.l_margin)

            # Print out first lyric segment, may be empty
            if l.lyrics[0]:
                self.set_font(CHORD_FONT, '', CHORD_SIZE)
                self.set_y(self.get_y() + self.font_size)

                self.set_font(LYRIC_FONT, '', LYRIC_SIZE)
                self.cell(self.get_string_width(
                    l.lyrics[0]), self.font_size, l.lyrics[0])

                self.set_font(CHORD_FONT, '', CHORD_SIZE)
                self.set_xy(self.get_x(), self.get_y() - self.font_size)

            x_next = self.get_x()
            for i in range(len(l.chords)):
                self.set_x(x_next)

                self.set_font(CHORD_FONT, '', CHORD_SIZE)
                chord_x = self.get_x() + self.get_string_width(l.chords[i])
                self.cell(self.get_string_width(
                    l.chords[i]), self.font_size, l.chords[i], ln=2)

                self.set_font(LYRIC_FONT, '', LYRIC_SIZE)
                lyric_x = self.get_x() + self.get_string_width(l.lyrics[i + 1])
                self.cell(self.get_string_width(
                    l.lyrics[i + 1]), self.font_size, l.lyrics[i + 1])

                self.set_font(CHORD_FONT, '', CHORD_SIZE)
                self.set_y(self.get_y() - self.font_size)

                x_next = lyric_x if lyric_x > chord_x else chord_x

            self.set_font(LYRIC_FONT, '', LYRIC_SIZE)
            self.ln(2 * self.font_size)

    def print_song(self, song):
        self.add_page()
        self.print_title(song.key, song.title)

        for part, lines in song.chord_chart.items():
            self.print_part(lines)
