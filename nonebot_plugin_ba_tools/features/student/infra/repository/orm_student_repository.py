from datetime import date

from nonebot import logger
from nonebot_plugin_orm import AsyncSession
from sqlalchemy import and_, or_
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.sql import func, select

from nonebot_plugin_ba_tools.features.student.domain.model.birthday import Birthday
from nonebot_plugin_ba_tools.features.student.domain.model.student import Student
from nonebot_plugin_ba_tools.features.student.domain.repository.student_repository import (
    StudentRepository,
)
from nonebot_plugin_ba_tools.features.student.infra.table.students import Students

# 批处理大小：每次提交的学生数量
BATCH_SIZE = 50


class OrmStudentRepository(StudentRepository):
    """学生信息 ORM 仓库实现

    负责学生信息的数据库操作，包括查询和更新。
    """

    def __init__(self, session: AsyncSession) -> None:
        """初始化仓库

        Args:
            session: 数据库会话
        """
        self.session = session

    async def count(self) -> int:
        stmt = select(func.count(Students.id))
        result = await self.session.execute(stmt)
        cnt = result.scalar()
        return cnt if cnt else 0

    async def get_student_by_name(self, name: str) -> Student | None:
        """根据学生姓名或别名获取学生信息

        Args:
            name: 学生姓名或别名

        Returns:
            Student | None: 学生对象或 None
        """
        stmt = select(Students).where(
            or_(
                Students.name.contains(name),
                Students.nicknames.contains(name),
            )
        )
        result = await self.session.execute(stmt)
        student_orm = result.scalars().first()
        if student_orm is None:
            return None
        return self._to_domain(student_orm)

    async def get_students_by_birthday(self, target_date: date) -> list[Student]:
        """获取指定日期过生日的学生

        Args:
            target_date: 目标日期（datetime 或 date 对象）

        Returns:
            list[Student]: 在指定日期过生日的学生列表
        """
        # 提取月和日
        month = target_date.month
        day = target_date.day

        # 查询数据库中月和日匹配的学生
        stmt = select(Students).where(
            and_(
                Students.birthday_month == month,
                Students.birthday_day == day,
            )
        )
        result = await self.session.execute(stmt)
        students_orm = result.scalars().all()

        return [self._to_domain(student) for student in students_orm]

    async def update_students(self, students: list[Student]) -> None:
        """批量插入或更新学生信息

        使用分批处理的方式来优化性能，避免单次事务过大导致的锁定问题。

        Args:
            students: 学生信息列表

        Raises:
            Exception: 数据库操作异常
        """
        if not students:
            return

        total = len(students)
        logger.info(f"开始批处理更新 {total} 个学生信息（批大小: {BATCH_SIZE}）")

        # 按批次处理学生数据
        for batch_start in range(0, total, BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE, total)
            batch_students = students[batch_start:batch_end]

            # 构建行数据，转换 Birthday 值对象为数据库字段
            student_rows = []
            for student in batch_students:
                row = {
                    "id": student.id,
                    "name": student.name,
                    "nicknames": student.nicknames,
                    "avatars": student.avatars,
                }

                # 处理 Birthday 值对象
                if student.birthday is not None:
                    row["birthday_month"] = student.birthday.month
                    row["birthday_day"] = student.birthday.day
                else:
                    row["birthday_month"] = None
                    row["birthday_day"] = None

                student_rows.append(row)

            try:
                stmt = insert(Students).values(student_rows)
                upsert_stmt = stmt.on_conflict_do_update(
                    index_elements=[Students.id],
                    set_={
                        Students.name: stmt.excluded.name,
                        Students.nicknames: stmt.excluded.nicknames,
                        Students.birthday_month: stmt.excluded.birthday_month,
                        Students.birthday_day: stmt.excluded.birthday_day,
                        Students.avatars: stmt.excluded.avatars,
                    },
                )
                await self.session.execute(upsert_stmt)
                await self.session.commit()

                logger.debug(
                    f"已处理 {batch_end}/{total} 个学生信息"
                    f" (批次 {batch_start // BATCH_SIZE + 1})"
                )
            except Exception as e:
                logger.error(
                    f"批处理更新学生数据失败 (批次范围 {batch_start}-{batch_end}): {e}",
                    exc_info=True,
                )
                await self.session.rollback()
                raise

        logger.info(f"成功批处理更新所有 {total} 个学生信息")

    def _to_domain(self, student_orm: Students) -> Student:
        """将 ORM 模型转换为领域模型

        Args:
            student_orm: ORM 学生对象

        Returns:
            Student: 领域模型学生对象
        """
        # 从数据库字段重建 Birthday 值对象
        birthday = None
        if (
            student_orm.birthday_month is not None
            and student_orm.birthday_day is not None
        ):
            birthday = Birthday(
                month=student_orm.birthday_month,
                day=student_orm.birthday_day,
            )

        return Student(
            id=student_orm.id,
            name=student_orm.name,
            nicknames=student_orm.nicknames,
            birthday=birthday,
            avatars=student_orm.avatars,
        )
