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
    Image,
    Match,
    UniMessage,
    on_alconna,
)

_simple_appraise: Alconna[Any] = Alconna("ba角色简评", Args["server", str])
get_simple_appraise: type[AlconnaMatcher] = on_alconna(
    _simple_appraise, use_cmd_start=True
)


@get_simple_appraise.assign("server")
async def _(bot: Bot, server: Match[str]):
    if server.available:
        pre_msg: dict[str, int] = {"message_id": -1}
        msg: UniMessage[Image] | None = await get_img(
            f"{server.result}角色简评", f"{server.result}角色简评"
        )
        if msg:
            if plugin_config.loading_switch:
                pre_msg = await get_simple_appraise.send("正在努力查询……")
            await get_simple_appraise.send(msg)
            if plugin_config.loading_switch:
                await bot.delete_msg(message_id=pre_msg["message_id"])
            await get_simple_appraise.finish()
        else:
            await get_simple_appraise.finish("该服务器不支持查询角色简评")
