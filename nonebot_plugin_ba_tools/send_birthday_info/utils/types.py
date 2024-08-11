import json
from typing import List, Dict, Any


class Student:
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get("Id")
        self.is_released = data.get("IsReleased")
        self.name = data.get("Name")
        self.personal_name = data.get("PersonalName")
        self.birthday = data.get("Birthday")
        self.skills = [Skill(skill) for skill in data.get("Skills", [])]
        self.weapon = Weapon(data.get("Weapon", {}))
        self.gear = Gear(data.get("Gear", {}))
        self.summons = [Summon(summon) for summon in data.get("Summons", [])]


class Skill:
    def __init__(self, data: Dict[str, Any]):
        self.skill_type = data.get("SkillType")
        self.effects = [Effect(effect) for effect in data.get("Effects", [])]


class Effect:
    def __init__(self, data: Dict[str, Any]):
        self.type = data.get("Type")
        self.value = data.get("Value")
        # Add other fields as necessary


class Weapon:
    def __init__(self, data: Dict[str, Any]):
        self.name = data.get("Name")
        self.desc = data.get("Desc")
        # Add other fields as necessary


class Gear:
    def __init__(self, data: Dict[str, Any]):
        self.released = data.get("Released")
        # Add other fields as necessary


class Summon:
    def __init__(self, data: Dict[str, Any]):
        self.name = data.get("Name")
        self.desc = data.get("Desc")
        # Add other fields as necessary


class StudentParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse(self) -> List[Student]:
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Student(student) for student in data]


class BirthdayItem:
    def __init__(self, Id: int, Name: str, PersonalName: str, Birthday: str) -> None:
        self.id = Id
        self.name = Name
        self.personal_name = PersonalName
        self.birthday = Birthday


class BirthdayItemParser:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def parse(self) -> List[BirthdayItem]:
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [BirthdayItem(**d) for d in data]
