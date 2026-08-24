from datetime import date

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Label, ProgressBar, Static

from uni_speedrun.fachmodell.modul import Modul
from uni_speedrun.fachmodell.studienplan import Studienplan


class DashboardScreen(Screen):
    """Dashboard des aktuellen Studienplans."""

    BINDINGS = [
        ("s", "einstellungen", "Einstellungen"),
        ("a", "archiv", "Archiv"),
        ("m", "modul_abschliessen", "Modul abschließen"),
        ("q", "beenden", "Beenden"),
    ]

    def __init__(self, studienplan: Studienplan | None = None) -> None:
        super().__init__()
        self.studienplan = studienplan

    def compose(self) -> ComposeResult:
        if self.studienplan is None:
            yield Static(
                "Noch kein Studienplan vorhanden.",
                id="kein-studienplan",
            )
            yield Footer()
            return

        plan = self.studienplan
        heute = date.today()

        aktives_modul = plan.zeige_aktives_modul()
        naechstes_modul = plan.naechstes_modul()

        fortschritt = min(max(plan.fortschritt_prozent(), 0), 100)
        prognose = plan.prognostiziertes_studienende()
        abweichung = plan.abweichung_zum_zieldatum()

        yield Static("UNI Speedrun", id="dashboard-titel")

        with Horizontal(id="top-info"):
            with Vertical(classes="info-block"):
                yield Label("①", classes="marker")
                yield Label(
                    f"Ziel: {plan.zieldatum():%d.%m.%Y}",
                    classes="info-value",
                )

            with Vertical(classes="info-block"):
                yield Label("②", classes="marker")
                if prognose is None:
                    yield Label(
                        "Prognose: –",
                        classes="info-value",
                    )
                else:
                    yield Label(
                        f"Prognose: {prognose:%d.%m.%Y}",
                        classes="info-value",
                    )

            with Vertical(classes="info-block"):
                yield Label("③", classes="marker")
                yield Label(
                    f"Abweichung: {self._format_abweichung(abweichung)}",
                    classes="info-value",
                )

        with Vertical(id="current-module"):
            yield Label("④", classes="marker")

            if aktives_modul is None:
                yield Static(
                    "AKTUELL: KEIN MODUL AKTIV",
                    classes="current-title",
                )
                yield Static(
                    "Starte das nächste Modul mit [M].",
                    classes="current-subtitle",
                )
            else:
                yield Static(
                    f"AKTUELL: {aktives_modul.name.upper()}",
                    classes="current-title",
                )
                yield Static(
                    f"{aktives_modul.ects} ECTS | "
                    f"{self._wochen(aktives_modul.geplante_dauer_tage)} geplant",
                    classes="current-subtitle",
                )
                yield Static(
                    f"{max(aktives_modul.berechne_restzeit(heute), 0)} Tage übrig",
                    classes="days-left",
                )

        with Vertical(id="progress-card"):
            yield Label(
                f"{plan.erreichte_ects()} / {plan.zielects} ECTS",
                id="ects-value",
            )

            with Horizontal(id="progress-row"):
                yield Label("0%", classes="progress-end")
                yield ProgressBar(
                    total=100,
                    show_eta=False,
                    show_percentage=False,
                    id="progress-bar",
                )
                yield Label("100%", classes="progress-end")

            yield Label(
                f"{fortschritt:g}%",
                id="progress-percent",
            )

        with Horizontal(id="next-module"):
            yield Label("⑥", classes="marker")
            if naechstes_modul is None:
                yield Static("Nächstes Modul: –", id="next-title")
            else:
                yield Static(
                    f"Nächstes Modul: {naechstes_modul.name}",
                    id="next-title",
                )
                yield Static(
                    f"{naechstes_modul.ects} ECTS | "
                    f"{self._wochen(naechstes_modul.geplante_dauer_tage)}",
                    id="next-details",
                )

        with Horizontal(id="dashboard-actions"):
            yield Label("[S] Einstellungen", classes="action")
            yield Label("[A] Archiv", classes="action")
            yield Label("[M] Modul abschließen", classes="action")
            yield Label("[Q] Beenden", classes="action")

        yield Footer()

    def on_mount(self) -> None:
        if self.studienplan is not None:
            self.query_one("#progress-bar", ProgressBar).update(
                progress=min(max(self.studienplan.fortschritt_prozent(), 0), 100)
            )

    def action_einstellungen(self) -> None:
        self.notify("Einstellungen kommen in einer späteren Phase.")

    def action_archiv(self) -> None:
        self.notify("Das Archiv kommt in einer späteren Phase.")

    def action_modul_abschliessen(self) -> None:
        self.notify("Modul-Abschluss kommt in einer späteren Phase.")

    def action_beenden(self) -> None:
        self.app.exit()

    @staticmethod
    def _wochen(tage: int) -> str:
        wochen = tage / 7
        if wochen.is_integer():
            return f"{int(wochen)} Wochen"
        return f"{wochen:.1f} Wochen"

    @staticmethod
    def _format_abweichung(abweichung) -> str:
        if abweichung is None:
            return "–"

        tage = abweichung.days
        if tage == 0:
            return "0 Tage"

        sign = "+" if tage > 0 else "-"
        tage = abs(tage)

        monate = tage // 30
        resttage = tage % 30

        if monate:
            text = f"{monate} Monat" if monate == 1 else f"{monate} Monate"
            if resttage:
                text += f" {resttage} Tage"
        else:
            text = f"{resttage} Tage"

        return f"{sign}{text}"
