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

# TODO: 添加命令别名
walkthrough: Alconna[Any] = Alconna("ba攻略", Args["option", str])
get_walkthrough: type[AlconnaMatcher] = on_alconna(walkthrough, use_cmd_start=True)


@get_walkthrough.assign("option")
async def _(bot: Bot, option: Match[str]) -> None:
    if option.available:
        pre_msg: dict[str, int] = {"message_id": -1}
        type = "关卡攻略" if option.result.startswith("关卡") else option.result
        msg: UniMessage[Image] | None = await get_img(
            option.result.replace("关卡", ""), type
        )
        if msg:
            if plugin_config.loading_switch:
                pre_msg = await get_walkthrough.send("攻略正在来的路上……")
            await get_walkthrough.send(msg)
            if plugin_config.loading_switch:
                await bot.delete_msg(message_id=pre_msg["message_id"])
            await get_walkthrough.finish()
        else:
            await get_walkthrough.finish(f"未找到对应{option.result}的攻略哦～")
