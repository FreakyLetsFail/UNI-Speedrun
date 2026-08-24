from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
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

            if self.studienplan is None:
                with Vertical(classes="archive-section"):
                    yield Static(
                        "Kein Studienplan vorhanden.",
                        classes="archive-empty",
                    )
                with Horizontal(classes="screen-actions"):
                    yield Button("Zurück", id="zurueck")
                return

            abgeschlossene = [
                modul
                for modul in self.studienplan.modul_reihenfolge()
                if modul.status == Modulstatus.ABGESCHLOSSEN
            ]

            erreichte_ects = sum(m.ects for m in abgeschlossene)
            noten = [m.note for m in abgeschlossene if m.note is not None]
            schnitt_str = (
                f"Ø Note: {sum(noten) / len(noten):.2f}"
                if noten
                else "ohne Notenschnitt"
            )

            with Vertical(classes="archive-stats"):
                yield Label(
                    f"{len(abgeschlossene)} Module abgeschlossen | "
                    f"{erreichte_ects} / {self.studienplan.zielects} ECTS | "
                    f"{schnitt_str}",
                    classes="archive-stats-text",
                )

            with VerticalScroll(classes="archive-section"):
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
                        datum_str = (
                            f"abgeschlossen am {modul.abschlussdatum:%d.%m.%Y}"
                            if modul.abschlussdatum
                            else ""
                        )
                        yield Horizontal(
                            Static(modul.name, classes="module-name"),
                            Static(f"{modul.ects} ECTS", classes="module-meta"),
                            Static(note, classes="module-meta"),
                            Static(datum_str, classes="module-meta"),
                            classes="module-row",
                        )

            with Horizontal(classes="screen-actions"):
                yield Button("Zurück", id="zurueck")

    def action_zurueck(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "zurueck":
            self.app.pop_screen()

