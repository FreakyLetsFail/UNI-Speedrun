
from datetime import date
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

#Überprüfung, ob ein Objekt alleine richtig übergeben werden kann.
def test_studienplan_mit_1_objekt(beispiel_module):
    _, info, _ = beispiel_module
    test1 = Studienplan([info], "Bachelor Cyber Security", 180, 15)
    assert info in test1.module

#Überprüfung, ob das gewünschte Zieldatum richtig berechnet wird
def test_zieldatum_studienplan():
    test2 = Studienplan([beispiel_module], "Bachelor Cyber Security", 180, 15)
    assert test2.zieldatum() == date(2027, 11, 12)

#Überprüfung, ob mehrere Objekte richtig übergeben werden 
def test_studienplan_mit_2_objekt(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    test3 = Studienplan(beispiel_module, "Bachelor Cyber Security", 180, 15)
    
    assert mathe in test3.module
    assert info in test3.module
    assert datenschutz in test3.module



#Überprüfung ob die Studienziele richtig verarbeitet werden
def test_studienziele():
    test4 = Studienplan(beispiel_module, "Bachelor Cyber Security", 180, 15)
    
    assert test4.studienziel_name == "Bachelor Cyber Security"
    assert test4.zielects == 180
    assert test4.zieldauer == 15

#Überprüfung ob ECTS richtig ausgegeben werden
def test_ects_points(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    test5 = Studienplan(beispiel_module, "Bachelor Cyber Security", 180, 15)
    info._schliesse_ab()
    assert test5.erreichte_ects() == 5


#Überprüfung ob Prozentfortschritt richtig ausgegeben wird
def test_fortschritt_prozent(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    test6 = Studienplan(beispiel_module, "Bachelor Cyber Security", 180, 15)
    info._schliesse_ab()
    assert test6.fortschritt_prozent() == 2.78


"""






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

"""