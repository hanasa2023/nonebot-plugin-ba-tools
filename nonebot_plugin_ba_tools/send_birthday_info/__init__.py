import re
from datetime import datetime
from typing import Dict

from nonebot import get_plugin_config, require

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import Emoji, Image, Target, UniMessage

from ..config import Config
from ..utils.constants import ASSERTS_URL
from .utils.types import StudentParser

plugin_config = get_plugin_config(Config)

# TODO:实现使用命令增加/删除订阅群聊


@scheduler.scheduled_job("cron", hour=0, minute=0, id="send_birthday_info")
async def send_birthday_info():
    # 解析student.json
    parser = StudentParser(url=ASSERTS_URL + "/data/zh/students.json")
    students = await parser.parse()
    # 获取当前月份及日期
    current_datetime = datetime.now()
    current_month = current_datetime.month
    current_day = current_datetime.day
    # 创建hasp map用来过滤重复学生
    hash_map: Dict[str, bool] = {}

    for student in students:
        match = re.search(r"(\d+)月(\d+)日", student.birthday)
        if match:
            month: str = match.group(1)
            day: str = match.group(2)
            # 若该学生今日生日，则推送群消息
            if (
                int(month) == current_month
                and int(day) == current_day
                and hash_map.get(student.personal_name) == None
            ):
                hash_map[student.personal_name] = True

                message = UniMessage(
                    [
                        f"今天是{student.name}的生日哦，在学生值日的前提下，切换为非l2d的值日模式，可以听到特殊语音哦。让我们一起祝福{student.name}生日快乐吧!",
                        Emoji(id="144"),
                        Image(
                            url=ASSERTS_URL + f"/images/student/l2d/{student.id}.webp"
                        ),
                    ]
                )
                # 在订阅此消息的群聊中推送学生生日消息
                for group_id in plugin_config.send_daily_info_group_list:
                    target = Target(group_id)
                    await message.send(target=target)
