from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Label


class DashboardScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("UNI Speedrun")
        yield Label("Dashboard")
        yield Footer()