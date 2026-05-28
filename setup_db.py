import sqlite3 as sql

TRACKER_DB = "./TrackerCalendar.db"
with sql.connect(TRACKER_DB) as conn:
    curs = conn.cursor()
    # Remove #
    curs.execute("""
        DROP TABLE IF EXISTS Tracker;
    """)
    curs.execute("""
        DROP TABLE IF EXISTS Contribution;
    """)

    # Create #
    curs.execute("""
        CREATE TABLE IF NOT EXISTS Tracker (
            id INTEGER PRIMARY KEY,
            name VARCHAR[30] NOT NULL,
            theme VARCHAR[15] DEFAULT "green"
        );
    """)
    curs.execute("""
        CREATE TABLE IF NOT EXISTS Contribution (
            id INTEGER PRIMARY KEY,
            Tracker_id INTEGER REFERENCES Tracker(id),
            date DATE NOT NULL
        );
    """)

    # Commit
    conn.commit()

