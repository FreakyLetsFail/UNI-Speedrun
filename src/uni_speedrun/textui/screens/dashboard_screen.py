from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static

from uni_speedrun.fachmodell.studienplan import Studienplan


class DashboardScreen(Screen):

    def __init__(self, studienplan: Studienplan | None) -> None:
        super().__init__()

        self.studienplan = studienplan

    def compose(self) -> ComposeResult:
        yield Header()

        if self.studienplan is None:
            yield Static("Noch kein Studienplan vorhanden.")
        else:
            yield Static(
                f"Studienziel: {self.studienplan.studienziel_name}"
            )

        yield Footer()