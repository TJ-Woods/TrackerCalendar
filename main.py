import random
import datetime as dt
import sqlite3 as sql
import pygame as pg; pg.init()

WIN = pg.Window(title="TrackerCalendar", resizable=True)
WIN.maximize()
DIS = WIN.get_surface()

clock = pg.time.Clock()
TICK = 30
FONT = pg.font.SysFont("", 12)
TITLE_FONT = pg.font.SysFont("", 20)

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
    def __init__(self, x, y, color, count, date: dt.date = None,):
        self.x = x
        self.y = y
        self.color = color
        self.count = count
        self.rect = pg.Rect(self.x, self.y, DOT_SIZE, DOT_SIZE)
        self.date = date if date is not None else dt.datetime.today().date()
        self.draw_info_timer = 0

    def update(self):
        if self.draw_info_timer:
            self.draw_info(self.tracker, True)
            self.draw_info_timer -= 1
        if self.draw_info_timer == 1:
            return True  # Signal update

    def draw(self, parent_rect):
        parentx = parent_rect[0]
        parenty = parent_rect[1]
        rect = pg.Rect(
            parentx+self.rect[0]+TRACKER_INT_PADX,
            parenty+self.rect[1]+TRACKER_INT_PADY,
            DOT_SIZE,
            DOT_SIZE
        )
        lvl = self.count  # TODO: Normalise lvl to integer between 0 and 4
        pg.draw.rect(DIS, self.color[lvl], rect, border_radius=DOT_BRAD)

    def draw_info(self, tracker, internal=False):
        self.tracker = tracker
        txt = str(self.date) + " " + str(sql_get_day_count(tracker, self.date)[0][0])
        DIS.blit(FONT.render(txt, False, Theme.fg, Theme.bg), (self.rect[0], self.rect[1]))
        if not internal:
            self.draw_info_timer = 150


class Tracker:
    def __init__(
            self,
            name: str,
            x: int, y: int,
            color: list = Theme.themes["green"],
            show_name: bool = False,
            show_year: bool = False,
    ):
        self.name = name
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x, self.y, TRACKER_WIDTH, TRACKER_HEIGHT)
        self.dots = [[], [], [], [], [], [], []]
        self.color = color
        self.show_name = show_name
        self.show_year = show_year
        year = 2026  # TODO: CALCULATE YEAR
        self.year = year
        y_offset = get_calendar_date(year, 1).weekday()
        day_count = 1
        for x_rel in range(52+1):
            for y_rel in range(7):
                # x and y are relative to box in pixels
                date = get_calendar_date(year, day_count)
                if date == -1: continue
                if y_rel < y_offset and x_rel == 0: continue
                day_count += 1
                x = 1 + x_rel * (DOT_SIZE + DOT_PADX)
                y = 1 + y_rel * (DOT_SIZE + DOT_PADY)
                count = sql_get_day_count(self.name, date)[0][0]
                self.dots[y_rel].append(Dot(x, y, self.color, count, date))

    def draw(self):
        pg.draw.rect(DIS, Theme.Tracker.border_color, self.rect, 2, 10)
        for y in range(len(self.dots)):
            for x in range(len(self.dots[y])):
                self.dots[y][x].draw(self.rect)
        if self.show_name:
            txt = " " + str(self.name) + " "
            DIS.blit(TITLE_FONT.render(txt, True, Theme.Tracker.border_color, Theme.bg), (self.x + 2*DOT_SIZE, self.y-DOT_SIZE//2))
        if self.show_year:
            txt = list((i for i in str(self.year)))
            for i in range(len(txt)):
                DIS.blit(TITLE_FONT.render(" ", False, Theme.Tracker.border_color, Theme.bg), (self.x, self.y + i*1.5*DOT_SIZE + 2*DOT_SIZE))
            for i in range(len(txt)):
                DIS.blit(TITLE_FONT.render(txt[i], True, Theme.Tracker.border_color, Theme.bg), (self.x-DOT_SIZE//3, self.y + i*1.5*DOT_SIZE+DOT_SIZE*2.5))



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
    """
    Takes in tracker_name, date;
    Returns ((count,),)
    """
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


def get_calendar_date(year, day):
    """
    Gets the calendar date in form 'YYYY-MM-DD' given
    the day of the year (1-365[+1])
    """
    try:
        return dt.datetime.strptime(f"{year}-{day}", "%Y-%j").date()
    except:
        return -1


def handle_event(event):
    global trackers
    update = False
    if event.type == pg.MOUSEBUTTONUP:
        if event.button == pg.BUTTON_LEFT:
            mouse_pos = pg.mouse.get_pos()
            mouse_rect = pg.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
            for tracker in trackers:
                if mouse_rect.colliderect(tracker.rect):
                    for y in tracker.dots:
                        for dot in y:
                            if mouse_rect.colliderect(dot.rect):
                                dot.draw_info(tracker.name)
                                update = True
    return update


def main():
    global trackers
    trackers = [
    ]
    x, y = 20, 20
    for t in sql_get_trackers():
        trackers.append(Tracker(
            t[1],
            x, y,
            Theme.themes[t[2]],
            show_name=True,
            show_year=True,
        ))
        y += 130
    update = True
    while True:
        DIS.fill(Theme.bg)
        for tracker in trackers:
            for y in tracker.dots:
                for dot in y:
                    update = dot.update() or update
            update = tracker.draw() or update

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
            else:
                update = handle_event(event) or update

        if update:
            WIN.flip()
        clock.tick(TICK)
        update = False


main()
