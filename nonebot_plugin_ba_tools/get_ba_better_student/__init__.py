from __future__ import annotations

from typing import Any

from nonebot import require

from ..config import ConfigManager
from ..utils.get_img_from_name import get_img

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import (
    Alconna,
    AlconnaMatcher,
    Image,
    UniMessage,
    on_alconna,
)
from nonebot_plugin_alconna.uniseg import Receipt

_better_student: Alconna[Any] = Alconna("ba人权")
get_better_student: type[AlconnaMatcher] = on_alconna(_better_student, use_cmd_start=True)


@get_better_student.handle()
async def _() -> None:
    pre_msg: Receipt | None = None
    msg: UniMessage[Image] | None = await get_img("BA人权", "人权")
    if msg:
        if ConfigManager.get().pic.loading_switch:
            pre_msg = await UniMessage.text("正在努力查询……").send()
        await get_better_student.send(msg)
        if ConfigManager.get().pic.loading_switch and pre_msg:
            await pre_msg.recall()
        await get_better_student.finish()
    else:
        await get_better_student.finish("似乎发生了某些错误")
