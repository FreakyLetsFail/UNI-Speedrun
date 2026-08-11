from datetime import date

from uni_speedrun.fachmodell.studienziel import Studienziel


def test_bezeichnung():
    bachelor_cs = Studienziel(
        name="Bachelor Cyber Security",
        zielects=180,
        zieldauer=14
    )

    assert bachelor_cs.name == "Bachelor Cyber Security"
    assert bachelor_cs.zielects == 180
    assert bachelor_cs.zieldauer == 14


def test_zieldatum_wird_korrekt_berechnet():
    bachelor_cs1 = Studienziel(
        name="VWL",
        zielects=110,
        zieldauer=14
    )

    assert bachelor_cs1.name == "VWL"
    assert bachelor_cs1.zielects == 110
    assert bachelor_cs1.zieldauer == 14
    assert bachelor_cs1.zieldatum() == date(2027, 10, 11)#Hier Datum eintragen