from typing import Any

from bs4 import BeautifulSoup
from nonebot import require
from nonebot.adapters.onebot.v11 import Bot

from ..config import plugin_config
from ..utils.wiki import get_data_from_html, get_wiki_url_from_title
from .utils.get_clairvoyance_img import (
    create_clairvoyance_img,
)

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
        if server.result == "国际服":
            url = await get_wiki_url_from_title("国际服千里眼")
            if url:
                if plugin_config.loading_switch:
                    pre_msg = await get_ba_clairvoyance.send("拼命加载图片中……")
                msg = await create_clairvoyance_img(url)
                await get_ba_clairvoyance.send(msg)
                if plugin_config.loading_switch:
                    await bot.delete_msg(message_id=pre_msg["message_id"])
                await get_ba_clairvoyance.finish()
        elif server.result == "国服":
            url = await get_wiki_url_from_title("国服卡池千里眼")
            if url:
                if plugin_config.loading_switch:
                    pre_msg = await get_ba_clairvoyance.send("拼命加载图片中……")
                text = await get_data_from_html(url)
                soup = BeautifulSoup(text, "html.parser")
                imgs = soup.select(".preview-image")
                src = imgs[0].get("src")
                msg = UniMessage([Image(url=f"https:{src}")])
                await get_ba_clairvoyance.send(msg)
                if plugin_config.loading_switch:
                    await bot.delete_msg(message_id=pre_msg["message_id"])
                await get_ba_clairvoyance.finish()
        else:
            await get_ba_clairvoyance.finish("不支持的服务器哦～")
