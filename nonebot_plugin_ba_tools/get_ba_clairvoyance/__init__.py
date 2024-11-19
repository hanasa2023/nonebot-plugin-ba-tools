from __future__ import annotations

from typing import Any

from nonebot import require

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
from nonebot_plugin_alconna.uniseg import Receipt  # noqa: E402

# TODO:命令别名
clairvoyance: Alconna[Any] = Alconna("ba千里眼", Args["server", str])
get_clairvoyance: type[AlconnaMatcher] = on_alconna(clairvoyance, use_cmd_start=True)


@get_clairvoyance.assign("server")
async def _(server: Match[str]) -> None:
    if server.available:
        pre_msg: Receipt | None = None
        msg: UniMessage[Image] | None = await get_img(
            f"{server.result}未来视", "千里眼"
        )
        if msg:
            if plugin_config.loading_switch:
                pre_msg = await UniMessage.text("拼命加载图片中……").send()
            await get_clairvoyance.send(msg)
            if plugin_config.loading_switch and pre_msg:
                await pre_msg.recall()
            await get_clairvoyance.finish()
        else:
            await get_clairvoyance.finish("不支持的服务器哦～")
