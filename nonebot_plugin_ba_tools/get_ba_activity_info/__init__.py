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

activity: Alconna[Any] = Alconna("ba活动一览")
get_activity_info: type[AlconnaMatcher] = on_alconna(activity, use_cmd_start=True)


@get_activity_info.handle()
async def _() -> None:
    pre_msg: Receipt | None = None
    msg: UniMessage[Image] | None = await get_img("BA活动", "活动")
    if msg:
        if ConfigManager.get().pic.loading_switch:
            pre_msg = await UniMessage.text("正在加载图片……").send()
        await get_activity_info.send(msg)
        if ConfigManager.get().pic.loading_switch and pre_msg:
            await pre_msg.recall()
        await get_activity_info.finish()
    else:
        await get_activity_info.finish("不支持的服务器哦～")
