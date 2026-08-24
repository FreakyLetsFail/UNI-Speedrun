from pathlib import Path

from textual.app import App

from uni_speedrun.controller.dashboard_controller import DashboardController
from uni_speedrun.database.sqlite_repository import SQLiteStudienplanRepository
from uni_speedrun.textui.screens.dashboard_screen import DashboardScreen
from uni_speedrun.textui.screens.studienplan_erstellen_screen import (
    StudienplanErstellenScreen,
)


class UniSpeedrunApp(App):
    """Hauptanwendung von Uni Speedrun (Composition Root für Dependency Injection)."""

    CSS_PATH = "styles/app.tcss"

    def __init__(self):
        super().__init__()

        projektordner = Path(__file__).resolve().parents[3]
        datenbank_pfad = projektordner / "data" / "uni_speedrun.db"

        self.repository = SQLiteStudienplanRepository(str(datenbank_pfad))
        self.controller = DashboardController(self.repository)

    def on_mount(self) -> None:
        studienplan = self.controller.lade_studienplan()

        if studienplan is None:
            self.push_screen(StudienplanErstellenScreen(self.repository))
        else:
            self.push_screen(
                DashboardScreen(studienplan, self.repository, self.controller)
            )

