from .modul import Modul, Modulstatus

class Studienplan:
    def __init__(self, module: list[Modul]):
        self.module = module
    

    def berechne_ects(self):
        ects_points = 0
        for modul in self.module:
            if modul.status == Modulstatus.ABGESCHLOSSEN:
                ects_points += modul.ects
        
        return ects_points

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
                modul.aktivieren()
                print(f"Modul: {modul.name} wurde aktiviert")
            else:
                aktives = self.aktives_modul()
                raise ValueError(
                    f"Aktiven nicht möglich! Das modul {aktives.name} ist bereits aktiv."
                    )