from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Input, Label, Static

from uni_speedrun.database.repository import StudienplanRepository
from uni_speedrun.fachmodell.modul import Modul
from uni_speedrun.fachmodell.studienplan import Studienplan
from uni_speedrun.textui.screens.modul_bearbeiten_screen import (
    ModulBearbeitenScreen,
)


class EinstellungenScreen(Screen):
    """Bearbeitet Studienplan und Modul-Liste."""

    BINDINGS = [
        ("escape", "zurueck", "Zurück"),
    ]

    def __init__(
        self,
        studienplan: Studienplan | None,
        repository: StudienplanRepository | None,
    ) -> None:
        super().__init__()
        self.studienplan = studienplan
        self.repository = repository

    def compose(self) -> ComposeResult:
        with Vertical(id="settings-screen"):
            yield Label("EINSTELLUNGEN", classes="screen-title")

            with Vertical(classes="settings-section"):
                yield Label("STUDIENPLAN", classes="field-label")

                yield Label("Studienziel", classes="field-label")
                yield Input(
                    value=(
                        self.studienplan.studienziel_name
                        if self.studienplan
                        else ""
                    ),
                    id="studienziel",
                    classes="field-input",
                )

                yield Label("Ziel-ECTS", classes="field-label")
                yield Input(
                    value=(
                        str(self.studienplan.zielects)
                        if self.studienplan
                        else "180"
                    ),
                    id="zielects",
                    classes="field-input",
                )

                yield Label("Zieldauer in Monaten", classes="field-label")
                yield Input(
                    value=(
                        str(self.studienplan.zieldauer)
                        if self.studienplan
                        else "15"
                    ),
                    id="zieldauer",
                    classes="field-input",
                )

                yield Button("Plan speichern", id="plan-speichern")

            with Vertical(classes="settings-section"):
                yield Label("MODULE", classes="field-label")

                with VerticalScroll(id="module-liste"):
                    yield from self._module_rows()

                with Horizontal(classes="screen-actions"):
                    yield Button("+ Modul", id="modul-hinzufuegen")
                    yield Button("Zurück", id="zurueck")

    def _module_rows(self) -> list[Horizontal]:
        if self.studienplan is None:
            return []

        rows = []

        for modul in self.studienplan.modul_reihenfolge():
            rows.append(
                Horizontal(
                    Static(modul.name, classes="module-name"),
                    Static(
                        f"{modul.ects} ECTS | "
                        f"{modul.geplante_dauer_tage} Tage",
                        classes="module-meta",
                    ),
                    Static(
                        modul.status.value,
                        classes="module-status",
                    ),
                    Button(
                        "Edit",
                        id=f"edit-{modul.reihenfolge}",
                        classes="module-action",
                    ),
                    Button(
                        "X",
                        id=f"delete-{modul.reihenfolge}",
                        classes="module-action",
                    ),
                    classes="module-row",
                )
            )

        if not rows:
            rows.append(
                Horizontal(
                    Static(
                        "Noch keine Module angelegt.",
                        classes="module-name",
                    ),
                    classes="module-row",
                )
            )

        return rows

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id or ""

        if button_id == "zurueck":
            self.app.pop_screen()
            return

        if button_id == "plan-speichern":
            self._plan_speichern()
            return

        if button_id == "modul-hinzufuegen":
            if self.studienplan is None:
                return

            reihenfolge = len(self.studienplan.module) + 1
            self.app.push_screen(
                ModulBearbeitenScreen(None, reihenfolge),
                callback=self._modul_editor_beendet,
            )
            return

        if button_id.startswith("edit-"):
            self._modul_bearbeiten(button_id)
            return

        if button_id.startswith("delete-"):
            self._modul_loeschen(button_id)

    def _plan_speichern(self) -> None:
        if self.studienplan is None:
            return

        studienziel = self.query_one("#studienziel", Input).value.strip()

        try:
            zielects = int(
                self.query_one("#zielects", Input).value.strip()
            )
            zieldauer = int(
                self.query_one("#zieldauer", Input).value.strip()
            )
        except ValueError:
            self.notify(
                "ECTS und Zieldauer müssen Zahlen sein.",
                severity="error",
            )
            return

        if not studienziel or zielects <= 0 or zieldauer <= 0:
            self.notify(
                "Bitte gültige Planwerte eingeben.",
                severity="error",
            )
            return

        self.studienplan.studienziel_name = studienziel
        self.studienplan.zielects = zielects
        self.studienplan.zieldauer = zieldauer
        self._speichern()
        self.notify("Studienplan gespeichert.")

    def _modul_bearbeiten(self, button_id: str) -> None:
        if self.studienplan is None:
            return

        reihenfolge = int(button_id.split("-")[1])
        modul = next(
            (
                modul
                for modul in self.studienplan.module
                if modul.reihenfolge == reihenfolge
            ),
            None,
        )

        if modul is None:
            return

        self.app.push_screen(
            ModulBearbeitenScreen(modul, reihenfolge),
            callback=self._modul_editor_beendet,
        )

    def _modul_editor_beendet(self, modul: Modul | None) -> None:
        if modul is None or self.studienplan is None:
            return

        if modul not in self.studienplan.module:
            self.studienplan.module.append(modul)

        self._normalisiere_reihenfolge()
        self._speichern()
        self.refresh(recompose=True)

    def _modul_loeschen(self, button_id: str) -> None:
        if self.studienplan is None:
            return

        reihenfolge = int(button_id.split("-")[1])

        modul = next(
            (
                modul
                for modul in self.studienplan.module
                if modul.reihenfolge == reihenfolge
            ),
            None,
        )

        if modul is None:
            return

        self.studienplan.module.remove(modul)
        self._normalisiere_reihenfolge()
        self._speichern()
        self.refresh(recompose=True)
        self.notify(f"{modul.name} wurde entfernt.")

    def _normalisiere_reihenfolge(self) -> None:
        if self.studienplan is None:
            return

        for nummer, modul in enumerate(
            self.studienplan.modul_reihenfolge(),
            start=1,
        ):
            modul.reihenfolge = nummer

    def _speichern(self) -> None:
        if self.repository is not None and self.studienplan is not None:
            self.repository.speichern(self.studienplan)

    def action_zurueck(self) -> None:
        self.app.pop_screen()
