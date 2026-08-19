from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Input, Button, Static

class StartScreen(Screen):

    def compose(self) -> ComposeResult:

        yield Static(
            "Willkommen bei UNI Speedrun!"
        )

        yield Static(
            "Bitte gib den Pfad zur SQLite-Datenbank ein:"
        )

        yield Input(
            placeholder="z.B. UniSpeedrun.db",
            id="datenbank_pfad",
        )

        yield Button(
            "Datenbank öffnen",
            id="datenbank_oeffnen",
        )

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "datenbank_oeffnen":
            datenbank_pfad = self.query_one(
                "#datenbank_pfad",
                Input
            ).value

            self.app.oeffne_datenbank(datenbank_pfad)