from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label

from uni_speedrun.fachmodell.modul import Modul


class ModulErstellenScreen(Screen):

    def __init__(self, studienplan):
        super().__init__()
        self.studienplan = studienplan

    def compose(self) -> ComposeResult:
        yield Header()

        with Center():
            with Vertical():

                yield Label(
                    "Modul erstellen",
                    id="titel",
                )

                yield Label("Modulname:")

                yield Input(
                    placeholder="z. B. Python OOP",
                    id="name",
                )

                yield Label("ECTS:")

                yield Input(
                    placeholder="z. B. 5",
                    id="ects",
                )

                yield Label("Geplante Dauer in Tagen:")

                yield Input(
                    placeholder="z. B. 14",
                    id="geplante-dauer",
                )

                yield Label("Reihenfolge:")

                yield Input(
                    placeholder="z. B. 1",
                    id="reihenfolge",
                )

                yield Button(
                    "Modul erstellen",
                    id="modul-erstellen",
                )

                yield Button(
                    "Zurück",
                    id="zurueck",
                )

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == "zurueck":
            self.app.pop_screen()
            return

        if event.button.id == "modul-erstellen":
            self.modul_erstellen()

    def modul_erstellen(self) -> None:

        name = self.query_one("#name", Input).value
        ects_text = self.query_one("#ects", Input).value
        dauer_text = self.query_one("#geplante-dauer", Input).value
        reihenfolge_text = self.query_one("#reihenfolge", Input).value

        if not name:
            self.notify(
                "Bitte einen Modulnamen eingeben.",
                severity="error",
            )
            return

        try:
            ects = int(ects_text)
            geplante_dauer = int(dauer_text)
            reihenfolge = int(reihenfolge_text)

        except ValueError:
            self.notify(
                "ECTS, Dauer und Reihenfolge müssen Zahlen sein.",
                severity="error",
            )
            return

        try:
            modul = Modul(
                name=name,
                ects=ects,
                geplante_dauer_tage=geplante_dauer,
                reihenfolge=reihenfolge,
            )

        except ValueError as fehler:
            self.notify(
                str(fehler),
                severity="error",
            )
            return

        self.studienplan.module.append(modul)

        self.app.repository.speichern(
            self.studienplan
        )

        self.notify(
            f"Modul '{modul.name}' wurde erstellt."
        )

        self.app.pop_screen()