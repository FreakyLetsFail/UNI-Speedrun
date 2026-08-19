from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, Select
from uni_speedrun.fachmodell.modul import Modul
from uni_speedrun.fachmodell.modulstatus import Modulstatus

class ModulErstellenScreen(Screen):
    """
    Screen zum Erstellen mehrerer Module.

    Module werden zunächst in der Oberfläche gesammelt.
    Erst bei "Fertig" werden sie als Fachmodell-Objekte erzeugt.
    """

    BINDINGS = [
        ("f2", "neues_modul", "Neues Modul"),
        ("f10", "fertig", "Fertig"),
        ("escape", "zurueck", "Zurück"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Enthält die Nummern der aktuell angelegten Module.
        self.modul_nummer = 0

    def compose(self) -> ComposeResult:
        yield Header()

        yield Label(
            "Modul erstellen",
            id="titel",
        )

        # Tabellenkopf
        yield Horizontal(
            Label("Nr.", classes="kopf nr"),
            Label("Modulname", classes="kopf modulname"),
            Label("ECTS", classes="kopf ects"),
            Label("Status", classes="kopf status"),
            Label("Dauer", classes="kopf dauer"),
            classes="modul-kopf",
        )

        yield VerticalScroll(
            id="modul-liste",
        )

        yield Horizontal(
            Button(
                "+ Modul",
                id="neues-modul",
            ),
            Button(
                "Fertig",
                id="fertig",
                variant="success",
            ),
            Button(
                "Zurück",
                id="zurueck",
            ),
            id="aktionen",
        )

        yield Footer()

    def on_mount(self) -> None:
        """
        Beim Öffnen direkt das erste Modul anlegen.
        """
        self.neues_modul()

    def action_neues_modul(self) -> None:
        self.neues_modul()

    def action_fertig(self) -> None:
        self.module_fertig()

    def action_zurueck(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "neues-modul":
            self.neues_modul()

        elif event.button.id == "fertig":
            self.module_fertig()

        elif event.button.id == "zurueck":
            self.app.pop_screen()

    def neues_modul(self) -> None:
        """
        Fügt eine neue Modulzeile hinzu.

        Wichtig:
        Die Widgets werden direkt beim Erzeugen der Horizontal-Zeile
        übergeben. Dadurch entsteht kein MountError.
        """

        self.modul_nummer += 1
        nummer = self.modul_nummer

        liste = self.query_one("#modul-liste", VerticalScroll)

        zeile = Horizontal(
            Label(
                f"{nummer}.",
                classes="nr",
            ),

            Input(
                placeholder="Modulname",
                id=f"modulname-{nummer}",
                classes="modulname",
            ),

            Input(
                value="5",
                placeholder="ECTS",
                id=f"ects-{nummer}",
                classes="ects",
            ),

            Select(
                [
                    ("geplant", "geplant"),
                    ("begonnen", "begonnen"),
                    ("warte auf Ergebnis", "warte_auf_ergebnis"),
                    ("abgeschlossen", "abgeschlossen"),
                ],
                value="geplant",
                id=f"status-{nummer}",
                classes="status",
            ),

            Input(
                value="14",
                placeholder="Tage",
                id=f"dauer-{nummer}",
                classes="dauer",
            ),

            id=f"modul-zeile-{nummer}",
            classes="modul-zeile",
        )

        # Die komplette Zeile wird eingehängt.
        # NICHT mehr zeile.mount(...) verwenden.
        liste.mount(zeile)

        # Fokus direkt auf das neue Modulname-Feld setzen.
        self.set_focus(
            self.query_one(
                f"#modulname-{nummer}",
                Input,
            )
        )

    def module_fertig(self) -> None:
        """
        Liest alle Modulzeilen aus und erzeugt daraus Fachmodell-Objekte.
        """

        module = []

        for nummer in range(1, self.modul_nummer + 1):
            modulname = self.query_one(
                f"#modulname-{nummer}",
                Input,
            ).value.strip()

            ects_text = self.query_one(
                f"#ects-{nummer}",
                Input,
            ).value.strip()

            status = self.query_one(
                f"#status-{nummer}",
                Select,
            ).value

            dauer_text = self.query_one(
                f"#dauer-{nummer}",
                Input,
            ).value.strip()

            # Leere Zeilen nicht speichern.
            if not modulname:
                self.notify(
                    f"Bitte Modul {nummer} benennen.",
                    severity="error",
                )
                self.set_focus(
                    self.query_one(
                        f"#modulname-{nummer}",
                        Input,
                    )
                )
                return

            try:
                ects = int(ects_text)
                dauer = int(dauer_text)

            except ValueError:
                self.notify(
                    f"ECTS und Dauer von Modul {nummer} müssen Zahlen sein.",
                    severity="error",
                )
                return

            if ects <= 0:
                self.notify(
                    f"ECTS von Modul {nummer} müssen größer als 0 sein.",
                    severity="error",
                )
                return

            if dauer <= 0:
                self.notify(
                    f"Die Dauer von Modul {nummer} muss größer als 0 sein.",
                    severity="error",
                )
                return

            try:
                status_enum = Modulstatus(status)

                modul = Modul(
                    modulname,
                    ects,
                    dauer,
                    nummer,
                    status_enum,
                )

            except ValueError as error:
                self.notify(
                    f"Modul {nummer}: {error}",
                    severity="error",
                )
                return

            module.append(modul)

        # Die fertigen Module an den aufrufenden Screen zurückgeben.
        self.dismiss(module)