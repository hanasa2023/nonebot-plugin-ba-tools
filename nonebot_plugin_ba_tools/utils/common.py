import json
from pathlib import Path

import httpx

from ..config import plugin_config
from .constants import (
    BIRTHDAY_INFO_GROUP_LIST_FILE,
    DATA_STUDENT_JSON_FOLDER_PATH,
    DATA_STUDENTS_JSON_FILE_PATH,
)
from .dataloader import DataLoader, DataLoadError
from .types import Student

# TODO: 构建一个student map，能够通过 生日/姓名/别名... 查询学生


def load_group_list() -> list[int]:
    """
    获取已订阅的群组列表
    """
    full_path: Path = plugin_config.setting_path / BIRTHDAY_INFO_GROUP_LIST_FILE
    with open(full_path, "r", encoding="utf-8") as f:
        group_list: list[int] = json.load(f)
        return group_list


async def get_student_by_id(student_id: int) -> Student:
    """获取学生信息

    Args:
        student_id (int): 学生ID

    Returns:
        Student: 对应id的学生信息
    """
    student_folder = plugin_config.assert_path / DATA_STUDENT_JSON_FOLDER_PATH
    student_json_path = student_folder / f"{student_id}.json"
    if student_json_path.exists():
        with open(student_json_path, "r", encoding="utf-8") as f:
            return Student.model_validate(json.load(f))
    if not student_folder.exists():
        student_folder.mkdir(parents=True, exist_ok=True)

    students: list[Student] = await DataLoader(DATA_STUDENTS_JSON_FILE_PATH).load()
    for student in students:
        this_student_json_path = student_folder / f"{student.id}.json"
        if not this_student_json_path.exists():
            with open(this_student_json_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(student, ensure_ascii=False, indent=4))
        if student.id == student_id:
            with open(student_json_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(student, ensure_ascii=False, indent=4))
            return student
    raise DataLoadError(f"ID为{student_id}的学生不存在！")


async def get_all_students() -> list[Student]:
    """获取所有学生信息

    Returns:
        list[Student]: 所有学生信息的列表
    """
    return await DataLoader(DATA_STUDENTS_JSON_FILE_PATH).load()


async def get_data_from_html(url: str) -> str:
    """获取指定url的网页数据

    Args:
        url (str): 指定的url
    """
    async with httpx.AsyncClient() as ctx:
        response: httpx.Response = await ctx.get(url)
        response.encoding = "utf-8"
        return response.text
