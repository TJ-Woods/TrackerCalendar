import datetime as dt


def get_calendar_date(year, x, y):
    return dt.datetime.strptime(f"{year}-{7*x+y+1}", "%Y-%j").date()


print(get_calendar_date(2026, 0, 0))
