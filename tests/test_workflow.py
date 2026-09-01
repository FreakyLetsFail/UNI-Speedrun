from datetime import date
import pytest

from uni_speedrun.database.sqlite_repository import SQLiteStudienplanRepository
from uni_speedrun.fachmodell.modul import Modul
from uni_speedrun.fachmodell.modulstatus import Modulstatus
from uni_speedrun.fachmodell.studienplan import Studienplan


def test_kompletter_modul_lebenszyklus(tmp_path):
    datenbank = tmp_path / "test_lifecycle.db"
    repo = SQLiteStudienplanRepository(str(datenbank))

    modul1 = Modul(
        name="Python OOP",
        ects=5,
        geplante_dauer_tage=14,
        reihenfolge=1,
    )
    modul2 = Modul(
        name="Wissenschaftliches Arbeiten",
        ects=5,
        geplante_dauer_tage=14,
        reihenfolge=2,
    )

    plan = Studienplan(
        [modul1, modul2],
        "Bachelor Cyber Security",
        180,
        15,
        startdatum=date(2026, 8, 1),
    )

    plan.aktiviere_modul(modul1)
    assert modul1.status == Modulstatus.AKTIV
    assert plan.zeige_aktives_modul() == modul1

    plan.modul_in_bewertung_versetzen(modul1)
    assert modul1.status == Modulstatus.WARTE_AUF_ERGEBNIS
    assert plan.zeige_aktives_modul() is None

    assert plan.naechstes_modul() == modul2
    plan.aktiviere_modul(modul2)
    assert modul2.status == Modulstatus.AKTIV

    plan.ergebnis_eintragen(modul1, bestanden=True, note=1.3)
    assert modul1.status == Modulstatus.ABGESCHLOSSEN
    assert modul1.note == 1.3
    assert plan.erreichte_ects() == 5

    repo.speichern(plan)
    geladener_plan = repo.laden()

    assert geladener_plan is not None
    assert geladener_plan.erreichte_ects() == 5
    m1 = geladener_plan.module[0]
    m2 = geladener_plan.module[1]
    assert m1.status == Modulstatus.ABGESCHLOSSEN
    assert m1.note == 1.3
    assert m2.status == Modulstatus.AKTIV
