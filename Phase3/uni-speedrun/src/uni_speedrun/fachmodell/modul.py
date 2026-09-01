from datetime import date, timedelta

from .modulstatus import Modulstatus
from .pruefungsleistung import Pruefungsleistung


class Modul:
    """Repräsentiert ein einzelnes Studienmodul mit validierenden Properties."""

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
        pruefungsleistung: Pruefungsleistung | None = None,
    ) -> None:
        self.name = name
        self.ects = ects
        self.geplante_dauer_tage = geplante_dauer_tage
        self.reihenfolge = reihenfolge
        self.status = status
        self.startdatum = startdatum
        self.pruefungsdatum = pruefungsdatum
        self.abschlussdatum = abschlussdatum
        self._pruefungsleistung = pruefungsleistung
        if pruefungsleistung and pruefungsleistung.datum and not pruefungsdatum:
            self.pruefungsdatum = pruefungsleistung.datum

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Der Modulname darf nicht leer sein.")
        self._name = value.strip()

    @property
    def ects(self) -> int:
        return self._ects

    @ects.setter
    def ects(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ECTS müssen größer als 0 sein.")
        self._ects = value

    @property
    def geplante_dauer_tage(self) -> int:
        return self._geplante_dauer_tage

    @geplante_dauer_tage.setter
    def geplante_dauer_tage(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Die geplante Dauer muss größer als 0 sein.")
        self._geplante_dauer_tage = value

    @property
    def reihenfolge(self) -> int:
        return self._reihenfolge

    @reihenfolge.setter
    def reihenfolge(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Die Reihenfolge muss größer als 0 sein.")
        self._reihenfolge = value

    @property
    def pruefungsleistung(self) -> Pruefungsleistung | None:
        return self._pruefungsleistung

    @pruefungsleistung.setter
    def pruefungsleistung(self, value: Pruefungsleistung | None) -> None:
        self._pruefungsleistung = value
        if value and value.datum:
            self.pruefungsdatum = value.datum

    @property
    def note(self) -> float | None:
        if self._pruefungsleistung is not None:
            return self._pruefungsleistung.note
        return getattr(self, "_note", None)

    @note.setter
    def note(self, value: float | None) -> None:
        self._note = value
        if self._pruefungsleistung is not None:
            self._pruefungsleistung.note = value
        elif value is not None:
            self._pruefungsleistung = Pruefungsleistung(
                titel=f"Prüfung {self.name}",
                datum=self.pruefungsdatum or self.abschlussdatum,
                note=value,
            )

    def _aktivieren(self, startdatum: date | None = None) -> None:
        self.status = Modulstatus.AKTIV
        self.startdatum = startdatum or date.today()

    def _warte_auf_ergebnis(self, pruefungsdatum: date | None = None) -> None:
        self.status = Modulstatus.WARTE_AUF_ERGEBNIS
        datum = pruefungsdatum or date.today()
        self.pruefungsdatum = datum
        if self._pruefungsleistung is None:
            self._pruefungsleistung = Pruefungsleistung(
                titel=f"Prüfung {self.name}",
                datum=datum,
            )
        else:
            self._pruefungsleistung.datum = datum

    def _schliesse_ab(self, abschlussdatum: date | None = None) -> None:
        self.status = Modulstatus.ABGESCHLOSSEN
        datum = abschlussdatum or date.today()
        self.abschlussdatum = datum
        if self._pruefungsleistung is not None and self._pruefungsleistung.datum is None:
            self._pruefungsleistung.datum = datum

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