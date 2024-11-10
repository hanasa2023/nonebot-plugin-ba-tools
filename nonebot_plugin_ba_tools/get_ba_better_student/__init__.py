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

_better_student: Alconna[Any] = Alconna("ba人权", Args["server", str])
get_better_student: type[AlconnaMatcher] = on_alconna(
    _better_student, use_cmd_start=True
)


@get_better_student.assign("server")
async def _(bot: Bot, server: Match[str]):
    if server.available:
        pre_msg: dict[str, int] = {"message_id": -1}
        msg: UniMessage[Image] | None = await get_img(
            f"{server.result}人权", f"{server.result}人权"
        )
        if msg:
            if plugin_config.loading_switch:
                pre_msg = await get_better_student.send("正在努力查询……")
            await get_better_student.send(msg)
            if plugin_config.loading_switch:
                await bot.delete_msg(message_id=pre_msg["message_id"])
            await get_better_student.finish()
        else:
            await get_better_student.finish("该服务器不支持查询人权")
