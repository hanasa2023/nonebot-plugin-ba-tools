from nonebot import logger

from nonebot_plugin_ba_tools.features.student.domain.model.student import Student
from nonebot_plugin_ba_tools.features.student.domain.port.student_data_gateway import (
    StudentDataGateway,
)
from nonebot_plugin_ba_tools.features.student.domain.repository.student_repository import (
    StudentRepository,
)


class StudentDataSynchronizer:
    """学生数据同步用例

    协调学生数据网关（外部数据源）和学生仓库（本地存储）的交互，
    完成学生数据的拉取、验证和存储流程。
    """

    def __init__(
        self,
        student_data_gateway: StudentDataGateway,
        student_repository: StudentRepository,
    ) -> None:
        """初始化学生数据同步器

        Args:
            student_data_gateway: 学生数据网关（如 SchaleDB API）
            student_repository: 学生仓库（本地数据库）
        """
        self.student_data_gateway = student_data_gateway
        self.student_repository = student_repository

    async def check_synchronization(self) -> None:
        """检查是否需要同步学生数据，如果需要则执行同步"""
        if await self.student_repository.count() == 0:
            logger.info("学生数据表为空，开始同步……")
            await self.synchronize()

    async def synchronize(self) -> str:
        """执行学生数据同步

        从外部数据源获取最新的学生数据，与本地数据库进行同步（插入或更新）。

        Returns:
            str : 描述信息

        Raises:
            Exception: 网络请求或数据库操作失败
        """
        try:
            logger.info("开始学生数据同步流程")

            # 从网关获取数据
            students = await self._fetch_students()

            if not students:
                return "未能从数据源获取学生数据"

            logger.info(f"成功获取 {len(students)} 个学生信息")

            # 验证数据
            valid_students = self._validate_students(students)

            if not valid_students:
                return f"获取 {len(students)} 个学生，但没有有效数据"

            # 同步到数据库
            await self.student_repository.update_students(valid_students)

            message = f"✅ 学生数据同步成功！共同步 {len(valid_students)} 个学生"
            logger.info(message)

        except Exception as e:
            error_msg = f"学生数据同步失败: {e}"
            logger.error(error_msg, exc_info=True)
            return f"❌ 同步失败: {e}"
        return message

    async def _fetch_students(self) -> list[Student]:
        """从数据网关获取学生数据

        Returns:
            list[Student]: 学生列表

        Raises:
            Exception: 网络请求失败或数据格式错误
        """
        async with self.student_data_gateway:
            return await self.student_data_gateway.fetch_all_students()

    @staticmethod
    def _validate_students(students: list[Student]) -> list[Student]:
        """验证学生数据的有效性

        筛选出有效的学生数据，跳过不完整或无效的记录。

        Args:
            students: 学生列表

        Returns:
            list[Student]: 有效的学生列表
        """
        valid_students = []

        for student in students:
            # 基本的有效性检查
            if not student.id or not student.name:
                logger.warning(
                    f"跳过无效学生数据: id={student.id}, name={student.name}"
                )
                continue

            valid_students.append(student)

        if len(valid_students) < len(students):
            logger.warning(
                f"有效学生数 {len(valid_students)}/{len(students)}, "
                f"跳过 {len(students) - len(valid_students)} 条无效数据"
            )

        return valid_students
