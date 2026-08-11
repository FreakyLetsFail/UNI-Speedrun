from uni_speedrun.fachmodell.studienplan import Studienplan
from uni_speedrun.fachmodell.modul import Modul

mathe = Modul(
        name="mathe",
        ects=5,
        geplante_dauer_tage=14,
        reihenfolge=2,
    )

info = Modul(
        name="info",
        ects=5,
        geplante_dauer_tage=14,
        reihenfolge=3,
    )

datenschutz = Modul(
        name="datenschutz",
        ects=5,
        geplante_dauer_tage=14,
        reihenfolge=1,
    )


module_list = [mathe,info, datenschutz]

def test_studienplan_mit_1_objekt():
    Plan1 = Studienplan([info])

    assert info in Plan1.module 


def test_studienplan_mit_2_objekt():
    Plan2 = Studienplan(module_list)

    assert info in Plan2.module 


def test_ects_points():
    info.schliesse_ab()
    print("STATUS VON INFO:", info.status)
    Plan3 = Studienplan(module_list)

    assert Plan3.berechne_ects() == 5

def test_reihenfolge():
    Plan4 = Studienplan(module_list)

    sortierte_module = Plan4.modul_reihenfolge()

    assert sortierte_module == [datenschutz, mathe, info]
    
    # Optional: Einzelne Indizes explizit prüfen
    assert sortierte_module[0] == datenschutz
    assert sortierte_module[1] == mathe
    assert sortierte_module[2] == info

def test_aktives_modul():
    Plan5 = Studienplan(module_list)
    info.aktivieren()
    ## mathe.aktivieren() <-- Müsste RunTimeError ausgeben und nicht absturz 

    assert Plan5.aktives_modul() == info
