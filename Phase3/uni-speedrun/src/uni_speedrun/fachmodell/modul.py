from datetime import date, timedelta

from .modulstatus import Modulstatus


class Modul:
    def __init__(
        self,
        name: str,
        ects: int,
        geplante_dauer_tage: int,
        reihenfolge: int,
        status: Modulstatus = Modulstatus.GEPLANT,
        startdatum: date | None = None,
        pruefungsdatum: date | None = None,
        abschlussdatum: date | None = None,
    ) -> None:
        if not name:
            raise ValueError("Der Modulname darf nicht leer sein.")
        self.name = name

        if ects <= 0:
            raise ValueError("ECTS müssen größer als 0 sein.")
        self.ects = ects

        if geplante_dauer_tage <= 0:
            raise ValueError("Die geplante Dauer muss größer als 0 sein.")
        self.geplante_dauer_tage = geplante_dauer_tage

        if reihenfolge <= 0:
            raise ValueError("Die Reihenfolge muss größer als 0 sein.")
        self.reihenfolge = reihenfolge

        self.status = status
        self.startdatum = startdatum
        self.pruefungsdatum = pruefungsdatum
        self.abschlussdatum = abschlussdatum
        self.note = None

    def _aktivieren(self, startdatum: date | None = None) -> None:
        self.status = Modulstatus.AKTIV
        self.startdatum = startdatum or date.today()

    def _warte_auf_ergebnis(self, pruefungsdatum: date | None = None) -> None:
        self.status = Modulstatus.WARTE_AUF_ERGEBNIS
        self.pruefungsdatum = pruefungsdatum or date.today()

    def _schliesse_ab(self, abschlussdatum: date | None = None) -> None:
        self.status = Modulstatus.ABGESCHLOSSEN
        self.abschlussdatum = abschlussdatum or date.today()

    def berechne_enddatum(self) -> date | None:
        if self.startdatum is None:
            return None

        return self.startdatum + timedelta(
            days=self.geplante_dauer_tage
        )

    def berechne_aktive_tage(self, heute: date | None = None) -> int:
        if self.startdatum is None:
            return 0

        enddatum = self.abschlussdatum or heute or date.today()
        return (enddatum - self.startdatum).days

    def berechne_restzeit(self, heute: date | None = None) -> int:
        enddatum = self.berechne_enddatum()

        if enddatum is None:
            return 0

        vergleichsdatum = heute or date.today()
        return (enddatum - vergleichsdatum).days