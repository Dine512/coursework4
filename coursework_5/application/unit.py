from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Equipment, Weapon, Armor
from classes import UnitClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass, weapon, armor):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = weapon
        self.armor = armor
        self._is_skill_used = False

    @property
    def health_points(self):
        return self.hp # TODO возвращаем аттрибут hp в красивом виде

    @property
    def stamina_points(self):
        return self.stamina # TODO возвращаем аттрибут hp в красивом виде

    @stamina_points.setter
    def stamina_points(self, stamina):
        self.stamina = stamina




    # def equip_weapon(self, weapon: Weapon):
    #     # TODO присваиваем нашему герою новое оружие
    #     self.weapon = weapon
    #     return f"{self.name} экипирован оружием {self.weapon.name}"
    #
    # def equip_armor(self, armor: Armor):
    #     self.armor = armor
    #     # TODO одеваем новую броню
    #     return f"{self.name} экипирован броней {self.weapon.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        # TODO Эта функция должна содержать:
        #  логику расчета урона игрока
        #  логику расчета брони цели
        #  здесь же происходит уменьшение выносливости атакующего при ударе
        #  и уменьшение выносливости защищающегося при использовании брони
        #  если у защищающегося нехватает выносливости - его броня игнорируется
        #  после всех расчетов цель получает урон - target.get_damage(damage)
        #  и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде
        base_damage = self.weapon.damage * self.unit_class.attack
        self.stamina = round(self.stamina - self.weapon.stamina_per_hit, 1)
        if target.stamina < target.armor.stamina_per_turn:
            target.get_damage(base_damage)
            return round(base_damage, 1)

        armor_target = target.armor.defence * target.unit_class.armor
        damage = base_damage - armor_target
        target.stamina = round(target.stamina - target.armor.stamina_per_turn)
        target.get_damage(damage)

        return round(damage, 1)

    def get_damage(self, damage: int):
        # TODO получение урона целью
        #      присваиваем новое значение для аттрибута self.hp
        if damage >= 0:
            self.hp = round(self.hp - damage, 1)


    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if self._is_skill_used:
            return "Навык уже использован"
        self._is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)



class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        if self.stamina_points < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage <= 0:
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."

        return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."

class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """
        if randint(1, 10) == 1:
            return self.use_skill(target)

        if self.stamina_points < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage <= 0:
            return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."

        return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
