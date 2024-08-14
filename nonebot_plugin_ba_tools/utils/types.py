from typing import List

from pydantic import BaseModel


class Effect(BaseModel):
    type: str
    hits: List[int]
    scale: List[int]


class Skill(BaseModel):
    skill_type: str
    effects: List[Effect]


class Weapon(BaseModel):
    name: str
    desc: str


class Gear(BaseModel):
    released: List[bool]


class Summon(BaseModel):
    name: str
    desc: str


# TODO: 完善对Student的解析
class Student(BaseModel):
    id: int
    is_released: List[bool]
    name: str
    personal_name: str
    birthday: str
    skills: List[Skill]
    weapon: Weapon
    gear: Gear
    summons: List[Summon]
