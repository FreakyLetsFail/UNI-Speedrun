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

    assert bachelor_cs.zieldatum() == date(2027, 10, 10)