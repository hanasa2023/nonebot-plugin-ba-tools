from typing import Any, Dict, List
from .dataloader import DataLoader


class Student:
    def __init__(self, data: Dict[str, Any]):
        self.id: str = str(data.get("Id", "-1"))
        self.is_released: List[bool] = [d for d in data.get("IsReleased", [])]
        self.name: str = str(data.get("Name", "-"))
        self.personal_name: str = str(data.get("PersonalName", "-"))
        self.birthday: str = str(data.get("Birthday", "-"))
        self.skills: List[Skill] = [Skill(skill) for skill in data.get("Skills", [])]
        self.weapon: Weapon = Weapon(data.get("Weapon", {}))
        self.gear: Gear = Gear(data.get("Gear", {}))
        self.summons: List[Summon] = [Summon(summon) for summon in data.get("Summons", [])]


class Skill:
    def __init__(self, data: Dict[str, Any]):
        self.skill_type = data.get("SkillType")
        self.effects = [Effect(effect) for effect in data.get("Effects", [])]


class Effect:
    def __init__(self, data: Dict[str, Any]):
        self.type = data.get("Type")
        self.value = data.get("Value")


class Weapon:
    def __init__(self, data: Dict[str, Any]):
        self.name = data.get("Name")
        self.desc = data.get("Desc")


class Gear:
    def __init__(self, data: Dict[str, Any]):
        self.released = data.get("Released")


class Summon:
    def __init__(self, data: Dict[str, Any]):
        self.name = data.get("Name")
        self.desc = data.get("Desc")


class DataLoadError(Exception):
    pass


class StudentParser:
    """对students.json的解析类，若file_path属性不为空，则从解析本地文件，若url不为空，则解析网络文件，否则抛出异常"""

    def __init__(self, file_path: str):
        self.file_path = file_path


    async def parse(self) -> List[Student]:
        """students.json的解析方法

        Returns:
            List[Student]: Student类的列表
        """

        data = await DataLoader(self.file_path).load()
        if data is None:
            raise DataLoadError("数据加载错误,请检查file_path是否正确")
        return [Student(student) for student in data]
