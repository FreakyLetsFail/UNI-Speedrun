from uni_speedrun.database.sqlite_repository import (
    SQLiteStudienplanRepository,
)
import sqlite3


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