from nonebot import require
from nonebot_plugin_orm import Model
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column


class Students(Model):
    """学生信息表

    存储学生的基本信息，包括 ID、姓名、别名、生日（月和日）和头像。
    """

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    """学生的唯一标识符"""

    name: Mapped[str]
    """学生的姓名"""

    nicknames: Mapped[list[str]] = mapped_column(JSON, default=list)
    """学生的别名列表（JSON 格式）"""

    birthday_month: Mapped[int | None] = mapped_column(nullable=True)
    """学生生日的月份 (1-12)，可为 None"""

    birthday_day: Mapped[int | None] = mapped_column(nullable=True)
    """学生生日的日期 (1-31)，可为 None"""

    avatars: Mapped[list[str]] = mapped_column(JSON, default=list)
    """学生的头像 URL 列表（JSON 格式）"""
