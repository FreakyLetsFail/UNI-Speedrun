from textual.app import App

from uni_speedrun.database.repository import StudienplanRepository
from uni_speedrun.textui.screens.dashboard_screen import DashboardScreen


class UniSpeedrunApp(App):

    TITLE = "UNI Speedrun"

    def __init__(self, repository: StudienplanRepository) -> None:
        super().__init__()

        self.repository = repository
        self.studienplan = repository.laden()

    def on_mount(self) -> None:
        self.push_screen(
            DashboardScreen(self.studienplan)
        )