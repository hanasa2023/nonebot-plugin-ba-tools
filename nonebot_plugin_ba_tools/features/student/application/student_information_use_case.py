from nonebot import logger

from nonebot_plugin_ba_tools.features.student.domain.model.student import Student
from nonebot_plugin_ba_tools.features.student.domain.repository.student_repository import (
    StudentRepository,
)
from nonebot_plugin_ba_tools.shared.domain.port.html_render_service import (
    HtmlRenderService,
)


class StudentInformationUseCase:
    """学生信息查询用例

    协调学生仓库的交互，完成学生信息的查询和检索流程。
    """

    def __init__(
        self,
        student_repository: StudentRepository,
        html_render_service: HtmlRenderService,
    ) -> None:
        self.student_repository = student_repository
        self.html_render_service = html_render_service

    async def get_student_by_name(self, name: str) -> Student | None:
        """根据名称查询学生信息"""
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
        """获取学生生日信息"""
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
        """通过关键词搜索学生"""
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

    async def generate_student_info_card(self, name: str) -> bytes | None:
        """生成学生信息卡片"""
        student = await self.student_repository.get_student_by_name(name)
        if not student:
            return None

        adaptation_label = {0: "D", 1: "C", 2: "B", 3: "A", 4: "S", 5: "SS"}

        data = {
            "name": student.name,
            "avatar": student.get_primary_avatar(),
            "school": student.school or "未知",
            "club": student.club or "未知",
            "star_grade": student.star_grade or 0,
            "squad_type": student.squad_type or "未知",
            "tactic_role": student.tactic_role or "未知",
            "position": student.position or "未知",
            "bullet_type": student.bullet_type or "未知",
            "armor_type": student.armor_type or "未知",
            "weapon_type": student.weapon_type or "未知",
            "character_age": student.character_age or "未知",
            "height": student.height or "未知",
            "birthday_str": student.birthday_str or "未知",
            "character_voice": student.character_voice or "未知",
            "illustrator": student.illustrator or "未知",
            "hobby": student.hobby or "未知",
            "profile_introduction": student.profile_introduction or "暂无简介",
            "street_adaptation": adaptation_label.get(student.street_adaptation or 0, "D"),
            "outdoor_adaptation": adaptation_label.get(student.outdoor_adaptation or 0, "D"),
            "indoor_adaptation": adaptation_label.get(student.indoor_adaptation or 0, "D"),
        }

        return await self.html_render_service.render_from_template(
            template_name="student_info_card.html",
            data=data,
        )
