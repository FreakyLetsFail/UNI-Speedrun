import sqlite3


def connect_to_database(db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Modul (
            name TEXT,
            ects INTEGER,
            time INTEGER
        )
    """)

    cur.execute("""
        INSERT INTO Modul (name, ects, time)
        VALUES
            ('Wissenschaftliches Arbeiten', 5, 2),
            ('Mathe 1', 5, 4)
    """)

    con.commit()
    con.close()


def read_from_database(db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    for row in cur.execute("SELECT * FROM Modul"):
        print(row)

    con.close()


connect_to_database("test1.db")
read_from_database("test1.db")