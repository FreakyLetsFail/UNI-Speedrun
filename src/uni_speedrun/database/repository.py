from abc import ABC, abstractmethod

from uni_speedrun.fachmodell.studienplan import Studienplan


class StudienplanRepository(ABC):

    @abstractmethod
    def speichern(self, studienplan: Studienplan) -> None:
        pass

    @abstractmethod
    def laden(self) -> Studienplan | None:
        pass