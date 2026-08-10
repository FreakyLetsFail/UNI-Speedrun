from uni_speedrun.fachmodell.modulstatus import Modulstatus


def test_alle_modulstatus_sind_vorhanden() -> None:
    assert Modulstatus.GEPLANT.value == "geplant"
    assert Modulstatus.AKTIV.value == "aktiv"
    assert Modulstatus.ABGESCHLOSSEN.value == "abgeschlossen"


def test_modulstatus_koennen_aus_text_erzeugt_werden() -> None:
    assert Modulstatus("geplant") is Modulstatus.GEPLANT
    assert Modulstatus("aktiv") is Modulstatus.AKTIV
    assert Modulstatus("abgeschlossen") is Modulstatus.ABGESCHLOSSEN


def test_modulstatus_hat_genau_drei_werte() -> None:
    assert len(Modulstatus) == 3