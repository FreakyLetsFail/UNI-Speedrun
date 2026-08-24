from datetime import date
from uni_speedrun.controller.dashboard_controller import DashboardController
from uni_speedrun.database.repository import StudienplanRepository
from uni_speedrun.fachmodell.modul import Modul
from uni_speedrun.fachmodell.modulstatus import Modulstatus
from uni_speedrun.fachmodell.studienplan import Studienplan


class MockRepository(StudienplanRepository):
    def __init__(self, plan: Studienplan | None = None):
        self.plan = plan
        self.saved_count = 0

    def laden(self) -> Studienplan | None:
        return self.plan

    def speichern(self, studienplan: Studienplan) -> None:
        self.plan = studienplan
        self.saved_count += 1


def test_controller_workflow():
    m1 = Modul("Modul 1", 5, 14, 1, Modulstatus.GEPLANT)
    m2 = Modul("Modul 2", 5, 14, 2, Modulstatus.GEPLANT)
    plan = Studienplan([m1, m2], "Bachelor Cyber Security", 180, 36)
    repo = MockRepository(plan)
    controller = DashboardController(repo)

    # 1. Modul starten
    ok, msg = controller.modul_abschliessen_oder_starten()
    assert ok is True
    assert m1.status == Modulstatus.AKTIV

    # 2. Modul in Bewertung versetzen
    ok, msg = controller.modul_abschliessen_oder_starten()
    assert ok is True
    assert m1.status == Modulstatus.WARTE_AUF_ERGEBNIS

    # 3. Nächstes Modul starten
    ok, msg = controller.modul_abschliessen_oder_starten()
    assert ok is True
    assert m2.status == Modulstatus.AKTIV

    # 4. Modul 1 abschließen
    ok, msg = controller.modul_schnell_abschliessen(1)
    assert ok is True
    assert m1.status == Modulstatus.ABGESCHLOSSEN

    # 5. Verschieben und Speichern
    controller.modul_verschieben(2, nach_oben=True)
    assert m2.reihenfolge == 1
    assert m1.reihenfolge == 2
