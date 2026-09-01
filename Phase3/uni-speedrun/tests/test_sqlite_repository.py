from uni_speedrun.database.sqlite_repository import (
    SQLiteStudienplanRepository,
)
import sqlite3

from datetime import date

from uni_speedrun.fachmodell.studienplan import Studienplan
from uni_speedrun.fachmodell.modul import Modul
from uni_speedrun.fachmodell.modulstatus import Modulstatus


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

def test_module_werden_gespeichert(tmp_path):
    datenbank = tmp_path / "test.db"

    repository = SQLiteStudienplanRepository(str(datenbank))

    modul1 = Modul(
        name="Python OOP",
        ects=5,
        geplante_dauer_tage=14,
        reihenfolge=1,
    )

    modul2 = Modul(
        name="Mathematik",
        ects=5,
        geplante_dauer_tage=21,
        reihenfolge=2,
    )

    studienplan = Studienplan(
        [modul1, modul2],
        "Bachelor Cyber Security",
        180,
        15,
    )

    repository.speichern(studienplan)

    with sqlite3.connect(datenbank) as con:
        module = con.execute(
            """
            SELECT name, ects, geplante_dauer_tage, reihenfolge
            FROM modul
            ORDER BY reihenfolge
            """
        ).fetchall()

    assert module == [
        ("Python OOP", 5, 14, 1),
        ("Mathematik", 5, 21, 2),
    ]

def test_studienplan_kann_geladen_werden(tmp_path):
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

    geladener_studienplan = repository.laden()

    assert geladener_studienplan is not None
    assert geladener_studienplan.studienziel_name == "Bachelor Cyber Security"
    assert geladener_studienplan.zielects == 180
    assert geladener_studienplan.zieldauer == 15
    assert geladener_studienplan.startdatum == date(2026, 8, 15)

def test_module_werden_geladen(tmp_path):
    datenbank = tmp_path / "test.db"

    repository = SQLiteStudienplanRepository(str(datenbank))

    modul1 = Modul(
        name="Python OOP",
        ects=5,
        geplante_dauer_tage=14,
        reihenfolge=1,
    )

    modul2 = Modul(
        name="Mathematik",
        ects=5,
        geplante_dauer_tage=21,
        reihenfolge=2,
    )

    studienplan = Studienplan(
        [modul1, modul2],
        "Bachelor Cyber Security",
        180,
        15,
    )

    repository.speichern(studienplan)

    geladener_studienplan = repository.laden()

    assert geladener_studienplan is not None
    assert len(geladener_studienplan.module) == 2

    assert geladener_studienplan.module[0].name == "Python OOP"
    assert geladener_studienplan.module[0].ects == 5
    assert geladener_studienplan.module[0].geplante_dauer_tage == 14
    assert geladener_studienplan.module[0].reihenfolge == 1

    assert geladener_studienplan.module[1].name == "Mathematik"
    assert geladener_studienplan.module[1].ects == 5
    assert geladener_studienplan.module[1].geplante_dauer_tage == 21
    assert geladener_studienplan.module[1].reihenfolge == 2

def test_laden_gibt_none_bei_leerer_datenbank(tmp_path):
    datenbank = tmp_path / "test.db"

    repository = SQLiteStudienplanRepository(str(datenbank))

    assert repository.laden() is None

def test_modulstatus_wird_gespeichert_und_geladen(tmp_path):
    datenbank = tmp_path / "test.db"

    repository = SQLiteStudienplanRepository(str(datenbank))

    modul = Modul(
        name="Python OOP",
        ects=5,
        geplante_dauer_tage=14,
        reihenfolge=1,
    )

    modul._aktivieren(date(2026, 8, 10))

    studienplan = Studienplan(
        [modul],
        "Bachelor Cyber Security",
        180,
        15,
    )

    repository.speichern(studienplan)

    geladener_studienplan = repository.laden()

    assert geladener_studienplan.module[0].status == Modulstatus.AKTIV

def test_modul_daten_werden_gespeichert_und_geladen(tmp_path):
    datenbank = tmp_path / "test.db"

    repository = SQLiteStudienplanRepository(str(datenbank))

    modul = Modul(
        name="Python OOP",
        ects=5,
        geplante_dauer_tage=14,
        reihenfolge=1,
    )

    modul._aktivieren(date(2026, 8, 10))
    modul._warte_auf_ergebnis(date(2026, 8, 24))

    studienplan = Studienplan(
        [modul],
        "Bachelor Cyber Security",
        180,
        15,
    )

    repository.speichern(studienplan)

    geladener_studienplan = repository.laden()
    geladenes_modul = geladener_studienplan.module[0]

    assert geladenes_modul.startdatum == date(2026, 8, 10)
    assert geladenes_modul.pruefungsdatum == date(2026, 8, 24)

def test_modulnote_wird_gespeichert_und_geladen(tmp_path):
    datenbank = tmp_path / "test.db"

    repository = SQLiteStudienplanRepository(str(datenbank))

    modul = Modul(
        name="Python OOP",
        ects=5,
        geplante_dauer_tage=14,
        reihenfolge=1,
    )

    modul._aktivieren(date(2026, 8, 10))
    modul._warte_auf_ergebnis(date(2026, 8, 24))

    studienplan = Studienplan(
        [modul],
        "Bachelor Cyber Security",
        180,
        15,
    )

    modul.note = 1.7

    repository.speichern(studienplan)

    geladener_studienplan = repository.laden()

    assert geladener_studienplan.module[0].note == 1.7