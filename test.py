import sqlite3 as sql

TRACKER_DB = "./TrackerCalendar.db"


def sql_query(func):
    def wrapper(*args, **kwargs):
        with sql.connect(TRACKER_DB) as conn:
            curs = conn.cursor()
            res = func(curs, *args, **kwargs)
            data = res.fetchall()
        print(data)
        return data

    return wrapper


@sql_query
def get_all(curs, tracker_name):
    return curs.execute("""
        SELECT C.date, COUNT(C.id)
        FROM Contribution AS C
        INNER JOIN Tracker AS T
        ON C.Tracker_id == T.id
        WHERE T.name == ?
        GROUP BY C.date;
    """, (tracker_name,))


get_all("Study")
