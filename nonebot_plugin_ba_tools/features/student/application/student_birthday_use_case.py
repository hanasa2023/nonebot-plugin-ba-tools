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


class StudentBirthdayUseCase:
    """学生生日相关用例

    协调学生仓库的交互，完成学生生日信息的查询和渲染流程。
    """

    def __init__(
        self,
        student_repository: StudentRepository,
        html_render_service: HtmlRenderService,
    ) -> None:
        self.student_repository = student_repository
        self.html_render_service = html_render_service

    async def get_birthday_students_today(self) -> list[Student]:
        """获取今天生日的学生"""
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
        """获取明天生日的学生"""
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
        """生成生日日历"""

        parsed_month = StudentBirthdayUseCase.parse_month(month)
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
        """生成全年生日热力图"""

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

    @staticmethod
    def parse_month(date_str: str) -> int | None:
        """
        从字符串解析月份 (支持: "1月", "01", "一月", "十一", "1")
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
