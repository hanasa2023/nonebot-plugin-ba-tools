from datetime import date, timedelta

from nonebot import logger

from nonebot_plugin_ba_tools.features.student.domain.model.student import Student
from nonebot_plugin_ba_tools.features.student.domain.repository.student_repository import (
    StudentRepository,
)


class StudentInformationUseCase:
    """学生信息查询用例

    协调学生仓库的交互，完成学生信息的查询和检索流程。
    """

    def __init__(self, student_repository: StudentRepository) -> None:
        """初始化学生信息查询用例

        Args:
            student_repository: 学生仓库（本地数据库）
        """
        self.student_repository = student_repository

    async def get_student_by_name(self, name: str) -> Student | None:
        """根据名称查询学生信息

        支持通过学生名称或别名查询学生。

        Args:
            name: 学生名称或别名

        Returns:
            学生信息对象或 None
        """
        try:
            logger.debug(f"查询学生: {name}")
            student = await self.student_repository.get_student_by_name(name)

            if student:
                logger.debug(f"成功查询到学生: {student.name} (ID: {student.id})")
                return student
        except Exception as e:
            error_msg = f"查询学生失败: {e}"
            logger.error(error_msg, exc_info=True)
            return None

        logger.debug(f"未找到学生: {name}")
        return None

    async def get_student_birthday_info(self, name: str) -> tuple[bool, str]:
        """获取学生生日信息

        查询学生的生日信息并返回格式化的字符串。

        Args:
            name: 学生名称

        Returns:
            tuple: (成功标志, 消息)
                - success: 是否成功获取
                - message: 生日信息或错误消息
        """
        try:
            student = await self.student_repository.get_student_by_name(name)
        except Exception as e:
            error_msg = f"获取生日信息失败: {e}"
            logger.error(error_msg, exc_info=True)
            return False, f"❌ 查询失败: {e}"

        if not student:
            msg = f"未找到学生: {name}"
            logger.info(msg)
            return False, msg

        if not student.birthday:
            msg = f"{student.name} 没有生日信息"
            logger.info(msg)
            return False, msg

        birthday_str = student.birthday.to_str()
        msg = f"{student.name} 的生日是 {birthday_str}"
        logger.debug(msg)

        return True, msg

    async def search_students_by_keyword(self, keyword: str) -> list[Student]:
        """通过关键词搜索学生

        支持模糊搜索学生名称。

        Args:
            keyword: 搜索关键词

        Returns:
            list: 匹配的学生列表
        """
        try:
            logger.debug(f"搜索学生: {keyword}")
            student = await self.student_repository.get_student_by_name(keyword)

            if student:
                return [student]

        except Exception as e:
            error_msg = f"搜索学生失败: {e}"
            logger.error(error_msg, exc_info=True)
            return []

        return []

    async def get_birthday_students_today(self) -> list[Student]:
        """获取今天生日的学生

        Returns:
            list[Student]: 匹配的学生列表
        """
        try:
            logger.debug("获取今天生日的学生")
            students = await self.student_repository.get_students_by_birthday(
                date.today()
            )

            if students:
                return students

        except Exception as e:
            error_msg = f"获取今天生日的学生失败: {e}"
            logger.error(error_msg, exc_info=True)
            return []
        return []

    async def get_birthday_students_tomorrow(self) -> list[Student]:
        """获取明天生日的学生

        Returns:
            list[students]: 匹配的学生列表
        """
        try:
            logger.debug("获取明天生日的学生")
            students = await self.student_repository.get_students_by_birthday(
                date.today() + timedelta(days=1)
            )

            if students:
                return students

        except Exception as e:
            error_msg = f"获取明天生日的学生失败: {e}"
            logger.error(error_msg, exc_info=True)
            return []
        return []
