from datetime import date

from dateutil.relativedelta import relativedelta

from .modul import Modul
from .modulstatus import Modulstatus


class Studienplan:
    def __init__(
        self,
        module: list[Modul],
        studienziel_name: str,
        zielects: int,
        zieldauer: int,
        startdatum: date | None = None,
    ) -> None:
        self.module = list(module) if module is not None else []
        self._pruefe_reihenfolge()
        self.studienziel_name = studienziel_name
        self.zielects = zielects
        self.zieldauer = zieldauer
        self.startdatum = startdatum or date.today()

    @property
    def studienziel_name(self) -> str:
        return self._studienziel_name

    @studienziel_name.setter
    def studienziel_name(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Der Name des Studienziels darf nicht leer sein.")
        self._studienziel_name = value.strip()

    @property
    def zielects(self) -> int:
        return self._zielects

    @zielects.setter
    def zielects(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Ziel-ECTS müssen eine Zahl größer als 0 sein.")
        self._zielects = value

    @property
    def zieldauer(self) -> int:
        return self._zieldauer

    @zieldauer.setter
    def zieldauer(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Zieldauer muss eine Zahl größer als 0 sein.")
        self._zieldauer = value

    def _pruefe_reihenfolge(self) -> None:
        reihenfolge = [modul.reihenfolge for modul in self.module]
        if len(reihenfolge) != len(set(reihenfolge)):
            raise ValueError(
                "Jedes Modul muss eine eindeutige Reihenfolge haben."
            )


    def zieldatum(self) -> date:
        return self.startdatum + relativedelta(months=self.zieldauer)

    def erreichte_ects(self) -> int:
        ects_points = 0

        for modul in self.module:
            if modul.status == Modulstatus.ABGESCHLOSSEN:
                ects_points += modul.ects

        return ects_points

    def fortschritt_prozent(self) -> float:
        return round((self.erreichte_ects() / self.zielects) * 100, 2)

    def modul_reihenfolge(self) -> list[Modul]:
        return sorted(self.module, key=lambda x: x.reihenfolge)

    def zeige_aktives_modul(self) -> Modul | None:
        for modul in self.module:
            if modul.status == Modulstatus.AKTIV:
                return modul

        return None

    def aktiviere_modul(self, modul: Modul) -> None:
        aktives = self.zeige_aktives_modul()
        if aktives is not None:
            raise ValueError(
                f"Aktivieren nicht möglich! "
                f"Das Modul {aktives.name} ist bereits aktiv."
            )

        naechstes = self.naechstes_modul()
        if naechstes is None:
            raise ValueError("Es gibt kein geplantes Modul mehr.")

        if modul != naechstes:
            raise ValueError(
                f"Aktivieren nicht möglich! "
                f"Das nächste Modul ist {naechstes.name}."
            )

        modul._aktivieren()

    def schliesse_modul_ab(self, modul: Modul) -> None:
        if modul.status == Modulstatus.ABGESCHLOSSEN:
            raise ValueError(
                f"Das Modul {modul.name} ist bereits abgeschlossen."
            )

        if modul.status != Modulstatus.AKTIV:
            raise ValueError(
                f"Das Modul {modul.name} ist nicht aktiv "
                "und kann nicht abgeschlossen werden."
            )

        modul._schliesse_ab()

    def modul_in_bewertung_versetzen(self, modul: Modul) -> None:
        if modul.status == Modulstatus.WARTE_AUF_ERGEBNIS:
            raise ValueError(
                f"Das Modul {modul.name} ist bereits auf "
                "WARTE_AUF_ERGEBNIS."
            )

        if modul.status != Modulstatus.AKTIV:
            raise ValueError(
                f"Das Modul {modul.name} ist nicht aktiv und kann "
                "nicht auf WARTE_AUF_ERGEBNIS gesetzt werden."
            )

        modul._warte_auf_ergebnis()

    def naechstes_geplantes_modul(self) -> Modul | None:
        offene_module = [
            modul
            for modul in self.module
            if modul.status == Modulstatus.GEPLANT
        ]

        if not offene_module:
            return None

        return min(
            offene_module,
            key=lambda modul: modul.reihenfolge,
        )

    def naechstes_modul(self) -> Modul | None:
        if self.zeige_aktives_modul() is not None:
            raise ValueError("Es ist bereits ein Modul aktiv.")

        return self.naechstes_geplantes_modul()

    def ergebnis_eintragen(
        self,
        modul: Modul,
        bestanden: bool,
        note: float,
    ) -> None:
        if modul.status != Modulstatus.WARTE_AUF_ERGEBNIS:
            raise ValueError(
                "Das ausgewählte Modul hat derzeit nicht den Status "
                "WARTE_AUF_ERGEBNIS."
            )

        if bestanden:
            if note < 1 or note > 4:
                raise ValueError(
                    "Zum Bestehen muss die Note zwischen 1 und 4 liegen."
                )

            modul.note = note
            modul._schliesse_ab()

        else:
            modul.status = Modulstatus.GEPLANT
            modul.startdatum = None
            modul.pruefungsdatum = None
            modul.note = None

    def aktualisiere_zeitplan(self) -> None:
        aktuelles_datum = self.startdatum

        for modul in self.module:
            if modul.status == Modulstatus.ABGESCHLOSSEN:
                if (
                    modul.abschlussdatum is not None
                    and modul.abschlussdatum > aktuelles_datum
                ):
                    aktuelles_datum = modul.abschlussdatum

            elif modul.status == Modulstatus.WARTE_AUF_ERGEBNIS:
                if (
                    modul.pruefungsdatum is not None
                    and modul.pruefungsdatum > aktuelles_datum
                ):
                    aktuelles_datum = modul.pruefungsdatum

        for modul in self.modul_reihenfolge():

            if modul.status == Modulstatus.ABGESCHLOSSEN:
                continue

            if modul.status == Modulstatus.WARTE_AUF_ERGEBNIS:
                continue

            if modul.status == Modulstatus.AKTIV:
                if (
                    modul.startdatum is None
                    or modul.startdatum < aktuelles_datum
                ):
                    modul.startdatum = aktuelles_datum

                aktuelles_datum = (
                    modul.startdatum
                    + relativedelta(days=modul.geplante_dauer_tage)
                )

            elif modul.status == Modulstatus.GEPLANT:
                modul.startdatum = aktuelles_datum

                aktuelles_datum = (
                    modul.startdatum
                    + relativedelta(days=modul.geplante_dauer_tage)
                )

    def prognostiziertes_studienende(self) -> date | None:
        self.aktualisiere_zeitplan()

        offene_module = [
            modul
            for modul in self.module
            if modul.status != Modulstatus.ABGESCHLOSSEN
        ]

        if not offene_module:
            return None

        letztes_modul = max(
            offene_module,
            key=lambda modul: modul.startdatum
        )

        return letztes_modul.startdatum + relativedelta(
            days=letztes_modul.geplante_dauer_tage
        )

    def abweichung_zum_zieldatum(self):
        prognose = self.prognostiziertes_studienende()

        if prognose is None:
            return None

        return prognose - self.zieldatum()
