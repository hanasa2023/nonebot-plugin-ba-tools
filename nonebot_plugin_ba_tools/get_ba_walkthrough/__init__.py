from __future__ import annotations

from typing import Any

import httpx
from nonebot import require

from ..config import ConfigManager
from ..utils.constants import ARONA_CDN_URL
from ..utils.get_img_from_name import get_img

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import (
    Alconna,
    AlconnaMatcher,
    Args,
    Image,
    Match,
    UniMessage,
    on_alconna,
)
from nonebot_plugin_alconna.uniseg import Receipt

walkthrough: Alconna[Any] = Alconna("ba攻略", Args["option", str])
get_walkthrough: type[AlconnaMatcher] = on_alconna(walkthrough, use_cmd_start=True)

walkthrough_list: Alconna[Any] = Alconna("ba可用攻略")
get_walkthrough_list: type[AlconnaMatcher] = on_alconna(walkthrough_list, use_cmd_start=True)


@get_walkthrough.assign("option")
async def _(option: Match[str]) -> None:
    if option.available:
        pre_msg: Receipt | None = None
        type: str = "关卡攻略" if option.result.startswith("关卡") else option.result
        middle_route: str = "chapter-map" if option.result.startswith("关卡") else "strategy"
        msg: UniMessage[Image] | None = await get_img(option.result.replace("关卡", ""), type, middle_route)
        if msg:
            if ConfigManager.get().pic.loading_switch:
                pre_msg = await UniMessage.text("攻略正在来的路上……").send()
            await get_walkthrough.send(msg)
            if ConfigManager.get().pic.loading_switch and pre_msg:
                await pre_msg.recall()
            await get_walkthrough.finish()
        else:
            await get_walkthrough.finish(f"未找到对应{option.result}的攻略哦～")


@get_walkthrough_list.handle()
async def _() -> None:
    async with httpx.AsyncClient() as ctx:
        response: httpx.Response = await ctx.get(f"{ARONA_CDN_URL}/data/available-list.json")
        if response.status_code == 200:
            walkthroughs: list[str] = response.json()["walkthrough"]
            msg = "可用的攻略有：\n"
            for name in walkthroughs:
                msg += f"- {name}\n"

            await get_walkthrough_list.finish(msg)
    await get_walkthrough_list.finish("获取出错了")
