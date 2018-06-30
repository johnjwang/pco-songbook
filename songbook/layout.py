from collections import deque


class SongbookOrganizer:

    def __init__(self):
        self.pages = []
        self.layout = {
            0: None,  # top left
            1: None,  # top right
            2: None,  # bottom left
            3: None,  # bottom right
        }
        self.vacant = deque()

    def add_page(self):
        self.pages.append(dict(self.layout))
        self.vacant.clear()
        for i in range(len(self.layout)):
            self.vacant.append((len(self.pages) - 1, i))  # (pg, quad)

    def get_vacant_space(self, overflow):
        if overflow:
            re_add = []
            while len(self.vacant):
                quad = self.vacant.popleft()
                if quad[1] < 2 and not self.pages[quad[0]][quad[1] + 2]:
                    self.vacant.extendleft(re_add[::-1])
                    self.vacant.remove((quad[0], quad[1] + 2))
                    return quad
                re_add.append(quad)

            self.add_page()

            quad = self.vacant.popleft()
            self.vacant.remove((quad[0], quad[1] + 2))
            return quad
        else:
            if not len(self.vacant):
                self.add_page()
            return self.vacant.popleft()

    def insert_song(self, song, overflow):
        page_num, quad = self.get_vacant_space(overflow)
        self.pages[page_num][quad] = song
