from pathlib import Path

from textual.app import App

from uni_speedrun.database.sqlite_repository import SQLiteStudienplanRepository
from uni_speedrun.textui.screens.dashboard_screen import DashboardScreen


class UniSpeedrunApp(App):

    def __init__(self):
        super().__init__()

        projektordner = Path(__file__).resolve().parents[3]
        datenbank_pfad = projektordner / "data" / "uni_speedrun.db"

        self.repository = SQLiteStudienplanRepository(
            str(datenbank_pfad)
        )

    def on_mount(self) -> None:
        studienplan = self.repository.laden()

        self.push_screen(
            DashboardScreen(studienplan)
        )