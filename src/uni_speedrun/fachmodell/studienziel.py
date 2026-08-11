from datetime import date
from dateutil.relativedelta import relativedelta


class Studienziel:
    def __init__(self, name: str, zielects: int, zieldauer: int):
        self.name = name
        self.zielects = zielects
        self.zieldauer = zieldauer
        self.startdatum = date.today()


    def zieldatum(self):
        return self.startdatum + relativedelta(months=self.zieldauer)