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

_rank1: Alconna[Any] = Alconna("ba总力战档线", Args["server", str])
get_rank1_charts: type[AlconnaMatcher] = on_alconna(_rank1, use_cmd_start=True)


@get_rank1_charts.assign("server")
async def _(bot: Bot, server: Match[str]):
    if server.available:
        name_and_type: str = ""
        if "官服" in server.result:
            name_and_type = "国服官服总力战档线"
        elif "b服" in server.result or "B服" in server.result:
            name_and_type = "国服B服总力战档线"
        elif "日服" in server.result:
            name_and_type = "日服总力战档线"
        else:
            await get_rank1_charts.finish("未知的服务器")
        pre_msg: dict[str, int] = {"message_id": -1}
        msg: UniMessage[Image] | None = await get_img(name_and_type, name_and_type)
        if msg:
            if plugin_config.loading_switch:
                pre_msg = await get_rank1_charts.send("正在努力查询……")
            await get_rank1_charts.send(msg)
            if plugin_config.loading_switch:
                await bot.delete_msg(message_id=pre_msg["message_id"])
            await get_rank1_charts.finish()
        else:
            await get_rank1_charts.finish("该服务器(暂)不支持查询总力战档线")
