from __future__ import annotations

from typing import Any

from nonebot import require
from nonebot.adapters.onebot.v11 import Bot

from ..config import plugin_config
from ..utils.get_img_from_name import get_img

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import (  # noqa: E402
    Alconna,
    AlconnaMatcher,
    Args,
    Image,  # noqa: E402
    Match,  # noqa: E402
    UniMessage,
    on_alconna,
)

activity: Alconna[Any] = Alconna("ba活动一览", Args["server", str])
get_activity_info: type[AlconnaMatcher] = on_alconna(activity, use_cmd_start=True)


@get_activity_info.assign("server")
async def _(bot: Bot, server: Match[str]) -> None:
    if server.available:
        pre_msg: dict[str, int] = {"message_id": -1}
        msg: UniMessage[Image] | None = await get_img(f"{server.result}活动", "活动")
        if msg:
            if plugin_config.loading_switch:
                pre_msg = await get_activity_info.send("正在加载图片……")
            await get_activity_info.send(msg)
            if plugin_config.loading_switch:
                await bot.delete_msg(message_id=pre_msg["message_id"])
            await get_activity_info.finish()
        else:
            await get_activity_info.finish("不支持的服务器哦～")
