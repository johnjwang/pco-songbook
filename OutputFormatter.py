import fpdf


class Songbook(fpdf.FPDF):

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'B', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def song_title(self, num, title):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, num + ' - ' + title, 0, 1, 'L', 0)
        # Line break
        self.ln(4)

    def song_body(self, song):
        # Times 12
        self.set_font('Courier', '', 12)
        # Output justified text
        for part, lines in song.items():
            self.cell(0, 6, part, 0, 1, 'L', 0)
            for line in lines:
                self.multi_cell(0, 6, line.getTwoline(), 0, 1, 'L', 0)
            self.ln()

    def print_song(self, num, title, song):
        self.add_page()
        self.song_title(num, title)
        self.song_body(song)
