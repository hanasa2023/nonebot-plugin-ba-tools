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

    school: Mapped[str | None] = mapped_column(nullable=True)
    """学校"""

    club: Mapped[str | None] = mapped_column(nullable=True)
    """社团"""

    star_grade: Mapped[int | None] = mapped_column(nullable=True)
    """星级"""

    squad_type: Mapped[str | None] = mapped_column(nullable=True)
    """编队类型"""

    tactic_role: Mapped[str | None] = mapped_column(nullable=True)
    """战术角色"""

    position: Mapped[str | None] = mapped_column(nullable=True)
    """站位"""

    bullet_type: Mapped[str | None] = mapped_column(nullable=True)
    """攻击属性"""

    armor_type: Mapped[str | None] = mapped_column(nullable=True)
    """护甲类型"""

    weapon_type: Mapped[str | None] = mapped_column(nullable=True)
    """武器类型"""

    character_age: Mapped[str | None] = mapped_column(nullable=True)
    """年龄"""

    height: Mapped[str | None] = mapped_column(nullable=True)
    """身高"""

    birthday_str: Mapped[str | None] = mapped_column(nullable=True)
    """生日显示用字符串"""

    character_voice: Mapped[str | None] = mapped_column(nullable=True)
    """声优"""

    illustrator: Mapped[str | None] = mapped_column(nullable=True)
    """画师"""

    hobby: Mapped[str | None] = mapped_column(nullable=True)
    """爱好"""

    profile_introduction: Mapped[str | None] = mapped_column(nullable=True)
    """简介"""

    street_adaptation: Mapped[int | None] = mapped_column(nullable=True)
    """街道适应性"""

    outdoor_adaptation: Mapped[int | None] = mapped_column(nullable=True)
    """室外适应性"""

    indoor_adaptation: Mapped[int | None] = mapped_column(nullable=True)
    """室内适应性"""
