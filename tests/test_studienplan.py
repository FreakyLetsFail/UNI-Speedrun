import pytest  # <-- WICHTIG für pytest.raises
from uni_speedrun.fachmodell.modul import Modul, Modulstatus
from uni_speedrun.fachmodell.studienplan import Studienplan


# Fixture liefert vor jedem Test frische Modul-Objekte zurück
@pytest.fixture
def beispiel_module():
    mathe = Modul(name="mathe", ects=5, geplante_dauer_tage=14, reihenfolge=2)
    info = Modul(name="info", ects=5, geplante_dauer_tage=14, reihenfolge=3)
    datenschutz = Modul(name="datenschutz", ects=5, geplante_dauer_tage=14, reihenfolge=1)
    return mathe, info, datenschutz


def test_studienplan_mit_1_objekt(beispiel_module):
    _, info, _ = beispiel_module
    Plan1 = Studienplan([info])
    assert info in Plan1.module


def test_studienplan_mit_2_objekt(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    module_list = [mathe, info, datenschutz]

    Plan2 = Studienplan(module_list)
    assert info in Plan2.module


def test_ects_points(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    module_list = [mathe, info, datenschutz]

    info.schliesse_ab()
    Plan3 = Studienplan(module_list)

    assert Plan3.berechne_ects() == 5


def test_reihenfolge(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    module_list = [mathe, info, datenschutz]

    Plan4 = Studienplan(module_list)
    sortierte_module = Plan4.modul_reihenfolge()

    assert sortierte_module == [datenschutz, mathe, info]
    assert sortierte_module[0] == datenschutz
    assert sortierte_module[1] == mathe
    assert sortierte_module[2] == info


def test_aktives_modul(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    Plan5 = Studienplan([mathe, info, datenschutz])

    Plan5.aktiviere_modul(info)  # Über Studienplan aktivieren!
    assert Plan5.aktives_modul() == info


def test_aktiviere_modul_erfolgreich(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    Plan6 = Studienplan([mathe, info, datenschutz])

    Plan6.aktiviere_modul(mathe)
    assert mathe.status == Modulstatus.AKTIV


def test_aktiviere_zweites_modul_schleagt_fehl(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    Plan7 = Studienplan([mathe, info, datenschutz])

    Plan7.aktiviere_modul(mathe)

    # Zweites Aktivieren muss den Fehler auslösen
    with pytest.raises(ValueError):
        Plan7.aktiviere_modul(info)