from datetime import date

from dateutil.relativedelta import relativedelta
from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Label, ProgressBar, Static
from textual.css.query import NoMatches

from uni_speedrun.controller.dashboard_controller import DashboardController
from uni_speedrun.database.repository import StudienplanRepository
from uni_speedrun.fachmodell.modulstatus import Modulstatus
from uni_speedrun.fachmodell.studienplan import Studienplan


class DashboardScreen(Screen):
    """Hauptdashboard des aktuellen Studienplans (Reine Präsentationsschicht)."""

    BINDINGS = [
        ("s", "einstellungen", "Einstellungen"),
        ("a", "archiv", "Archiv"),
        ("m", "modul_abschliessen", "Modul abschließen"),
        ("q", "beenden", "Beenden"),
    ]

    def __init__(
        self,
        studienplan: Studienplan | None = None,
        repository: StudienplanRepository | None = None,
        controller: DashboardController | None = None,
    ) -> None:
        super().__init__()
        self.studienplan = studienplan
        self.repository = repository
        self.controller = controller
        if self.controller is None and self.repository is not None:
            self.controller = DashboardController(self.repository)

    def compose(self) -> ComposeResult:
        if self.studienplan is None:
            yield Static(
                "Noch kein Studienplan vorhanden.",
                id="kein-studienplan",
            )
            return

        plan = self.studienplan
        heute = date.today()
        aktives_modul = plan.zeige_aktives_modul()
        wartende_module = [
            m for m in plan.module if m.status == Modulstatus.WARTE_AUF_ERGEBNIS
        ]
        naechstes_modul = self._naechstes_modul_sicher()
        fortschritt = min(max(plan.fortschritt_prozent(), 0), 100)
        prognose = plan.prognostiziertes_studienende()

        with Horizontal(id="dashboard-header"):
            yield Static("", classes="header-line")
            yield Static("UNI Speedrun", id="dashboard-titel", markup=False)
            yield Static("", classes="header-line")

        with Horizontal(id="top-info"):
            with Vertical(classes="info-block"):
                yield Label(
                    f"Ziel: {plan.zieldatum():%d.%m.%Y}",
                    classes="info-value",
                    markup=False,
                )

            with Vertical(classes="info-block"):
                yield Label(
                    (
                        "Prognose: –"
                        if prognose is None
                        else f"Prognose: {prognose:%d.%m.%Y}"
                    ),
                    classes="info-value",
                    markup=False,
                )

            with Vertical(classes="info-block"):
                yield Label(
                    f"Abweichung: {self._format_abweichung(prognose, plan.zieldatum())}",
                    classes="info-value",
                    markup=False,
                )

        with Vertical(id="current-module"):
            if aktives_modul is not None:
                with Center():
                    yield Static(
                        f"AKTUELL: {aktives_modul.name.upper()}",
                        classes="current-title",
                        markup=False,
                    )
                yield Static(
                    f"{aktives_modul.ects} ECTS | "
                    f"{self._wochen(aktives_modul.geplante_dauer_tage)} geplant",
                    classes="current-subtitle",
                    markup=False,
                )
                yield Static(
                    f"{max(aktives_modul.berechne_restzeit(heute), 0)} Tage übrig",
                    classes="days-left",
                    markup=False,
                )
            elif wartende_module:
                letztes_wartend = wartende_module[-1]
                with Center():
                    yield Static(
                        f"WARTE AUF ERGEBNIS: {letztes_wartend.name.upper()}",
                        classes="current-title",
                        markup=False,
                    )
                yield Static(
                    "Starte nächstes Modul mit [M] | In [S] abschließen",
                    classes="current-subtitle",
                    markup=False,
                )
                yield Static(
                    (
                        f"Eingereicht am {letztes_wartend.pruefungsdatum:%d.%m.%Y}"
                        if letztes_wartend.pruefungsdatum
                        else "In Korrektur"
                    ),
                    classes="days-left",
                    markup=False,
                )
            else:
                with Center():
                    yield Static(
                        "AKTUELL: KEIN MODUL AKTIV",
                        classes="current-title",
                        markup=False,
                    )
                yield Static(
                    "Starte das nächste Modul mit [M].",
                    classes="current-subtitle",
                    markup=False,
                )
                yield Static("", classes="days-left", markup=False)

        with Vertical(id="progress-area"):
            with Center():
                with Vertical(id="progress-card"):
                    yield Label(
                        f"{plan.erreichte_ects()} / {plan.zielects} ECTS",
                        id="ects-value",
                        markup=False,
                    )

                    yield Label(
                        f"{fortschritt:g}%",
                        id="progress-percent",
                        markup=False,
                    )

                    with Horizontal(id="progress-row"):
                        yield Label("0%", classes="progress-end", markup=False)
                        yield ProgressBar(
                            total=100,
                            show_eta=False,
                            show_percentage=False,
                            id="progress-bar",
                        )
                        yield Label("100%", classes="progress-end", markup=False)

        with Vertical(id="next-module"):
            with Center():
                yield Static("", classes="next-divider-top")
            if naechstes_modul is None:
                yield Static("Nächstes Modul: –", id="next-title", markup=False)
                yield Static("", id="next-details", markup=False)
            else:
                yield Static(
                    f"Nächstes Modul: {naechstes_modul.name}",
                    id="next-title",
                    markup=False,
                )
                yield Static(
                    f"{naechstes_modul.ects} ECTS | "
                    f"{self._wochen(naechstes_modul.geplante_dauer_tage)}",
                    id="next-details",
                    markup=False,
                )
            with Center():
                yield Static("", classes="next-divider-bottom")

        with Horizontal(id="dashboard-actions"):
            yield Label("[S] Einstellungen", classes="action", markup=False)
            yield Label("[A] Archiv", classes="action", markup=False)
            yield Label("[M] Modul abschließen", classes="action", markup=False)
            yield Label("[Q] Beenden", classes="action", markup=False)

    def on_mount(self) -> None:
        self._update_progress()

    def _update_progress(self) -> None:
        if self.studienplan is None:
            return

        try:
            bar = self.query_one("#progress-bar", ProgressBar)
            bar.update(
                progress=min(
                    max(self.studienplan.fortschritt_prozent(), 0),
                    100,
                )
            )
        except NoMatches:
            return

    def _naechstes_modul_sicher(self):
        if self.studienplan is None:
            return None
        return self.studienplan.naechstes_geplantes_modul()

    def action_einstellungen(self) -> None:
        from uni_speedrun.textui.screens.einstellungen_screen import (
            EinstellungenScreen,
        )

        self.app.push_screen(
            EinstellungenScreen(self.studienplan, self.repository, self.controller),
            callback=self._on_subscreen_closed,
        )

    def action_archiv(self) -> None:
        from uni_speedrun.textui.screens.archiv_screen import ArchivScreen

        self.app.push_screen(
            ArchivScreen(self.studienplan),
            callback=self._on_subscreen_closed,
        )

    def _on_subscreen_closed(self, result=None) -> None:
        if self.controller is not None and self.controller.studienplan is not None:
            self.studienplan = self.controller.studienplan
        self.refresh(recompose=True)

    def action_modul_abschliessen(self) -> None:
        if self.controller is not None:
            erfolg, nachricht = self.controller.modul_abschliessen_oder_starten()
            self.studienplan = self.controller.studienplan
            self.notify(nachricht, severity="information" if erfolg else "warning")
        elif self.studienplan is not None:
            aktives = self.studienplan.zeige_aktives_modul()
            if aktives is None:
                naechstes = self._naechstes_modul_sicher()
                if naechstes:
                    self.studienplan.aktiviere_modul(naechstes)
                    self._speichern()
                    self.notify(f"{naechstes.name} wurde gestartet.")
            else:
                self.studienplan.modul_in_bewertung_versetzen(aktives)
                self._speichern()
                self.notify(f"{aktives.name} wartet jetzt auf das Ergebnis.")

        self.refresh(recompose=True)

    def action_beenden(self) -> None:
        self.app.exit()

    def _speichern(self) -> None:
        if self.controller is not None:
            self.controller.speichere_studienplan()
        elif self.repository is not None and self.studienplan is not None:
            self.repository.speichern(self.studienplan)


    @staticmethod
    def _wochen(tage: int) -> str:
        wochen = tage / 7
        if wochen == 1:
            return "1 Woche"
        if wochen.is_integer():
            return f"{int(wochen)} Wochen"
        return f"{wochen:.1f} Wochen"

    @staticmethod
    def _format_abweichung(prognose: date | None, ziel: date | None) -> str:
        if prognose is None or ziel is None:
            return "–"

        if prognose == ziel:
            return "0 Tage (im Zeitplan)"

        if prognose > ziel:
            rd = relativedelta(prognose, ziel)
            monate = rd.years * 12 + rd.months
            tage = rd.days
            if monate > 0 and tage > 0:
                return f"+{monate} {'Monat' if monate == 1 else 'Monate'} {tage} Tage"
            elif monate > 0:
                return f"+{monate} {'Monat' if monate == 1 else 'Monate'}"
            else:
                return f"+{tage} Tage"
        else:
            rd = relativedelta(ziel, prognose)
            monate = rd.years * 12 + rd.months
            tage = rd.days
            if monate > 0 and tage > 0:
                return f"-{monate} {'Monat' if monate == 1 else 'Monate'} {tage} Tage"
            elif monate > 0:
                return f"-{monate} {'Monat' if monate == 1 else 'Monate'}"
            else:
                return f"-{tage} Tage"

