import json
from typing import Any, Dict, List

from httpx import AsyncClient


class Student:
    def __init__(self, data: Dict[str, Any]):
        self.id = str(data.get("Id"))
        self.is_released = [d for d in data.get("IsReleased", [])]
        self.name = str(data.get("Name"))
        self.personal_name = str(data.get("PersonalName"))
        self.birthday = str(data.get("Birthday"))
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
    """对students.json的解析类，若file_path属性不为空，则从本地解析文件，若file_path为空且url不为空，则解析网络文件，否则抛出异常"""

    def __init__(self, file_path: str | None = None, url: str | None = None):
        self.file_path = file_path
        self.url = url

    async def parse(self) -> List[Student]:
        """students.json的解析方法

        Returns:
            List[Student]: Student类的列表
        """
        if self.file_path:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Student(student) for student in data]
        elif self.url:
            async with AsyncClient() as client:
                response = await client.get(self.url)
                response.raise_for_status()
                data = response.json()
                return [Student(student) for student in data]
        else:
            raise DataLoadError("数据加载错误,请检查file_path或url是否填写")
