from abc import ABC, abstractmethod
from .capability import TransformCapability

class Creature(ABC):
    def __init__(self, name: str, creature_type: str) -> None:
        self._name = name
        self._creature_type = creature_type

    def describe(self) -> str:
        return f"{self._name} is a {self._creature_type} type Creature"

    @abstractmethod
    def attack(self) -> str:
        pass


class Flameling(Creature):
    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")

    def attack(self) -> str:
        return "Flameling uses Ember!"


class Pyrodon(Creature):
    def __init__(self) -> None:
        super().__init__("Pyrodon", "Fire/Flying")

    def attack(self) -> str:
        return "Pyrodon uses Flamethrower!"


class Shiftling(Creature, TransformCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Shiftling", "Normal")
        TransformCapability.__init__(self)


if __name__ == "__main__":
    flameling = Flameling()
    pyrodon = Pyrodon()

    print(flameling.describe())
    print(flameling.attack())
    print(pyrodon.describe())
    print(pyrodon.attack())
