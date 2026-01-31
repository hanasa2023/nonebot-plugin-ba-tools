from calendar import monthcalendar
from collections import defaultdict
from datetime import date, timedelta

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
        """初始化学生信息查询用例

        Args:
            student_repository: 学生仓库（本地数据库）
            html_render_service: HTML 渲染服务
        """
        self.student_repository = student_repository
        self.html_render_service = html_render_service

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

    async def generate_birthday_calendar(
        self,
        month: str,
    ) -> bytes:
        """生成生日日历

        Returns:
            bytes: 生日日历
        """

        parsed_month = StudentInformationUseCase.parse_month(month)
        if parsed_month is None:
            raise ValueError("非法的月份")

        try:
            logger.debug("生成生日日历")
            today = date.today()
            data = {
                "title": f"{today.year}年{parsed_month}月",
                "days": [],
            }
            students = await self.student_repository.get_students_by_month(parsed_month)
            students_dict_by_day = defaultdict(list)
            for student in students:
                if student.birthday:
                    students_dict_by_day[student.birthday.day].append(student)
            cal = monthcalendar(today.year, parsed_month)
            for week in cal:
                for day_num in week:
                    day_dict = {
                        "day_number": day_num,
                        "is_today": day_num == today.day,
                        "is_other_month": (day_num == 0),
                        "students": [
                            {
                                "name": stu.name,
                                "avatar": stu.avatars[0],
                            }
                            for stu in students_dict_by_day[day_num]
                        ],
                    }
                    data["days"].append(day_dict)

            return await self.html_render_service.render_from_template(
                template_name="birthday_calendar.html",
                data=data,
            )
        except Exception as e:
            logger.error(f"生成生日日历失败: {e}")
            raise

    async def generate_birthday_heatmap(self) -> bytes:
        """生成全年生日热力图

        Returns:
            bytes: 热力图图片
        """

        try:
            logger.debug("生成全年生日热力图")
            today = date.today()
            months_data = []

            for m in range(1, 13):
                students = await self.student_repository.get_students_by_month(m)
                students_dict_by_day: dict[int, list[Student]] = defaultdict(list)
                for student in students:
                    if student.birthday:
                        students_dict_by_day[student.birthday.day].append(student)

                cal = monthcalendar(today.year, m)
                weeks = []
                for week in cal:
                    week_data = []
                    for day_num in week:
                        count = len(students_dict_by_day[day_num]) if day_num != 0 else 0
                        week_data.append({
                            "day_number": day_num,
                            "is_other_month": (day_num == 0),
                            "is_today": (
                                day_num == today.day and m == today.month
                            ),
                            "count": count,
                            "level": (
                                0 if count == 0
                                else 1 if count == 1
                                else 2 if count == 2
                                else 3
                            ),
                        })
                    weeks.append(week_data)

                months_data.append({
                    "name": f"{m}月",
                    "weeks": weeks,
                })

            data = {
                "title": f"{today.year}年 生日热力图",
                "months": months_data,
            }

            return await self.html_render_service.render_from_template(
                template_name="birthday_heatmap.html",
                data=data,
            )
        except Exception as e:
            logger.error(f"生成生日热力图失败: {e}")
            raise

    async def generate_student_info_card(self, name: str) -> bytes | None:
        """生成学生信息卡片

        Args:
            name: 学生名称或别名

        Returns:
            bytes | None: 信息卡片图片，未找到学生时返回 None
        """
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

    @staticmethod
    def parse_month(date_str: str) -> int | None:
        """
        从字符串解析月份 (支持: "1月", "01", "一月", "十一", "1")

        Args:
            date_str: 输入的月份字符串

        Returns:
            int: 月份 (1-12)
            None: 解析失败
        """
        if not date_str:
            return None

        clean_str = date_str.strip().rstrip("月").strip()

        if clean_str.isdigit():
            month = int(clean_str)
            return month if 1 <= month <= 12 else None

        cn_map = {
            "一": 1,
            "二": 2,
            "两": 2,
            "三": 3,
            "四": 4,
            "五": 5,
            "六": 6,
            "七": 7,
            "八": 8,
            "九": 9,
            "十": 10,
            "十一": 11,
            "十二": 12,
        }

        if clean_str in cn_map:
            return cn_map[clean_str]

        return None
