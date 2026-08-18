from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Input, Button, Static


class StartScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()

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