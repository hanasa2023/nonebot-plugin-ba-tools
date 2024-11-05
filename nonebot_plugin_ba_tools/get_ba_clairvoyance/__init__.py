from typing import Any

from nonebot import require
from nonebot.adapters.onebot.v11 import Bot

from ..config import plugin_config
from .utils.get_clairvoyance_img import get_img

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

# TODO:命令别名
clairvoyance: Alconna[Any] = Alconna("ba千里眼", Args["server", str])
get_ba_clairvoyance: type[AlconnaMatcher] = on_alconna(clairvoyance, use_cmd_start=True)


@get_ba_clairvoyance.assign("server")
async def _(bot: Bot, server: Match[str]) -> None:
    if server.available:
        pre_msg: dict[str, int] = {"message_id": -1}
        msg: UniMessage[Image] | None = await get_img(server.result)
        if msg:
            if plugin_config.loading_switch:
                pre_msg = await get_ba_clairvoyance.send("拼命加载图片中……")
            await get_ba_clairvoyance.send(msg)
            if plugin_config.loading_switch:
                await bot.delete_msg(message_id=pre_msg["message_id"])
            await get_ba_clairvoyance.finish()
        else:
            await get_ba_clairvoyance.finish("不支持的服务器哦～")
