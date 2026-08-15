import sqlite3

from uni_speedrun.database.repository import StudienplanRepository
from uni_speedrun.fachmodell.studienplan import Studienplan


class SQLiteStudienplanRepository(StudienplanRepository):
    def __init__(self, datenbank_pfad: str) -> None:
        self.datenbank_pfad = datenbank_pfad
        self._initialisiere_datenbank()

    def _initialisiere_datenbank(self) -> None:
        with sqlite3.connect(self.datenbank_pfad) as con:
            cur = con.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS studienplan (
                    id INTEGER PRIMARY KEY,
                    studienziel_name TEXT NOT NULL,
                    zielects INTEGER NOT NULL,
                    zieldauer INTEGER NOT NULL,
                    startdatum TEXT NOT NULL
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS modul (
                    id INTEGER PRIMARY KEY,
                    studienplan_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    ects INTEGER NOT NULL,
                    geplante_dauer_tage INTEGER NOT NULL,
                    reihenfolge INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    startdatum TEXT,
                    pruefungsdatum TEXT,
                    abschlussdatum TEXT,
                    note REAL,
                    FOREIGN KEY (studienplan_id)
                        REFERENCES studienplan(id)
                )
            """)

    def speichern(self, studienplan: Studienplan) -> None:
        pass

    def laden(self) -> Studienplan | None:
        pass