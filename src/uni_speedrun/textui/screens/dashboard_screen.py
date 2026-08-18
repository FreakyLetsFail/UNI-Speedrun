from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, Static

from uni_speedrun.fachmodell.studienplan import Studienplan


class DashboardScreen(Screen):

    def __init__(self, studienplan: Studienplan | None = None) -> None:
        super().__init__()
        self.studienplan = studienplan

    def compose(self) -> ComposeResult:
        yield Header()

        with Center():
            with Vertical():

                yield Label(
                    "UNI Speedrun",
                    id="titel",
                )

                if self.studienplan is None:
                    yield Static(
                        "Noch kein Studienplan vorhanden.",
                        id="kein_studienplan",
                    )
                else:
                    yield Label(
                        f"Studienziel: {self.studienplan.studienziel_name}",
                        id="studienziel",
                    )

                    yield Label(
                        f"ECTS: "
                        f"{self.studienplan.erreichte_ects()}"
                        f" / "
                        f"{self.studienplan.zielects}",
                        id="ects",
                    )

                    yield Label(
                        f"Fortschritt: "
                        f"{self.studienplan.fortschritt_prozent()} %",
                        id="fortschritt",
                    )

                    aktives_modul = self.studienplan.zeige_aktives_modul()

                    if aktives_modul is None:
                        yield Static(
                            "Aktuelles Modul: kein Modul aktiv",
                            id="aktives_modul",
                        )
                    else:
                        yield Static(
                            f"Aktuelles Modul: {aktives_modul.name}",
                            id="aktives_modul",
                        )

                    naechstes_modul = self.studienplan.naechstes_modul()

                    if naechstes_modul is None:
                        yield Static(
                            "Nächstes Modul: keines",
                            id="naechstes_modul",
                        )
                    else:
                        yield Static(
                            f"Nächstes Modul: {naechstes_modul.name}",
                            id="naechstes_modul",
                        )

        yield Footer()