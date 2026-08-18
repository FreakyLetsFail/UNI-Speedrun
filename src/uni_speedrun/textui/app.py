from textual.app import App

from uni_speedrun.database.sqlite_repository import SQLiteStudienplanRepository
from uni_speedrun.textui.screens.dashboard_screen import DashboardScreen


class UniSpeedrunApp(App):

    def __init__(self, repository=None):
        super().__init__()
        self.repository = repository

    def zeige_dashboard(self) -> None:
        self.push_screen(DashboardScreen())