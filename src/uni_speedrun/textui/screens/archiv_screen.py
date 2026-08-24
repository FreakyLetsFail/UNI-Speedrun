from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Label, Static

from uni_speedrun.fachmodell.modulstatus import Modulstatus
from uni_speedrun.fachmodell.studienplan import Studienplan


class ArchivScreen(Screen):
    """Zeigt alle bereits abgeschlossenen Module."""

    BINDINGS = [
        ("escape", "zurueck", "Zurück"),
    ]

    def __init__(self, studienplan: Studienplan | None) -> None:
        super().__init__()
        self.studienplan = studienplan

    def compose(self) -> ComposeResult:
        with Vertical(id="archive-screen"):
            yield Label("ARCHIV", classes="screen-title")

            with VerticalScroll(classes="archive-section"):
                if self.studienplan is None:
                    yield Static(
                        "Kein Studienplan vorhanden.",
                        classes="archive-empty",
                    )
                    return

                abgeschlossene = [
                    modul
                    for modul in self.studienplan.modul_reihenfolge()
                    if modul.status == Modulstatus.ABGESCHLOSSEN
                ]

                if not abgeschlossene:
                    yield Static(
                        "Noch keine Module abgeschlossen.",
                        classes="archive-empty",
                    )
                else:
                    for modul in abgeschlossene:
                        note = (
                            f"Note {modul.note:g}"
                            if modul.note is not None
                            else "ohne Note"
                        )
                        yield Static(
                            f"{modul.name}    |    "
                            f"{modul.ects} ECTS    |    {note}",
                            classes="module-row",
                        )

            with Vertical(classes="screen-actions"):
                yield Button("Zurück", id="zurueck")

    def action_zurueck(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "zurueck":
            self.app.pop_screen()
