from datetime import date
import pytest
from uni_speedrun.fachmodell.pruefungsleistung import Pruefungsleistung


def test_pruefungsleistung_erstellung():
    p = Pruefungsleistung(titel="Klausur OOP", datum=date(2026, 8, 20), note=1.7)
    assert p.titel == "Klausur OOP"
    assert p.note == 1.7
    assert p.datum == date(2026, 8, 20)
    assert p.ist_bewertet() is True
    assert p.ist_bestanden() is True


def test_pruefungsleistung_validierung():
    p = Pruefungsleistung(titel="Projektbericht")

    with pytest.raises(ValueError, match="nicht leer"):
        p.titel = ""

    with pytest.raises(ValueError, match="zwischen 1.0 und 5.0"):
        p.note = 0.5

    with pytest.raises(ValueError, match="zwischen 1.0 und 5.0"):
        p.note = 5.5

    p.note = 5.0
    assert p.ist_bestanden() is False


def test_pruefungsleistung_note_aktualisiert_bestanden_status():
    p = Pruefungsleistung(titel="Projektbericht", note=5.0)

    p.note = 1.7

    assert p.bestanden is True
    assert p.ist_bestanden() is True


def test_modul_property_validierung():
    from uni_speedrun.fachmodell.modul import Modul

    m = Modul("Test", 5, 14, 1)

    with pytest.raises(ValueError, match="Modulname darf nicht leer"):
        m.name = "   "

    with pytest.raises(ValueError, match="ECTS müssen größer als 0"):
        m.ects = -2

    with pytest.raises(ValueError, match="Dauer muss größer als 0"):
        m.geplante_dauer_tage = 0

    with pytest.raises(ValueError, match="Reihenfolge muss größer als 0"):
        m.reihenfolge = -1
