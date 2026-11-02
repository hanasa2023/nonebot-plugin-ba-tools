from __future__ import annotations

import re
from datetime import datetime
from typing import Any

import httpx
from nonebot import require

from ..config import ASSERT_DIR, ConfigManager
from ..utils.common import get_students_by_birth_month
from ..utils.constants import ARONA_API_URL, DATA_STUDENTS_BIRTHDAY_IMG_PATH
from ..utils.types import Student
from .utils.draw_img import (
    init_birthday_img,
)

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import (
    Alconna,
    AlconnaMatcher,
    Args,
    Image,
    Match,
    Text,
    UniMessage,
    on_alconna,
)
from nonebot_plugin_alconna.uniseg import Receipt

birthday_list: Alconna[Any] = Alconna("ba学生生日表", Args["month", str])
get_student_birthday_list: type[AlconnaMatcher] = on_alconna(
    birthday_list, use_cmd_start=True
)

birthday_map: Alconna[Any] = Alconna("ba学生生日分布")
get_birthday_map: type[AlconnaMatcher] = on_alconna(birthday_map, use_cmd_start=True)


@get_student_birthday_list.assign("month")
async def _(month: Match[str]) -> None:
    if month.available:
        month_match: re.Match[str] | None = re.search(r"(\d+)月", month.result)
        if month_match or month.result == "当月":
            pre_msg: Receipt | None = None
            real_month: str = (
                month_match.group(1) if month_match else str(datetime.now().month)
            )
            students: list[Student] = await get_students_by_birth_month(real_month)
            if len(students):
                if ConfigManager.get().pic.loading_switch:
                    pre_msg = await UniMessage.text("图片正在准备喵~").send()
                await init_birthday_img(students, real_month)
                msg: UniMessage[Image] = UniMessage(
                    Image(
                        path=ASSERT_DIR
                        / f"{DATA_STUDENTS_BIRTHDAY_IMG_PATH}/{real_month}.png"
                    )
                )
                await get_student_birthday_list.send(msg)
                if ConfigManager.get().pic.loading_switch and pre_msg:
                    await pre_msg.recall()
                await get_student_birthday_list.finish()
            else:
                await get_student_birthday_list.finish("是无效的月份呢")


@get_birthday_map.handle()
async def _() -> None:
    msg: UniMessage[Image | Text] = UniMessage.text("获取失败了😢")
    async with httpx.AsyncClient() as ctx:
        response: httpx.Response = await ctx.get(
            f"{ARONA_API_URL}/api/student/birthday/distribution"
        )
        if response.status_code == 200:
            msg = UniMessage.image(url=response.json()["data"]["imgUrl"])

    await get_birthday_map.finish(msg)
