import random
import sqlite3 as sql
import pygame as pg; pg.init()

WIN = pg.Window(title="TrackerCalendar", resizable=True)
WIN.maximize()
DIS = WIN.get_surface()

clock = pg.time.Clock()
TICK = 30

TRACKER_DB = "./TrackerCalendar.db"

TRACKER_WIDTH = 710
TRACKER_HEIGHT = 112
TRACKER_INT_PADX = 12  # Tracker Internal Padding X
TRACKER_INT_PADY = 12  # Tracker Internal Padding Y
TRACKER_BRAD = 4       # Tracker Border Radius
DOT_SIZE = 10   # Square Size
DOT_PADX = 3    # Padding X
DOT_PADY = 3    # Padding Y
DOT_BRAD = 2    # Border Radius


# Wrappers #
def sql_query(func):
    def wrapper(*args, **kwargs):
        with sql.connect(TRACKER_DB) as conn:
            curs = conn.cursor()
            res = func(curs, *args, **kwargs)
            data = res.fetchall()
        print(data)
        return data

    return wrapper


# Classes #
class Theme:
    bg = "#202020"
    fg = "#dddddd"
    themes = {
        "green": [
            "#2a2a30",
            "#033a16",
            "#196c2e",
            "#2ea043",
            "#40c463",
            "#56d364",
            bg,
        ],
        "purple": [
            "#2a2a30",
            "#16033a",
            "#2e196c",
            "#432ea0",
            "#6340c4",
            "#6456d3",
            bg,
        ],

        "teal": [
            "#2a2a30",
            "#458B74",
            "#66CDAA",
            "#76EEC6",
            "#7FFFD4",
            "#9bffd0",
            bg,
        ],

        "red": [
            "#2a2a30",
            "#4C0519",
            "#991B1B",
            "#DC2626",
            "#F35141",
            "#FF0000",
            bg,
        ],

        "mono": [
            "#2a2a30",
            "#334155",
            "#4B5B70",
            "#64748B",
            "#94A3B8",
            "#CBD5E1",
            bg,
        ],

        "blue": [
            "#2a2a30",
            "#1E3A8A",
            "#224DBB",
            "#2563EB",
            "#3B82F6",
            "#60A5FA",
            bg,
        ],
    }

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
    def __init__(
            self,
            name: str,
            x: int, y: int,
            color: list = Theme.themes["green"],
            show_name: bool = False,
    ):
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
                year = 2026  # TODO: CALCULATE YEAR
                date = get_calendar_date(year, x, y)
                self.dots[y_rel].append(Dot(x, y, self.color, (random.randint(0, 5) if x_rel < 53 else 6)))

    def draw(self):
        pg.draw.rect(DIS, Theme.Tracker.border_color, self.rect, 2, 10)
        for y in range(len(self.dots)-1):
            for x in range(len(self.dots[y])-1):
                self.dots[y][x].draw(self.rect)


@sql_query
def sql_get_tracker_data(curs, tracker_name):
    return curs.execute("""
        SELECT C.date, COUNT(C.id)
        FROM Contribution AS C
        INNER JOIN Tracker AS T
        ON C.Tracker_id == T.id
        WHERE T.name == ?
        GROUP BY C.date;
    """, (tracker_name,))


@sql_query
def sql_get_day_count(curs, tracker_name, date):
    return curs.execute("""
        SELECT COUNT(C.id)
        FROM Contribution AS C
        INNER JOIN Tracker AS T
        ON C.Tracker_id == T.id
        WHERE T.name == ?
        AND C.date == ?;
    """, (tracker_name, date))


@sql_query
def sql_get_trackers(curs) -> list[str]:
    return curs.execute("""
        SELECT id, name, theme
        FROM Tracker;
    """)


def get_calendar_date(year, x, y):
    day = 0
    month = 0
    return f"{year}-{month}-{day}"


def main():

    trackers = [
    ]
    x, y = 20, 20
    for t in sql_get_trackers():
        trackers.append(Tracker(
            t[1],
            x, y,
            Theme.themes[t[2]],
        ))
        y += 130
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
        for tracker in trackers:
            tracker.draw()

        WIN.flip()
        clock.tick(TICK)

main()
