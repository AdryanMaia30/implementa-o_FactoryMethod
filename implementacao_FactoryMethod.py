from abc import ABC, abstractmethod


class Character(ABC):

    @abstractmethod
    def attack(self) -> str:
        pass


class Warrior(Character):

    def attack(self) -> str:
        return "O Guerreiro ataca com sua espada."


class Mage(Character):

    def attack(self) -> str:
        return "O Mago lança uma bola de fogo."


class Archer(Character):

    def attack(self) -> str:
        return "O Arqueiro dispara uma flecha precisa."


class Rogue(Character):

    def attack(self) -> str:
        return "O Ladino ataca rapidamente pelas sombras."


class CharacterCreator(ABC):

    @abstractmethod
    def factory_method(self) -> Character:
        pass

    def perform_attack(self) -> str:
        character = self.factory_method()
        return character.attack()


class WarriorCreator(CharacterCreator):

    def factory_method(self) -> Character:
        return Warrior()


class MageCreator(CharacterCreator):

    def factory_method(self) -> Character:
        return Mage()


class ArcherCreator(CharacterCreator):

    def factory_method(self) -> Character:
        return Archer()


class RogueCreator(CharacterCreator):

    def factory_method(self) -> Character:
        return Rogue()


def client_code(creator: CharacterCreator) -> None:
    print(creator.perform_attack())


if __name__ == "__main__":
    client_code(WarriorCreator())
    client_code(MageCreator())
    client_code(ArcherCreator())
    client_code(RogueCreator())