from datetime import date

from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Input, Label, Select

from uni_speedrun.fachmodell.modul import Modul
from uni_speedrun.fachmodell.modulstatus import Modulstatus


class ModulBearbeitenScreen(Screen):
    BINDINGS = [
        ("escape", "abbrechen", "Abbrechen"),
    ]

    STATUS_OPTIONEN = [
        ("Geplant", Modulstatus.GEPLANT.name),
        ("Aktiv", Modulstatus.AKTIV.name),
        ("Warte auf Ergebnis", Modulstatus.WARTE_AUF_ERGEBNIS.name),
        ("Abgeschlossen", Modulstatus.ABGESCHLOSSEN.name),
    ]

    def __init__(self, modul: Modul | None, reihenfolge: int) -> None:
        super().__init__()
        self.modul = modul
        self.reihenfolge = reihenfolge

    def compose(self) -> ComposeResult:
        aktueller_status = (
            self.modul.status.name if self.modul else Modulstatus.GEPLANT.name
        )

        with Center():
            with Vertical(id="modul-editor-screen"):
                yield Label(
                    "MODUL BEARBEITEN" if self.modul else "MODUL HINZUFÜGEN",
                    classes="screen-title",
                )

                yield Label("Modulname", classes="field-label")
                yield Input(
                    value=self.modul.name if self.modul else "",
                    placeholder="z. B. Mathematik",
                    id="modulname",
                    classes="field-input",
                )

                yield Label("ECTS", classes="field-label")
                yield Input(
                    value=str(self.modul.ects) if self.modul else "5",
                    id="ects",
                    classes="field-input",
                )

                yield Label("Dauer in Tagen", classes="field-label")
                yield Input(
                    value=(
                        str(self.modul.geplante_dauer_tage)
                        if self.modul
                        else "14"
                    ),
                    id="dauer",
                    classes="field-input",
                )

                yield Label("Reihenfolge (Position)", classes="field-label")
                yield Input(
                    value=(
                        str(self.modul.reihenfolge)
                        if self.modul
                        else str(self.reihenfolge)
                    ),
                    placeholder="z. B. 1",
                    id="reihenfolge",
                    classes="field-input",
                )

                yield Label("Status", classes="field-label")
                yield Select(
                    options=self.STATUS_OPTIONEN,
                    value=aktueller_status,
                    allow_blank=False,
                    id="status",
                    classes="field-select",
                )

                yield Label("Note (optional für Abgeschlossen)", classes="field-label")
                yield Input(
                    value=(
                        f"{self.modul.note:g}"
                        if self.modul and self.modul.note is not None
                        else ""
                    ),
                    placeholder="z. B. 1.7",
                    id="note",
                    classes="field-input",
                )

                with Horizontal(classes="screen-actions"):
                    yield Button("Speichern", id="speichern")
                    yield Button("Abbrechen", id="abbrechen")

    def action_abbrechen(self) -> None:
        self.dismiss(None)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "abbrechen":
            self.dismiss(None)
            return

        if event.button.id != "speichern":
            return

        name = self.query_one("#modulname", Input).value.strip()
        ects_text = self.query_one("#ects", Input).value.strip()
        dauer_text = self.query_one("#dauer", Input).value.strip()
        reihenfolge_text = self.query_one("#reihenfolge", Input).value.strip()
        status_value = self.query_one("#status", Select).value
        note_text = self.query_one("#note", Input).value.strip()

        if not name:
            self.notify("Bitte einen Modulnamen eingeben.", severity="error")
            return

        try:
            ects = int(ects_text)
            dauer = int(dauer_text)
            reihenfolge = int(reihenfolge_text)
        except ValueError:
            self.notify("ECTS, Dauer und Reihenfolge müssen Zahlen sein.", severity="error")
            return

        if ects <= 0 or dauer <= 0 or reihenfolge <= 0:
            self.notify("ECTS, Dauer und Reihenfolge müssen größer als 0 sein.", severity="error")
            return

        note = None
        if note_text:
            try:
                note = float(note_text.replace(",", "."))
                if note < 1.0 or note > 5.0:
                    self.notify(
                        "Die Note muss zwischen 1.0 und 5.0 liegen.",
                        severity="error",
                    )
                    return
            except ValueError:
                self.notify(
                    "Bitte eine gültige Note eingeben (z. B. 1.7).",
                    severity="error",
                )
                return

        status = (
            Modulstatus[status_value]
            if status_value in Modulstatus.__members__
            else Modulstatus.GEPLANT
        )

        if self.modul is None:
            self.modul = Modul(
                name=name,
                ects=ects,
                geplante_dauer_tage=dauer,
                reihenfolge=reihenfolge,
                status=status,
            )
        else:
            self.modul.name = name
            self.modul.ects = ects
            self.modul.geplante_dauer_tage = dauer
            self.modul.reihenfolge = reihenfolge
            self.modul.status = status

        self.modul.note = note
        heute = date.today()

        if status == Modulstatus.AKTIV and self.modul.startdatum is None:
            self.modul.startdatum = heute
        elif status == Modulstatus.WARTE_AUF_ERGEBNIS:
            if self.modul.startdatum is None:
                self.modul.startdatum = heute
            if self.modul.pruefungsdatum is None:
                self.modul.pruefungsdatum = heute
        elif status == Modulstatus.ABGESCHLOSSEN:
            if self.modul.startdatum is None:
                self.modul.startdatum = heute
            if self.modul.abschlussdatum is None:
                self.modul.abschlussdatum = heute

        self.dismiss(self.modul)

