from __future__ import annotations

import json
import re
from pathlib import Path

import aiofiles
import httpx

from ..config import ASSERT_DIR, SETTING_DIR, ConfigManager
from .constants import (
    BIRTHDAY_INFO_GROUP_LIST_FILE,
    DATA_STUDENT_JSON_FOLDER_PATH,
    DATA_STUDENTS_JSON_FILE_PATH,
)
from .dataloader import DataLoadError, StudentDataLoader
from .types import Student

# TODO: 构建一个student map，能够通过 生日/姓名/别名... 查询学生


async def load_group_list() -> list[int]:
    """
    获取已订阅的群组列表
    """
    full_path: Path = SETTING_DIR / BIRTHDAY_INFO_GROUP_LIST_FILE
    async with aiofiles.open(full_path, encoding="utf-8") as f:
        file_content: str = await f.read()
        group_list: list[int] = json.loads(file_content)
        return group_list


async def get_student_by_id(student_id: int) -> Student:
    """获取学生信息

    Args:
        student_id (int): 学生ID

    Returns:
        Student: 对应id的学生信息
    """
    student_folder = ASSERT_DIR / DATA_STUDENT_JSON_FOLDER_PATH
    student_json_path = student_folder / f"{student_id}.json"
    if student_json_path.exists():
        async with aiofiles.open(student_json_path, encoding="utf-8") as f:
            file_content: str = await f.read()
            return Student(**json.loads(file_content))
    if not student_folder.exists():
        student_folder.mkdir(parents=True, exist_ok=True)

    students: list[Student] = await StudentDataLoader(DATA_STUDENTS_JSON_FILE_PATH).load_students()
    for student in students:
        if student.id == student_id:
            async with aiofiles.open(student_json_path, "w", encoding="utf-8") as f:
                await f.write(json.dumps(student, ensure_ascii=False, indent=2))
            return student
        this_student_json_path = student_folder / f"{student.id}.json"
        if not this_student_json_path.exists():
            async with aiofiles.open(this_student_json_path, "w", encoding="utf-8") as f:
                await f.write(json.dumps(student, ensure_ascii=False, indent=2))
    raise DataLoadError(f"ID为{student_id}的学生不存在！")


async def get_students_by_birth_month(month: str) -> list[Student]:
    """获取生日在某月的学生列表

    Args:
        month (int): 月份

    Returns:
        list[Student]: 在某月过生日的学生列表
    """
    students_in_month: list[Student] = []
    students: list[Student] = await StudentDataLoader(DATA_STUDENTS_JSON_FILE_PATH).load_students()
    for student in students:
        birthday_match: re.Match[str] | None = re.search(r"(\d+)月(\d+)日", student.birthday)
        if birthday_match:
            month_str: str = birthday_match.group(1)
            if month_str == month:
                students_in_month.append(student)
    return students_in_month


async def get_all_students() -> list[Student]:
    """获取所有学生信息

    Returns:
        list[Student]: 所有学生信息的列表
    """
    return await StudentDataLoader(DATA_STUDENTS_JSON_FILE_PATH).load_students()


async def get_data_from_html(url: str) -> str:
    """获取指定url的网页数据

    Args:
        url (str): 指定的url
    """
    async with httpx.AsyncClient() as ctx:
        response: httpx.Response = await ctx.get(url)
        response.encoding = "utf-8"
        return response.text
