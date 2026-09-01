from datetime import date
import sqlite3

from uni_speedrun.database.repository import StudienplanRepository
from uni_speedrun.fachmodell.modul import Modul
from uni_speedrun.fachmodell.modulstatus import Modulstatus
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
        with sqlite3.connect(self.datenbank_pfad) as con:

            con.execute("PRAGMA foreign_keys = ON")

            con.execute("DELETE FROM modul")
            con.execute("DELETE FROM studienplan")

            cursor = con.execute(
                """
                INSERT INTO studienplan (
                    studienziel_name,
                    zielects,
                    zieldauer,
                    startdatum
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    studienplan.studienziel_name,
                    studienplan.zielects,
                    studienplan.zieldauer,
                    studienplan.startdatum.isoformat(),
                ),
            )

            studienplan_id = cursor.lastrowid

            for modul in studienplan.module:
                con.execute(
                    """
                    INSERT INTO modul (
                        studienplan_id,
                        name,
                        ects,
                        geplante_dauer_tage,
                        reihenfolge,
                        status,
                        startdatum,
                        pruefungsdatum,
                        abschlussdatum,
                        note
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        studienplan_id,
                        modul.name,
                        modul.ects,
                        modul.geplante_dauer_tage,
                        modul.reihenfolge,
                        modul.status.name,
                        modul.startdatum.isoformat()
                        if modul.startdatum
                        else None,
                        modul.pruefungsdatum.isoformat()
                        if modul.pruefungsdatum
                        else None,
                        modul.abschlussdatum.isoformat()
                        if modul.abschlussdatum
                        else None,
                        modul.note,
                    ),
                )

    def laden(self) -> Studienplan | None:
        with sqlite3.connect(self.datenbank_pfad) as con:
            eintrag = con.execute(
                """
                SELECT id, studienziel_name, zielects, zieldauer, startdatum
                FROM studienplan
                LIMIT 1
                """
            ).fetchone()

            if eintrag is None:
                return None

            (
                studienplan_id,
                studienziel_name,
                zielects,
                zieldauer,
                startdatum,
            ) = eintrag

            module_eintraege = con.execute(
                """
                SELECT
                    name,
                    ects,
                    geplante_dauer_tage,
                    reihenfolge,
                    status,
                    startdatum,
                    pruefungsdatum,
                    abschlussdatum,
                    note
                FROM modul
                WHERE studienplan_id = ?
                ORDER BY reihenfolge
                """,
                (studienplan_id,),
            ).fetchall()

        module = []

        for eintrag in module_eintraege:
            (
                name,
                ects,
                geplante_dauer_tage,
                reihenfolge,
                status,
                modul_startdatum,
                pruefungsdatum,
                abschlussdatum,
                note,
            ) = eintrag

            modul = Modul(
                name=name,
                ects=ects,
                geplante_dauer_tage=geplante_dauer_tage,
                reihenfolge=reihenfolge,
                status=Modulstatus[status],
                startdatum=(
                    date.fromisoformat(modul_startdatum)
                    if modul_startdatum
                    else None
                ),
                pruefungsdatum=(
                    date.fromisoformat(pruefungsdatum)
                    if pruefungsdatum
                    else None
                ),
                abschlussdatum=(
                    date.fromisoformat(abschlussdatum)
                    if abschlussdatum
                    else None
                ),
            )

            modul.note = note
            module.append(modul)

        studienplan = Studienplan(
            module,
            studienziel_name,
            zielects,
            zieldauer,
        )

        studienplan.startdatum = date.fromisoformat(startdatum)

        return studienplan
