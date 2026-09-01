from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label
from uni_speedrun.database.repository import StudienplanRepository
from uni_speedrun.fachmodell.studienplan import Studienplan
from uni_speedrun.textui.screens.modul_erstellen_screen import (ModulErstellenScreen,)
class StudienplanErstellenScreen(Screen):

    def __init__(self, repository: StudienplanRepository | None = None) -> None:
        super().__init__()
        self.repository = repository

    def compose(self) -> ComposeResult:
        yield Header()

        with Center():
            with Vertical():

                yield Label(
                    "Studienplan erstellen",
                    id="titel",
                )

                yield Label("Studienziel:")

                yield Input(
                    placeholder="z. B. Bachelor Cyber Security",
                    id="studienziel",
                )

                yield Label("Ziel-ECTS:")

                yield Input(
                    placeholder="z. B. 180",
                    id="zielects",
                )

                yield Label("Zieldauer in Monaten:")

                yield Input(
                    placeholder="z. B. 15",
                    id="zieldauer",
                )

                yield Button(
                    "Studienplan erstellen",
                    id="studienplan-erstellen",
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

        if event.button.id == "studienplan-erstellen":
            self.studienplan_erstellen()
    
    def studienplan_erstellen(self) -> None:

        studienziel = self.query_one("#studienziel", Input).value
        zielects_text = self.query_one("#zielects", Input).value
        zieldauer_text = self.query_one("#zieldauer", Input).value

        if not studienziel:
            self.notify(
                "Bitte ein Studienziel eingeben.",
                severity="error",
            )
            return

        try:
            zielects = int(zielects_text)
            zieldauer = int(zieldauer_text)

        except ValueError:
            self.notify(
                "ECTS und Zieldauer müssen Zahlen sein.",
                severity="error",
            )
            return

        if zielects <= 0 or zieldauer <= 0:
            self.notify(
                "ECTS und Zieldauer müssen größer als 0 sein.",
                severity="error",
            )
            return

        studienplan = Studienplan(
            [],
            studienziel,
            zielects,
            zieldauer,
        )

        self.app.push_screen(
            ModulErstellenScreen(studienplan)
        )
