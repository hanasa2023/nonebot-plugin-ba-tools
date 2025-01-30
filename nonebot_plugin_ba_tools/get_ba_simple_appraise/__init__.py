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

_simple_appraise: Alconna[Any] = Alconna("ba角色简评")
get_simple_appraise: type[AlconnaMatcher] = on_alconna(_simple_appraise, use_cmd_start=True)


@get_simple_appraise.handle()
async def _() -> None:
    pre_msg: Receipt | None = None
    msg: UniMessage[Image] | None = await get_img("BA角评", "角色简评")
    if msg:
        if ConfigManager.get().pic.loading_switch:
            pre_msg = await UniMessage.text("正在努力查询……").send()
        await get_simple_appraise.send(msg)
        if ConfigManager.get().pic.loading_switch and pre_msg:
            await pre_msg.recall()
        await get_simple_appraise.finish()
    else:
        await get_simple_appraise.finish("出错了喵~")
