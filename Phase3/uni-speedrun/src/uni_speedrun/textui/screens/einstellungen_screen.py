from datetime import date, datetime

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Input, Label, Static

from uni_speedrun.database.repository import StudienplanRepository
from uni_speedrun.fachmodell.modul import Modul
from uni_speedrun.fachmodell.modulstatus import Modulstatus
from uni_speedrun.fachmodell.studienplan import Studienplan
from uni_speedrun.textui.screens.modul_bearbeiten_screen import (
    ModulBearbeitenScreen,
)


class EinstellungenScreen(Screen):
    """Bearbeitet Studienplan und Modul-Liste."""

    BINDINGS = [
        ("escape", "zurueck", "Zurück"),
    ]

    STATUS_TEXT = {
        Modulstatus.GEPLANT: "Geplant",
        Modulstatus.AKTIV: "Aktiv",
        Modulstatus.WARTE_AUF_ERGEBNIS: "Warte auf Ergebnis",
        Modulstatus.ABGESCHLOSSEN: "Abgeschlossen",
    }

    def __init__(
        self,
        studienplan: Studienplan | None,
        repository: StudienplanRepository | None,
    ) -> None:
        super().__init__()
        self.studienplan = studienplan
        self.repository = repository

    def compose(self) -> ComposeResult:
        startdatum_str = (
            self.studienplan.startdatum.strftime("%d.%m.%Y")
            if self.studienplan and self.studienplan.startdatum
            else date.today().strftime("%d.%m.%Y")
        )

        with VerticalScroll(id="settings-screen"):
            yield Label("EINSTELLUNGEN", classes="screen-title")

            with Vertical(classes="settings-section"):
                yield Label("STUDIENPLAN", classes="section-heading")

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
                        else "36"
                    ),
                    id="zieldauer",
                    classes="field-input",
                )

                yield Label("Startdatum (TT.MM.JJJJ)", classes="field-label")
                yield Input(
                    value=startdatum_str,
                    placeholder="z. B. 01.11.2024",
                    id="startdatum",
                    classes="field-input",
                )

                with Horizontal(classes="screen-actions"):
                    yield Button("Plan speichern", id="plan-speichern")

            with Vertical(classes="settings-section"):
                yield Label("MODULE", classes="section-heading")

                with VerticalScroll(id="module-liste"):
                    yield from self._module_rows()

                with Horizontal(classes="screen-actions"):
                    yield Button("+ Modul", id="modul-hinzufuegen")
                    yield Button("Zurück", id="zurueck")

    def _module_rows(self) -> list[Horizontal]:
        if self.studienplan is None:
            return []

        rows = []
        alle_module = self.studienplan.modul_reihenfolge()
        anzahl = len(alle_module)

        for modul in alle_module:
            status_text = self.STATUS_TEXT.get(modul.status, modul.status.value)
            note_str = f" ({modul.note:g})" if modul.note is not None else ""

            row_items = [
                Static(f"#{modul.reihenfolge} {modul.name}", classes="module-name"),
                Static(
                    f"{modul.ects} ECTS | {modul.geplante_dauer_tage} T",
                    classes="module-meta",
                ),
                Static(
                    f"{status_text}{note_str}",
                    classes="module-status",
                ),
            ]

            if modul.status == Modulstatus.WARTE_AUF_ERGEBNIS:
                row_items.append(
                    Button(
                        "Abschließen",
                        id=f"complete-{modul.reihenfolge}",
                        classes="module-action-done",
                    )
                )

            row_items.extend([
                Button(
                    "▲",
                    id=f"up-{modul.reihenfolge}",
                    classes="module-action-arrow",
                    disabled=(modul.reihenfolge == 1),
                ),
                Button(
                    "▼",
                    id=f"down-{modul.reihenfolge}",
                    classes="module-action-arrow",
                    disabled=(modul.reihenfolge == anzahl),
                ),
                Button(
                    "Edit",
                    id=f"edit-{modul.reihenfolge}",
                    classes="module-action",
                ),
                Button(
                    "X",
                    id=f"delete-{modul.reihenfolge}",
                    classes="module-action-delete",
                ),
            ])

            rows.append(
                Horizontal(
                    *row_items,
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

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id in ("studienziel", "zielects", "zieldauer", "startdatum"):
            self._plan_speichern()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id or ""

        if button_id == "zurueck":
            self._plan_speichern(silent=True)
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

        if button_id.startswith("complete-"):
            self._modul_schnell_abschliessen(button_id)
            return

        if button_id.startswith("up-"):
            self._modul_verschieben(button_id, nach_oben=True)
            return

        if button_id.startswith("down-"):
            self._modul_verschieben(button_id, nach_oben=False)
            return

        if button_id.startswith("edit-"):
            self._modul_bearbeiten(button_id)
            return

        if button_id.startswith("delete-"):
            self._modul_loeschen(button_id)

    def _parse_datum(self, text: str) -> date:
        text = text.strip()
        for fmt in ("%d.%m.%Y", "%d.%m.%y", "%Y-%m-%d"):
            try:
                return datetime.strptime(text, fmt).date()
            except ValueError:
                pass
        raise ValueError("Datum bitte im Format TT.MM.JJJJ angeben (z. B. 01.11.2024).")

    def _plan_speichern(self, silent: bool = False) -> bool:
        if self.studienplan is None:
            return False

        try:
            studienziel = self.query_one("#studienziel", Input).value.strip()
            zielects_text = self.query_one("#zielects", Input).value.strip()
            zieldauer_text = self.query_one("#zieldauer", Input).value.strip()
            startdatum_text = self.query_one("#startdatum", Input).value.strip()
        except Exception:
            return False

        try:
            zielects = int(zielects_text)
            zieldauer = int(zieldauer_text)
        except ValueError:
            if not silent:
                self.notify("ECTS und Zieldauer müssen Zahlen sein.", severity="error")
            return False

        try:
            startdatum = self._parse_datum(startdatum_text)
        except ValueError as err:
            if not silent:
                self.notify(str(err), severity="error")
            return False

        if not studienziel or zielects <= 0 or zieldauer <= 0:
            if not silent:
                self.notify("Bitte gültige Planwerte eingeben.", severity="error")
            return False

        self.studienplan.studienziel_name = studienziel
        self.studienplan.zielects = zielects
        self.studienplan.zieldauer = zieldauer
        self.studienplan.startdatum = startdatum
        self._speichern()

        if not silent:
            self.notify("Studienplan gespeichert.")
        return True

    def _modul_schnell_abschliessen(self, button_id: str) -> None:
        if self.studienplan is None:
            return

        reihenfolge = int(button_id.split("-")[1])
        modul = next(
            (
                m
                for m in self.studienplan.module
                if m.reihenfolge == reihenfolge
            ),
            None,
        )

        if modul is None:
            return

        modul.status = Modulstatus.ABGESCHLOSSEN
        if modul.abschlussdatum is None:
            modul.abschlussdatum = date.today()

        self._speichern()
        self.refresh(recompose=True)
        self.notify(f"{modul.name} auf 'Abgeschlossen' gesetzt.")

    def _modul_verschieben(self, button_id: str, nach_oben: bool) -> None:
        if self.studienplan is None:
            return

        reihenfolge = int(button_id.split("-")[1])
        module = self.studienplan.modul_reihenfolge()
        ziel_reihenfolge = reihenfolge - 1 if nach_oben else reihenfolge + 1

        modul_a = next((m for m in module if m.reihenfolge == reihenfolge), None)
        modul_b = next((m for m in module if m.reihenfolge == ziel_reihenfolge), None)

        if modul_a and modul_b:
            modul_a.reihenfolge, modul_b.reihenfolge = (
                modul_b.reihenfolge,
                modul_a.reihenfolge,
            )
            self._speichern()
            self.refresh(recompose=True)

    def _modul_bearbeiten(self, button_id: str) -> None:
        if self.studienplan is None:
            return

        reihenfolge = int(button_id.split("-")[1])
        modul = next(
            (
                m
                for m in self.studienplan.module
                if m.reihenfolge == reihenfolge
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

        andere = [m for m in self.studienplan.module if m != modul]
        andere.sort(key=lambda m: m.reihenfolge)

        ziel_index = max(0, min(modul.reihenfolge - 1, len(andere)))
        andere.insert(ziel_index, modul)

        for index, m in enumerate(andere, start=1):
            m.reihenfolge = index

        self.studienplan.module = andere
        self._speichern()
        self.refresh(recompose=True)

    def _modul_loeschen(self, button_id: str) -> None:
        if self.studienplan is None:
            return

        reihenfolge = int(button_id.split("-")[1])

        modul = next(
            (
                m
                for m in self.studienplan.module
                if m.reihenfolge == reihenfolge
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
        self._plan_speichern(silent=True)
        self.app.pop_screen()


