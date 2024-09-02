from __future__ import annotations

import re
from datetime import datetime

from nonebot import require

from nonebot_plugin_ba_tools.utils.types import Student

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler  # noqa: E402

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import Target, UniMessage  # noqa: E402

from ..utils.common import get_all_students, load_group_list  # noqa: E402
from ..utils.constants import ASSERTS_URL  # noqa: E402
from .command import *  # noqa: E402, F403


@scheduler.scheduled_job("cron", hour=0, minute=0, id="send_birthday_info")
async def send_birthday_info() -> None:
    # 解析student.json
    logger.debug("处理生日信息推送")  # noqa: F405
    students: list[Student] = await get_all_students()

    # 获取当前已订阅的群组列表
    group_list: list[int] = load_group_list()

    # 获取当前月份及日期
    current_datetime: datetime = datetime.now()
    current_month: int = current_datetime.month
    current_day: int = current_datetime.day
    logger.debug(f"m:{current_month}, d: {current_day}")  # noqa: F405
    # 创建hasp map用来过滤重复学生
    hash_map: dict[str, bool] = {}

    for student in students:
        match: re.Match[str] | None = re.search(r"(\d+)月(\d+)日", student.birthday)
        if match:
            month: str = match.group(1)
            day: str = match.group(2)
            # 若该学生今日生日，则推送群消息
            if (
                int(month) == current_month
                and int(day) == current_day
                and hash_map.get(student.personal_name) is None
            ):
                hash_map[student.personal_name] = True

                message = (
                    UniMessage.text(
                        f"今天是{student.name}的生日哦，在学生值日的前提下，切换为非l2d的值日模式，可以听到特殊语音哦。让我们一起祝福{student.name}生日快乐吧!"
                    )
                    .emoji(id="144")
                    .image(url=ASSERTS_URL + f"/images/student/l2d/{student.id}.webp")
                )
                # 在订阅此消息的群聊中推送学生生日消息
                for group_id in group_list:
                    logger.debug(f"group_id: {group_id}")  # noqa: F405
                    target: Target = Target(str(group_id))
                    await message.send(target=target)
