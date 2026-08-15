from uni_speedrun.database.repository import StudienplanRepository
from uni_speedrun.fachmodell.studienplan import Studienplan


class SQLiteStudienplanRepository(StudienplanRepository):
    def __init__(self, datenbank_pfad: str) -> None:
        self.datenbank_pfad = datenbank_pfad

    def speichern(self, studienplan: Studienplan) -> None:
        pass

    def laden(self) -> Studienplan | None:
        pass