from dataclasses import dataclass

from nonebot_plugin_ba_tools.features.student.domain.model.birthday import Birthday


@dataclass
class Student:
    """学生信息模型

    表示一个学生的基本信息，包括 ID、姓名、别名、生日和头像。

    Attributes:
        id: 学生唯一标识符
        name: 学生姓名
        nicknames: 学生的别名列表
        birthday: 学生生日（只包含月和日）
        avatars: 学生头像 URL 列表
    """

    id: int
    """学生的唯一标识符"""

    name: str
    """学生的姓名"""

    nicknames: list[str]
    """学生的别名列表（如通用名、开发名等）"""

    birthday: Birthday | None
    """学生的生日（只包含月和日，不包含年份）"""

    avatars: list[str]
    """学生的头像 URL 列表"""

    school: str | None = None
    """学校"""

    club: str | None = None
    """社团"""

    star_grade: int | None = None
    """星级"""

    squad_type: str | None = None
    """编队类型（Main/Support）"""

    tactic_role: str | None = None
    """战术角色"""

    position: str | None = None
    """站位"""

    bullet_type: str | None = None
    """攻击属性"""

    armor_type: str | None = None
    """护甲类型"""

    weapon_type: str | None = None
    """武器类型"""

    character_age: str | None = None
    """年龄"""

    height: str | None = None
    """身高"""

    birthday_str: str | None = None
    """生日显示用字符串"""

    character_voice: str | None = None
    """声优"""

    illustrator: str | None = None
    """画师"""

    hobby: str | None = None
    """爱好"""

    profile_introduction: str | None = None
    """简介"""

    street_adaptation: int | None = None
    """街道适应性"""

    outdoor_adaptation: int | None = None
    """室外适应性"""

    indoor_adaptation: int | None = None
    """室内适应性"""

    def has_birthday_today(self) -> bool:
        """检查今天是否是这个学生的生日

        Returns:
            bool: 如果今天是学生生日则返回 True
        """
        if self.birthday is None:
            return False
        return self.birthday.matches_today()

    def get_display_name(self) -> str:
        """获取学生的显示名称

        优先返回主名称，如果有别名则加括号显示。

        Returns:
            str: 格式化的学生名称
        """
        if self.nicknames:
            nicknames_str = "、".join(self.nicknames)
            return f"{self.name}（{nicknames_str}）"
        return self.name

    def get_primary_avatar(self) -> str | None:
        """获取主头像 URL

        Returns:
            str | None: 主头像 URL，如果没有头像则返回 None
        """
        return self.avatars[0] if self.avatars else None
