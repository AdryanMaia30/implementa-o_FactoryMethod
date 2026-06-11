# Factory Method — Padrão de Projeto Criacional

> Baseado no conteúdo de [refactoring.guru/design-patterns/factory-method](https://refactoring.guru/design-patterns/factory-method)

---

## O que é o Factory Method?

O **Factory Method** é um padrão de projeto criacional que fornece uma interface para criar objetos em uma superclasse, mas permite que subclasses alterem o tipo de objeto que será criado. Em vez de instanciar objetos diretamente com o operador `new`, o padrão define um **método de fábrica** responsável por essa criação, que pode ser sobrescrito por subclasses para retornar tipos diferentes de produtos.

**Também conhecido como:** *Virtual Constructor*

---

## O Problema

Imagine que você está desenvolvendo um jogo RPG com diferentes tipos de personagens. Em uma primeira versão, só existe o Guerreiro. Boa parte do código está diretamente acoplada à classe `Warrior`.

Com o tempo, surgem novos personagens: Mago, Arqueiro, Ladino. Adicionar cada um exige mudanças em várias partes do código, resultando em condicionais espalhados por toda a base de código para controlar qual personagem instanciar.

---

## A Solução

O padrão sugere substituir as chamadas diretas de construção de objetos por chamadas a um **método de fábrica** especializado. Os objetos continuam sendo criados com `new`, mas isso ocorre dentro do método de fábrica. As subclasses podem sobrescrever esse método para alterar o tipo de objeto retornado.

Existe uma limitação: as subclasses só podem retornar tipos diferentes de produtos se esses produtos tiverem uma **interface ou classe base comum**. O tipo de retorno do método de fábrica deve ser declarado com base nessa interface.

---

## Estrutura do Padrão

```
    <<abstract>>
     Character             ← Product (interface comum)
    + attack(): str

   /    |    \    \
Warrior Mage Archer Rogue  ← Concrete Products

    <<abstract>>
  CharacterCreator          ← Creator
  + factory_method()        ← método de fábrica (abstrato)
  + perform_attack()        ← lógica de negócio que usa o produto

  /       |       \      \
WarriorCreator MageCreator ArcherCreator RogueCreator
                                         ← Concrete Creators
```

Os quatro papéis do padrão:

| Papel | Descrição | No código |
|---|---|---|
| **Product** | Interface comum a todos os produtos | `Character` (ABC) |
| **Concrete Products** | Implementações concretas do produto | `Warrior`, `Mage`, `Archer`, `Rogue` |
| **Creator** | Declara o método de fábrica; contém a lógica de negócio | `CharacterCreator` (ABC) |
| **Concrete Creators** | Sobrescrevem o método de fábrica | `WarriorCreator`, `MageCreator`, etc. |

---

## O Código

```python
from abc import ABC, abstractmethod

# ── Product ──────────────────────────────────────────────────
class Character(ABC):
    @abstractmethod
    def attack(self) -> str:
        pass

# ── Concrete Products ─────────────────────────────────────────
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

# ── Creator ───────────────────────────────────────────────────
class CharacterCreator(ABC):
    @abstractmethod
    def factory_method(self) -> Character:
        pass

    def perform_attack(self) -> str:
        character = self.factory_method()   # delega a criação
        return character.attack()           # usa o produto

# ── Concrete Creators ─────────────────────────────────────────
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

# ── Client code ───────────────────────────────────────────────
def client_code(creator: CharacterCreator) -> None:
    print(creator.perform_attack())

if __name__ == "__main__":
    client_code(WarriorCreator())
    client_code(MageCreator())
    client_code(ArcherCreator())
    client_code(RogueCreator())
```

**Saída:**
```
O Guerreiro ataca com sua espada.
O Mago lança uma bola de fogo.
O Arqueiro dispara uma flecha precisa.
O Ladino ataca rapidamente pelas sombras.
```

---

## Como Funciona (passo a passo)

1. `client_code` recebe qualquer `CharacterCreator` sem saber qual personagem será criado.
2. Chama `perform_attack()`, que está definido na classe **Creator** base.
3. `perform_attack()` delega a criação ao `factory_method()` — abstrato na base.
4. A subclasse concreta (ex.: `MageCreator`) sobrescreve `factory_method()` e retorna um `Mage`.
5. O método `attack()` é chamado no produto sem que o cliente saiba de qual classe concreta se trata.

O código cliente interage apenas com a interface `CharacterCreator` — **nenhum acoplamento direto** com `Warrior`, `Mage` ou qualquer produto concreto.

---

## Quando Usar

- Quando você **não sabe de antemão** o tipo exato do objeto que seu código precisa criar.
- Quando quer oferecer aos usuários de uma biblioteca uma forma de **estender componentes internos** sem modificar o código existente.
- Quando precisa **reutilizar objetos existentes** em vez de recriá-los sempre (ex.: pool de conexões).

---

## Prós e Contras

**Vantagens**

- Elimina o acoplamento direto entre o criador e os produtos concretos.
- Segue o **Princípio da Responsabilidade Única** — o código de criação fica em um único lugar.
- Segue o **Princípio Aberto/Fechado** — é possível adicionar novos tipos de personagens sem alterar o código existente; basta criar uma nova subclasse de `CharacterCreator` e uma nova subclasse de `Character`.

**Desvantagens**

- O código pode se tornar mais complexo, pois exige a introdução de muitas subclasses para implementar o padrão.

---

## Como Adicionar um Novo Personagem

Graças ao padrão, basta criar duas novas classes:

```python
class Paladin(Character):
    def attack(self) -> str:
        return "O Paladino golpeia com a luz divina."

class PaladinCreator(CharacterCreator):
    def factory_method(self) -> Character:
        return Paladin()

# Uso:
client_code(PaladinCreator())
# → O Paladino golpeia com a luz divina.
```

Nenhuma linha de código existente precisa ser alterada.

---

## Relações com Outros Padrões

- **Abstract Factory** — muitos projetos começam com Factory Method e evoluem para Abstract Factory quando o número de produtos relacionados cresce.
- **Template Method** — o Factory Method é uma especialização do Template Method; o método de fábrica pode ser um passo dentro de um Template Method maior.
- **Prototype** — diferente do Factory Method, o Prototype não usa herança, mas exige uma inicialização mais complexa do objeto clonado.

---
