
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
def test_zieldatum_studienplan(beispiel_module):
    test2 = Studienplan(beispiel_module, "Bachelor Cyber Security", 180, 15)
    assert test2.zieldatum() == date(2027, 11, 13) ## Schlägt fehl - muss immer an den letzten Konsturktor aufruf angepasst werden. 

#Überprüfung, ob mehrere Objekte richtig übergeben werden 
def test_studienplan_mit_2_objekt(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    test3 = Studienplan(beispiel_module, "Bachelor Cyber Security", 180, 15)
    
    assert mathe in test3.module
    assert info in test3.module
    assert datenschutz in test3.module

#Überprüfung ob die Studienziele richtig verarbeitet werden
def test_studienziele(beispiel_module):
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
    test6.aktiviere_modul(datenschutz)
    test6.schliesse_modul_ab(datenschutz)
    assert test6.fortschritt_prozent() == 2.78

def test_aktiviere_naechstes_modul(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    test7 = Studienplan(beispiel_module, "Bachelor Cyber Security", 180, 15)
    test7.aktiviere_modul(test7.naechstes_modul())

    assert test7.zeige_aktives_modul() == datenschutz


def test_aktiviere_falsches_modul(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    test8 = Studienplan(beispiel_module, "Bachelor Cyber Security", 180, 15)
    with pytest.raises(ValueError):
        test8.aktiviere_modul(mathe)

def test_aktiviere_modul_wenn_bereits_eines_aktiv_ist(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    test9 = Studienplan(beispiel_module, "Bachelor Cyber Security", 180, 15)
    test9.aktiviere_modul(test9.naechstes_modul())
    with pytest.raises(ValueError):
        test9.aktiviere_modul(info)

def test_aktiviere_naechstes_modul_nach_abschluss(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    test10 = Studienplan(beispiel_module, "Bachelor Cyber Security", 180, 15)
    assert test10.naechstes_modul() == datenschutz

    test10.aktiviere_modul(test10.naechstes_modul())
    test10.schliesse_modul_ab(datenschutz)
    assert datenschutz.status == Modulstatus.ABGESCHLOSSEN
    assert test10.naechstes_modul() == mathe
    test10.aktiviere_modul(test10.naechstes_modul())

def test_naechstes_modul_trotz_warten_auf_ergebnis(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    test11 = Studienplan(beispiel_module, "Bachelor Cyber Security", 180, 15)

    test11.aktiviere_modul(datenschutz)

    test11.modul_in_bewertung_versetzen(datenschutz)

    assert datenschutz.status == Modulstatus.WARTE_AUF_ERGEBNIS
    assert test11.naechstes_modul() == mathe

    test11.aktiviere_modul(test11.naechstes_modul())

    assert test11.zeige_aktives_modul() == mathe


def test_bewertung_nur_fuer_aktives_modul(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    test12 = Studienplan(beispiel_module, "Bachelor Cyber Security", 180, 15)

    with pytest.raises(ValueError):
        test12.modul_in_bewertung_versetzen(datenschutz)


def test_modul_in_bewertung_nicht_doppelt(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    test13 = Studienplan(beispiel_module, "Bachelor Cyber Security", 180, 15)

    test13.aktiviere_modul(datenschutz)
    test13.modul_in_bewertung_versetzen(datenschutz)

    with pytest.raises(ValueError):
        test13.modul_in_bewertung_versetzen(datenschutz)


def test_ergebnis_eintragen_bestanden(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    test14 = Studienplan(beispiel_module, "Bachelor Cyber Security", 180, 15)

    test14.aktiviere_modul(datenschutz)
    test14.modul_in_bewertung_versetzen(datenschutz)
    test14.ergebnis_eintragen(datenschutz, True, 2.1)

    assert datenschutz.status == Modulstatus.ABGESCHLOSSEN
    assert datenschutz.note == 2.1

def test_ergebnis_eintragen_nicht_bestanden(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    test15 = Studienplan(beispiel_module, "Bachelor Cyber Security", 180, 15)

    test15.aktiviere_modul(datenschutz)
    test15.modul_in_bewertung_versetzen(datenschutz)
    test15.ergebnis_eintragen(datenschutz, False, 5.0)

    assert datenschutz.status == Modulstatus.GEPLANT


def test_ergebnis_eintragen_bestanden_falsche_note(beispiel_module):
    mathe, info, datenschutz = beispiel_module
    test16 = Studienplan(beispiel_module, "Bachelor Cyber Security", 180, 15)

    test16.aktiviere_modul(datenschutz)
    test16.modul_in_bewertung_versetzen(datenschutz)


    with pytest.raises(ValueError):
        test16.ergebnis_eintragen(datenschutz, True, 5.0)



def test_aktualisiere_zeitplan(beispiel_module):
    mathe, info, datenschutz = beispiel_module

    test17 = Studienplan(
        beispiel_module,
        "Bachelor Cyber Security",
        180,
        15
    )

    test17.startdatum = date(2026, 9, 1)

    test17.aktualisiere_zeitplan()

    assert datenschutz.startdatum == date(2026, 9, 1)
    assert mathe.startdatum == date(2026, 9, 15)
    assert info.startdatum == date(2026, 9, 29)


def test_aktualisiere_zeitplan_ueberspringt_abgeschlossene_module(beispiel_module):
    mathe, info, datenschutz = beispiel_module

    test18 = Studienplan(
        beispiel_module,
        "Bachelor Cyber Security",
        180,
        15
    )

    datenschutz._aktivieren(date(2026, 8, 1))
    datenschutz._schliesse_ab(date(2026, 8, 10))

    test18.startdatum = date(2026, 9, 1)

    test18.aktualisiere_zeitplan()

    assert mathe.startdatum == date(2026, 9, 1)
    assert info.startdatum == date(2026, 9, 15)


def test_aktualisiere_zeitplan_warte_auf_ergebnis(beispiel_module):
    mathe, info, datenschutz = beispiel_module

    test19 = Studienplan(
        beispiel_module,
        "Bachelor Cyber Security",
        180,
        15
    )

    test19.startdatum = date(2026, 9, 1)

    datenschutz._aktivieren(date(2026, 9, 1))
    datenschutz._warte_auf_ergebnis(date(2026, 9, 9))

    test19.aktualisiere_zeitplan()

    assert mathe.startdatum == date(2026, 9, 9)


def test_aktualisiere_zeitplan_nach_nicht_bestanden(beispiel_module):
    mathe, info, datenschutz = beispiel_module

    test20 = Studienplan(
        beispiel_module,
        "Bachelor Cyber Security",
        180,
        15
    )

    test20.startdatum = date(2026, 9, 1)

    datenschutz._aktivieren(date(2026, 9, 1))
    datenschutz._warte_auf_ergebnis(date(2026, 9, 9))

    # Prüfung nicht bestanden
    test20.ergebnis_eintragen(
        datenschutz,
        bestanden=False,
        note=None
    )

    assert datenschutz.status == Modulstatus.GEPLANT

    # Mathe wird zuerst bearbeitet
    mathe._aktivieren(date(2026, 9, 9))
    mathe._schliesse_ab(date(2026, 9, 23))

    test20.aktualisiere_zeitplan()

    assert datenschutz.startdatum == date(2026, 9, 23)
    assert datenschutz.geplante_dauer_tage == 14

def test_prognostiziertes_studienende(beispiel_module):
    test21 = Studienplan(
        beispiel_module,
        "Bachelor Cyber Security",
        180,
        15
    )

    test21.startdatum = date(2026, 9, 1)

    assert plan.prognostiziertes_studienende() == date(2026, 10, 13)

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