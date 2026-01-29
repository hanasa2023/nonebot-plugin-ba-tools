from abc import ABC, abstractmethod
from datetime import date

from nonebot_plugin_ba_tools.features.student.domain.model.student import Student


class StudentRepository(ABC):
    """学生信息仓库"""

    @abstractmethod
    async def count(self) -> int:
        """获取学生数量

        Returns:
            int: 学生数量
        """

        raise NotImplementedError

    @abstractmethod
    async def get_student_by_name(self, name: str) -> Student | None:
        """根据学生姓名获取信息

        Args:
            name (str): 学生姓名

        Returns:
            Student | None: 学生信息或None
        """

        raise NotImplementedError

    @abstractmethod
    async def get_students_by_birthday(self, target_date: date) -> list[Student]:
        """获取指定日期过生日的学生

        Args:
            target_date (date): 指定日期

        Returns:
            list[Student]: 过生日的学生列表
        """

        raise NotImplementedError

    @abstractmethod
    async def update_students(self, students: list[Student]) -> None:
        """更新学生信息

        Args:
            student (Student): 学生信息
        """

        raise NotImplementedError
