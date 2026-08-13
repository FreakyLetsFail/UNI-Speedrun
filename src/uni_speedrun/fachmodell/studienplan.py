from .modul import Modul, Modulstatus
from datetime import date
from dateutil.relativedelta import relativedelta


class Studienplan:
    def __init__(self, module: list[Modul], studienziel_name, zielects, zieldauer):

        reihenfolge = [modul.reihenfolge for modul in module]

        if len(reihenfolge) != len(set(reihenfolge)):
            raise ValueError(
                "Jedes Modul muss eine eindeutige Reihenfolge haben."
            )

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

    def zeige_aktives_modul(self):
        for modul in self.module:
            if modul.status == Modulstatus.AKTIV:
                return modul
        else:
            return None

# Modul aktivieren
    def aktiviere_modul(self, modul):
            if self.zeige_aktives_modul() is None:
                if modul == self.naechstes_modul():
                    modul._aktivieren()
                    print(f"Modul: {modul.name} wurde aktiviert")
                else:
                    raise ValueError(f"Aktivieren nicht möglich! Das Modul {self.naechstes_modul()} ist nicht in der Reihenfolge als nächstes dran!")
            else:
                aktives = self.zeige_aktives_modul()
                raise ValueError(
                    f"Aktiviren nicht möglich! Das modul {aktives.name} ist bereits aktiv."
                    )

#Modul abschließen 
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


#Modul auf WARTE_AUF_ERGEBNIS setzen
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


# Zeige welches Modul als nächstes laut reihenfolge kommt
    def naechstes_modul(self):
        if self.zeige_aktives_modul() is not None:
            raise ValueError("Es ist bereits ein Modul aktiv.")


        offene_module = [
            modul for modul in self.module
            if modul.status == Modulstatus.GEPLANT
        ]

        if not offene_module:
            return None
        
        return min(
            offene_module,
            key=lambda modul: modul.reihenfolge
            )
    
    def ergebnis_eintragen(self, modul, bestanden, note):
        if modul.status != Modulstatus.WARTE_AUF_ERGEBNIS:
            raise ValueError(
                "Das ausgewählte Modul hat derzeit nicht den Status "
                "WARTE_AUF_ERGEBNIS."
            )

        if bestanden:
            if note < 1 or note > 4:
                raise ValueError(
                    "Zum Bestehen muss die Note zwischen 1 und 4 liegen."
                )

            modul.note = note
            modul._schliesse_ab()

        else:
            modul.status = Modulstatus.GEPLANT


    def aktualisiere_zeitplan(self):
        aktuelles_datum = self.startdatum

        for modul in self.modul_reihenfolge():

            if modul.status == Modulstatus.ABGESCHLOSSEN:
                if modul.abschlussdatum is not None:
                    aktuelles_datum = modul.abschlussdatum
                continue

            if modul.status == Modulstatus.WARTE_AUF_ERGEBNIS:
                if modul.pruefungsdatum is not None:
                    aktuelles_datum = modul.pruefungsdatum
                continue

            if modul.status == Modulstatus.AKTIV:
                if modul.startdatum is None:
                    modul.startdatum = aktuelles_datum

                aktuelles_datum = (
                    modul.startdatum
                    + relativedelta(days=modul.geplante_dauer_tage)
                )
                continue

            if modul.status == Modulstatus.GEPLANT:
                modul.startdatum = aktuelles_datum

                aktuelles_datum = (
                    modul.startdatum
                    + relativedelta(days=modul.geplante_dauer_tage)
                )


    def prognostiziertes_studienende(self):
        self.aktualisiere_zeitplan()

        offene_module = [
            modul for modul in self.module
            if modul.status != Modulstatus.ABGESCHLOSSEN
        ]

        if not offene_module:
            return None

        letztes_modul = max(
            offene_module,
            key=lambda modul: modul.startdatum
        )

        return letztes_modul.startdatum + relativedelta(
            days=letztes_modul.geplante_dauer_tage
        )