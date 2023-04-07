from dataclasses import dataclass, field
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    name: str
    defence: int
    stamina_per_turn: float

    class Meta:
        unknown = marshmallow.EXCLUDE

@dataclass
class Weapon:
    name: str
    min_damage: int
    max_damage: int
    stamina_per_hit: float


    @property
    def damage(self):
        return uniform(self.min_damage, self.max_damage)

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class EquipmentData:
    # TODO содержит 2 списка - с оружием и с броней
    weapon_list: List[Weapon] = field(metadata={"data_key": "weapons"})
    armor_list: List[Armor] = field(metadata={"data_key": "armors"})


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        # TODO возвращает объект оружия по имени
        for weapon in self.equipment.weapon_list:
            if weapon.name == weapon_name:
                return weapon
        pass

    def get_armor(self, armor_name) -> Armor:
        # TODO возвращает объект брони по имени
        for armor in self.equipment.armor_list:
            if armor.name == armor_name:
                return armor
        pass

    def get_weapons_names(self) -> list:
        # TODO возвращаем список с оружием
        return [weapon.name for weapon in self.equipment.weapon_list]

    def get_armors_names(self) -> list:
        # TODO возвращаем список с броней
        return [armor.name for armor in self.equipment.armor_list]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        # TODO этот метод загружает json в переменную EquipmentData
        equipment_file = open("../data/equipment.json", encoding='utf-8')
        data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
