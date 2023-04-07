from skills import Skill, FuryPunch, HardShot
from dataclasses import dataclass


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorClass = UnitClass("Воин", 60, 30, 0.8, 0.9, 1.2, FuryPunch()) # TODO Инициализируем экземпляр класса UnitClass и присваиваем ему необходимые значения аттрибуотов

ThiefClass = UnitClass("Вор", 50, 25, 1.5, 1.2, 1, HardShot()) # TODO действуем так же как и с войном

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}
