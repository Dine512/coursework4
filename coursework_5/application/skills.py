from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit

class Skill(ABC):
    """
    Базовый класс умения
    """
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def _is_stamina_enough(self):
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем просто use
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough():
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    _name = "Свирепый пинок"
    _stamina = 6
    _damage = 12

    @property
    def name(self):
        return self._name

    @property
    def stamina(self):
        return self._stamina

    @property
    def damage(self):
        return self._damage

    def skill_effect(self):
        # TODO логика использования скилла -> return str
        # TODO в классе нам доступны экземпляры user и target - можно использовать любые их методы
        # TODO именно здесь происходит уменшение стамины у игрока применяющего умение и
        # TODO уменьшение здоровья цели.
        # TODO результат применения возвращаем строкой
        self.user.stamina -= self.stamina
        self.target.hp -= self.damage
        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику"


class HardShot(Skill):
    _name = "Мощный укол"
    _stamina = 5
    _damage = 15

    @property
    def name(self):
        return self._name

    @property
    def stamina(self):
        return self._stamina

    @property
    def damage(self):
        return self._damage

    def skill_effect(self):
        self.user.stamina -= self.stamina
        self.target.hp -= self.damage
        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику"
