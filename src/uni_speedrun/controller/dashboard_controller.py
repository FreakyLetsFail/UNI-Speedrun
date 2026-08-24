from datetime import date

from uni_speedrun.database.repository import StudienplanRepository
from uni_speedrun.fachmodell.modul import Modul
from uni_speedrun.fachmodell.modulstatus import Modulstatus
from uni_speedrun.fachmodell.pruefungsleistung import Pruefungsleistung
from uni_speedrun.fachmodell.studienplan import Studienplan


class DashboardController:
    """Koordiniert die Anwendungslogik, Benutzeraktionen und die Persistenz."""

    def __init__(self, repository: StudienplanRepository) -> None:
        self.repository = repository
        self.studienplan: Studienplan | None = self.repository.laden()

    def lade_studienplan(self) -> Studienplan | None:
        self.studienplan = self.repository.laden()
        return self.studienplan

    def speichere_studienplan(self) -> None:
        if self.studienplan is not None:
            self.repository.speichern(self.studienplan)

    def modul_abschliessen_oder_starten(self) -> tuple[bool, str]:
        """Verarbeitet die Schnell-Aktion [M] auf dem Dashboard."""
        if self.studienplan is None:
            return False, "Kein Studienplan vorhanden."

        aktives = self.studienplan.zeige_aktives_modul()

        if aktives is None:
            naechstes = self.studienplan.naechstes_geplantes_modul()
            if naechstes is None:
                return False, "Alle Module sind bereits abgeschlossen."

            self.studienplan.aktiviere_modul(naechstes)
            self.speichere_studienplan()
            return True, f"{naechstes.name} wurde gestartet."
        else:
            self.studienplan.modul_in_bewertung_versetzen(aktives)
            self.speichere_studienplan()
            return True, f"{aktives.name} wartet jetzt auf das Ergebnis."

    def modul_schnell_abschliessen(self, reihenfolge: int) -> tuple[bool, str]:
        if self.studienplan is None:
            return False, "Kein Studienplan vorhanden."

        modul = next((m for m in self.studienplan.module if m.reihenfolge == reihenfolge), None)
        if modul is None:
            return False, "Modul nicht gefunden."

        modul.status = Modulstatus.ABGESCHLOSSEN
        if modul.abschlussdatum is None:
            modul.abschlussdatum = date.today()

        self.speichere_studienplan()
        return True, f"{modul.name} auf 'Abgeschlossen' gesetzt."

    def modul_verschieben(self, reihenfolge: int, nach_oben: bool) -> None:
        if self.studienplan is None:
            return

        module = self.studienplan.modul_reihenfolge()
        ziel_reihenfolge = reihenfolge - 1 if nach_oben else reihenfolge + 1

        modul_a = next((m for m in module if m.reihenfolge == reihenfolge), None)
        modul_b = next((m for m in module if m.reihenfolge == ziel_reihenfolge), None)

        if modul_a and modul_b:
            modul_a.reihenfolge, modul_b.reihenfolge = (
                modul_b.reihenfolge,
                modul_a.reihenfolge,
            )
            self.speichere_studienplan()

    def modul_speichern(self, modul: Modul) -> None:
        if self.studienplan is None:
            return

        if modul not in self.studienplan.module:
            self.studienplan.module.append(modul)

        andere = [m for m in self.studienplan.module if m != modul]
        andere.sort(key=lambda m: m.reihenfolge)

        ziel_index = max(0, min(modul.reihenfolge - 1, len(andere)))
        andere.insert(ziel_index, modul)

        for index, m in enumerate(andere, start=1):
            m.reihenfolge = index

        self.studienplan.module = andere
        self.speichere_studienplan()

    def modul_loeschen(self, reihenfolge: int) -> tuple[bool, str]:
        if self.studienplan is None:
            return False, "Kein Studienplan vorhanden."

        modul = next((m for m in self.studienplan.module if m.reihenfolge == reihenfolge), None)
        if modul is None:
            return False, "Modul nicht gefunden."

        self.studienplan.module.remove(modul)
        for nummer, m in enumerate(self.studienplan.modul_reihenfolge(), start=1):
            m.reihenfolge = nummer

        self.speichere_studienplan()
        return True, f"{modul.name} wurde entfernt."

    def aktualisiere_plan_daten(
        self,
        studienziel: str,
        zielects: int,
        zieldauer: int,
        startdatum: date,
    ) -> None:
        if self.studienplan is None:
            self.studienplan = Studienplan(
                module=[],
                studienziel_name=studienziel,
                zielects=zielects,
                zieldauer=zieldauer,
                startdatum=startdatum,
            )
        else:
            self.studienplan.studienziel_name = studienziel
            self.studienplan.zielects = zielects
            self.studienplan.zieldauer = zieldauer
            self.studienplan.startdatum = startdatum

        self.speichere_studienplan()
