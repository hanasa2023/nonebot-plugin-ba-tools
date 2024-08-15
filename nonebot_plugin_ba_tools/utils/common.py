import json

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
    group_list: list[int]
    full_path = plugin_config.setting_path / BIRTHDAY_INFO_GROUP_LIST_FILE
    with open(full_path, "r", encoding="utf-8") as f:
        group_list = json.load(f)
    return group_list


async def get_student_by_id(student_id: int) -> Student:
    """
    获取学生信息
    @param student_id: 学生ID
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
    """获取所有学生信息"""
    return await DataLoader(DATA_STUDENTS_JSON_FILE_PATH).load()
