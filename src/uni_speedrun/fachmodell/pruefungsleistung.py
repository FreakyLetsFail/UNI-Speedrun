from datetime import date


class Pruefungsleistung:
    """Repräsentiert die Prüfungsleistung eines Moduls (z. B. Klausur, Projekt, Portfolio)."""

    def __init__(
        self,
        titel: str,
        datum: date | None = None,
        note: float | None = None,
        bestanden: bool | None = None,
    ) -> None:
        self._note = None
        self._bestanden = bestanden
        self.titel = titel
        self.datum = datum
        self.note = note
        if bestanden is not None:
            self.bestanden = bestanden


    @property
    def titel(self) -> str:
        return self._titel

    @titel.setter
    def titel(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Der Titel der Prüfungsleistung darf nicht leer sein.")
        self._titel = value.strip()

    @property
    def note(self) -> float | None:
        return self._note

    @note.setter
    def note(self, value: float | None) -> None:
        if value is not None:
            if not isinstance(value, (int, float)):
                raise ValueError("Die Note muss eine Zahl sein.")
            if value < 1.0 or value > 5.0:
                raise ValueError("Die Note muss zwischen 1.0 und 5.0 liegen.")
            self._note = float(value)
            if self.bestanden is None:
                self.bestanden = self._note <= 4.0
        else:
            self._note = None

    @property
    def bestanden(self) -> bool | None:
        return self._bestanden

    @bestanden.setter
    def bestanden(self, value: bool | None) -> None:
        self._bestanden = value

    def ist_bewertet(self) -> bool:
        return self._note is not None

    def ist_bestanden(self) -> bool:
        if self._note is not None:
            return self._note <= 4.0
        return bool(self._bestanden)

