from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

from uni_speedrun.database.repository import StudienplanRepository


class UniSpeedrunApp(App):
    """Textual-Anwendung für UNI Speedrun."""

    TITLE = "UNI Speedrun"

    def __init__(self, repository: StudienplanRepository) -> None:
        super().__init__()

        self.repository = repository
        self.studienplan = repository.laden()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Willkommen bei UNI Speedrun!")
        yield Footer()