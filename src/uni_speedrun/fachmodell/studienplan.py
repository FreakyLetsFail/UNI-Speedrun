from .modul import Modul, Modulstatus
from datetime import date
from dateutil.relativedelta import relativedelta


class Studienplan:
    def __init__(self, module: list[Modul], studienziel_name, zielects, zieldauer):
        self.module = module
        self.studienziel_name = studienziel_name
        self.zielects = zielects
        self.zieldauer = zieldauer
        self.startdatum = date.today()
    

    def zieldatum(self):
        return self.startdatum + relativedelta(months=self.zieldauer)

    def erreichte_ects(self):
        ects_points = 0
        for modul in self.module:
            if modul.status == Modulstatus.ABGESCHLOSSEN:
                ects_points += modul.ects
        
        return ects_points
    
    def fortschritt_prozent(self):
        return round((self.erreichte_ects() / self.zielects)*100,2)

    def modul_reihenfolge(self):
        return sorted(self.module, key=lambda x: x.reihenfolge)

    def aktives_modul(self):
        for modul in self.module:
            if modul.status == Modulstatus.AKTIV:
                return modul
        else:
            return None

    def aktiviere_modul(self, modul):
            if self.aktives_modul() is None:
                modul._aktivieren()
                print(f"Modul: {modul.name} wurde aktiviert")
            else:
                aktives = self.aktives_modul()
                raise ValueError(
                    f"Aktiven nicht möglich! Das modul {aktives.name} ist bereits aktiv."
                    )

    def schliesse_modul_ab(self, modul):
        if modul.status == Modulstatus.ABGESCHLOSSEN:
            raise ValueError(
                f"Das Modul {modul.name} ist bereits abgeschlossen."
            )

        if modul.status != Modulstatus.AKTIV:
            raise ValueError(
                f"Das Modul {modul.name} ist nicht aktiv und kann nicht abgeschlossen werden."
            )

        modul._schliesse_ab()
        print(f"Modul: {modul.name} wurde erfolgreich abgeschlossen.")

    def modul_in_bewertung_versetzen(self, modul):
        if modul.status == Modulstatus.WARTE_AUF_ERGEBNIS:
            raise ValueError(
                f"Das Modul {modul.name} ist bereits auf WARTE_AUF_ERGEBNIS."
            )

        if modul.status != Modulstatus.AKTIV:
            raise ValueError(
                f"Das Modul {modul.name} ist nicht aktiv und kann nicht auf WARTE_AUF_ERGEBNIS gesetzt werden."
            )

        modul._warte_auf_ergebnis()
        print(f"Modul: {modul.name} wurde erfolgreich auf WARTE_AUF_ERGEBNIS gesetzt.")     