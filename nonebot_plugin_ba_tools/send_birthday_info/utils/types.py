import json
from typing import Any, Dict, List

from httpx import AsyncClient, HTTPStatusError
from nonebot import logger


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

    def __init__(self, file_path: str | None = None, url: str | None = None):
        self.file_path = file_path
        self.url = url

    async def parse(self) -> List[Student]:
        """students.json的解析方法

        Returns:
            List[Student]: Student类的列表
        """
        if self.file_path:
            async with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Student(student) for student in data]
        elif self.ur:
            async with AsyncClient() as client:
                try:
                    response = await client.get(self.url)
                    response.raise_for_status()
                    data = response.json()
                    return [Student(student) for student in data]
                except HTTPStatusError as e:
                    logger.error(e)
                except Exception as e:
                    logger.error(e)
        else:
            try:
                raise DataLoadError("数据加载错误,请检查file_path或url是否正确")
            except DataLoadError as e:
                logger.error(e)
