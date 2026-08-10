from datetime import date

from uni_speedrun.fachmodell.modul import Modul
from uni_speedrun.fachmodell.modulstatus import Modulstatus


def test_neues_modul_startet_geplant():
    modul = Modul(
        name="Python OOP",
        ects=5,
        geplante_dauer_tage=14,
        reihenfolge=1,
    )

    assert modul.name == "Python OOP"
    assert modul.ects == 5
    assert modul.geplante_dauer_tage == 14
    assert modul.reihenfolge == 1
    assert modul.status is Modulstatus.GEPLANT


def test_modul_kann_bereits_abgeschlossen_sein():
    modul = Modul(
        name="Mathematik 1",
        ects=5,
        geplante_dauer_tage=28,
        reihenfolge=1,
        status=Modulstatus.ABGESCHLOSSEN,
    )

    assert modul.status is Modulstatus.ABGESCHLOSSEN


def test_modul_wird_aktiviert():
    modul = Modul(
        name="Python OOP",
        ects=5,
        geplante_dauer_tage=14,
        reihenfolge=1,
    )
    startdatum = date(2026, 8, 10)

    modul.aktivieren(startdatum)

    assert modul.status is Modulstatus.AKTIV
    assert modul.startdatum == startdatum


def test_enddatum_wird_berechnet():
    modul = Modul(
        name="Python OOP",
        ects=5,
        geplante_dauer_tage=14,
        reihenfolge=1,
    )
    modul.aktivieren(date(2026, 8, 10))

    enddatum = modul.berechne_enddatum()

    assert enddatum == date(2026, 8, 24)


def test_restzeit_wird_berechnet():
    modul = Modul(
        name="Python OOP",
        ects=5,
        geplante_dauer_tage=14,
        reihenfolge=1,
    )
    modul.aktivieren(date(2026, 8, 10))

    restzeit = modul.berechne_restzeit(date(2026, 8, 20))

    assert restzeit == 4


def test_ueberfaelliges_modul_hat_negative_restzeit():
    modul = Modul(
        name="Python OOP",
        ects=5,
        geplante_dauer_tage=14,
        reihenfolge=1,
    )
    modul.aktivieren(date(2026, 8, 10))

    restzeit = modul.berechne_restzeit(date(2026, 8, 27))

    assert restzeit == -3


def test_modul_wird_abgeschlossen():
    modul = Modul(
        name="Python OOP",
        ects=5,
        geplante_dauer_tage=14,
        reihenfolge=1,
    )
    modul.aktivieren(date(2026, 8, 10))
    abschlussdatum = date(2026, 8, 22)

    modul.schliesse_ab(abschlussdatum)

    assert modul.status is Modulstatus.ABGESCHLOSSEN
    assert modul.abschlussdatum == abschlussdatum
    assert modul.berechne_aktive_tage() == 12