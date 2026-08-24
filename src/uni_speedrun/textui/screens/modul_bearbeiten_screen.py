from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Button, Input, Label

from uni_speedrun.fachmodell.modul import Modul


class ModulBearbeitenScreen(Screen):
    """Kleiner Editor für ein einzelnes Modul."""

    def __init__(self, modul: Modul | None, reihenfolge: int) -> None:
        super().__init__()
        self.modul = modul
        self.reihenfolge = reihenfolge

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="settings-screen"):
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

                with Vertical(classes="screen-actions"):
                    yield Button("Speichern", id="speichern")
                    yield Button("Abbrechen", id="abbrechen")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "abbrechen":
            self.app.pop_screen()
            return

        if event.button.id != "speichern":
            return

        name = self.query_one("#modulname", Input).value.strip()
        ects_text = self.query_one("#ects", Input).value.strip()
        dauer_text = self.query_one("#dauer", Input).value.strip()

        if not name:
            self.notify("Bitte einen Modulnamen eingeben.", severity="error")
            return

        try:
            ects = int(ects_text)
            dauer = int(dauer_text)
        except ValueError:
            self.notify("ECTS und Dauer müssen Zahlen sein.", severity="error")
            return

        try:
            if self.modul is None:
                self.modul = Modul(
                    name,
                    ects,
                    dauer,
                    self.reihenfolge,
                )
            else:
                self.modul.name = name
                self.modul.ects = ects
                self.modul.geplante_dauer_tage = dauer

        except ValueError as error:
            self.notify(str(error), severity="error")
            return

        self.app.pop_screen(result=self.modul)
