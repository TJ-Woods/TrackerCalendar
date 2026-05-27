import random
import pygame as pg; pg.init()

WIN = pg.Window(title="TrackerCalendar", resizable=True)
WIN.maximize()
DIS = WIN.get_surface()

clock = pg.time.Clock()
TICK = 30

TRACKER_WIDTH = 723
TRACKER_HEIGHT = 113
DOT_SIZE = 10   # Square Size
DOT_PADX = 3    # Padding X
DOT_PADY = 3    # Padding Y
DOT_BRAD = 2    # Border Radius
TRACKER_INT_PADX = 7  # Tracker Internal Padding X
TRACKER_INT_PADY = 9  # Tracker Internal Padding Y


class Theme:
    bg = "#202020"
    fg = "#dddddd"

    green = [
        "#2a2a30",
        "#033a16",
        "#196c2e",
        "#2ea043",
        "#40c463",
        "#56d364",
        bg,
    ]

    class Tracker:
        bg = "#202020"
        border_color = "#808080"


class Dot:
    def __init__(self, x, y, color, lvl):
        self.x = x
        self.y = y
        self.color = color
        self.lvl = lvl
        self.rect = pg.Rect(self.x, self.y, DOT_SIZE, DOT_SIZE)

    def draw(self, parent_rect):
        parentx = parent_rect[0]
        parenty = parent_rect[1]
        rect = pg.Rect(
            parentx+self.rect[0]+TRACKER_INT_PADX,
            parenty+self.rect[1]+TRACKER_INT_PADY,
            DOT_SIZE,
            DOT_SIZE
        )
        pg.draw.rect(DIS, self.color[self.lvl], rect, border_radius=DOT_BRAD)


class Tracker:
    def __init__(self, name: str, x: int, y: int, color: pg.Color):
        self.name = name
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x, self.y, TRACKER_WIDTH, TRACKER_HEIGHT)
        self.dots = []
        self.color = color
        for y_rel in range(self.rect.height//(DOT_SIZE+DOT_PADY)):
            self.dots.append([])
            for x_rel in range(self.rect.width//(DOT_SIZE+DOT_PADX)):
                # x and y are relative to box in pixels
                x = x_rel * (DOT_SIZE + DOT_PADX)
                y = y_rel * (DOT_SIZE + DOT_PADY)
                self.dots[y_rel].append(Dot(x, y, self.color, (random.randint(0,5) if x_rel < 52 else 6)))

    def draw(self):
        pg.draw.rect(DIS, Theme.Tracker.border_color, self.rect, 2, 10)
        for y in range(len(self.dots)-1):
            for x in range(len(self.dots[y])-1):
                self.dots[y][x].draw(self.rect)


def main():

    t = Tracker("test_tracker", 20, 20, Theme.green)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()

        DIS.fill(Theme.bg)
        t.draw()

        WIN.flip()
        clock.tick(TICK)

main()
