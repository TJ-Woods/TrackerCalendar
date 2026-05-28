import sqlite3 as sql

TRACKER_DB = "./TrackerCalendar.db"
with sql.connect(TRACKER_DB) as conn:
    curs = conn.cursor()
    data = (
        ("Drink Water", "blue"),
        ("Study", "green")
    )

    values = (
        (1, "2026-05-28"),
        (1, "2026-05-28"),
        (1, "2026-05-28"),
        (2, "2026-05-22"),
        (1, "2026-05-22"),
        (2, "2026-04-10"),
        (2, "2026-04-10"),
        (2, "2026-04-10")
    )
    curs.executemany("""
        INSERT INTO Tracker (name, theme) VALUES (?, ?)
     """, data)
    curs.executemany("""
         INSERT INTO Contribution (Tracker_id, date) VALUES (?, ?)
    """, values)
    conn.commit()
