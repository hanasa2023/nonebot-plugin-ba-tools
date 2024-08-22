from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from nonebot import require
from nonebot.adapters.onebot.v11 import Bot

from nonebot_plugin_ba_tools.get_student_birthday.utils.draw_img import (
    init_birthday_img,
)

from ..config import plugin_config
from ..utils.common import get_students_by_birth_month
from ..utils.constants import DATA_STUDENTS_BIRTHDAY_IMG_PATH
from ..utils.types import Student

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import (  # noqa: E402
    Alconna,
    AlconnaMatcher,
    Args,
    Image,
    Match,
    UniMessage,
    on_alconna,
)

birthday_list: Alconna[Any] = Alconna("ba学生生日表", Args["month", str])
get_student_birthday_list: type[AlconnaMatcher] = on_alconna(
    birthday_list, use_cmd_start=True
)


@get_student_birthday_list.assign("month")
async def _(bot: Bot, month: Match[str]) -> None:
    if month.available:
        month_match: re.Match[str] | None = re.search(r"(\d+)月", month.result)
        if month_match or month.result == "当月":
            pre_msg: dict[str, int] = {"message_id": -1}
            real_month: str = (
                month_match.group(1) if month_match else str(datetime.now().month)
            )
            students: list[Student] = await get_students_by_birth_month(real_month)
            if len(students):
                if plugin_config.loading_switch:
                    pre_msg = await get_student_birthday_list.send("图片正在准备喵~")
                await init_birthday_img(students, real_month)
                msg: UniMessage[Image] = UniMessage(
                    Image(
                        path=plugin_config.assert_path
                        / f"{DATA_STUDENTS_BIRTHDAY_IMG_PATH}/{real_month}.png"
                    )
                )
                await get_student_birthday_list.send(msg)
                if plugin_config.loading_switch:
                    await bot.delete_msg(message_id=pre_msg["message_id"])
                await get_student_birthday_list.finish()
            else:
                await get_student_birthday_list.finish("是无效的月份呢")
