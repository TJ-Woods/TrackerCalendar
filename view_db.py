import sqlite3 as sql

TRACKER_DB = "./TrackerCalendar.db"
with sql.connect(TRACKER_DB) as conn:
    curs = conn.cursor()
    res1 = curs.execute("SELECT * FROM Tracker;").fetchall()
    res2 = curs.execute("""
        SELECT T.name, COUNT(C.id), C.date
        FROM Contribution AS C
        INNER JOIN Tracker as T
        ON C.Tracker_id == T.id
        GROUP BY T.name, C.date;
    """).fetchall()


for i in range(len(res2)):
    for j in range(len(res2[i])):
        print(res2[i][j], end=", ")
    print()
