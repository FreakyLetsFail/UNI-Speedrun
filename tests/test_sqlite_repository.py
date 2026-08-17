from uni_speedrun.database.sqlite_repository import (
    SQLiteStudienplanRepository,
)
import sqlite3

from datetime import date

from uni_speedrun.fachmodell.studienplan import Studienplan


def test_sqlite_repository_kann_erstellt_werden(tmp_path):
    datenbank = tmp_path / "test.db"

    repository = SQLiteStudienplanRepository(str(datenbank))

    assert repository.datenbank_pfad == str(datenbank)


def test_sqlite_repository_erstellt_datenbank(tmp_path):
    datenbank = tmp_path / "test.db"

    SQLiteStudienplanRepository(str(datenbank))

    import sqlite3

    with sqlite3.connect(datenbank) as con:
        tabellen = con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()

    namen = {tabelle[0] for tabelle in tabellen}

    assert "studienplan" in namen
    assert "modul" in namen

def test_studienplan_wird_gespeichert(tmp_path):
    datenbank = tmp_path / "test.db"

    repository = SQLiteStudienplanRepository(str(datenbank))

    studienplan = Studienplan(
        [],
        "Bachelor Cyber Security",
        180,
        15,
    )

    studienplan.startdatum = date(2026, 8, 15)

    repository.speichern(studienplan)

    import sqlite3

    with sqlite3.connect(datenbank) as con:
        eintrag = con.execute(
            """
            SELECT studienziel_name, zielects, zieldauer, startdatum
            FROM studienplan
            """
        ).fetchone()

    assert eintrag == (
        "Bachelor Cyber Security",
        180,
        15,
        "2026-08-15",
    )