import random
from typing import Any

from nonebot import require
from nonebot.adapters.onebot.v11 import Bot

from ..config import plugin_config
from ..utils.wiki import get_img_from_url, get_max_manga_index, get_wiki_urls_from_title

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

manga: Alconna[Any] = Alconna("ba漫画", Args["index", str])
get_manga: type[AlconnaMatcher] = on_alconna(manga, use_cmd_start=True)


@get_manga.assign("index")
async def _(bot: Bot, index: Match) -> None:
    if index.available:
        pre_msg: dict[str, int] = {"message_id": -1}
        max_index: int = (await get_max_manga_index()) - 1
        random_index: int = random.randint(0, max_index)
        title: str = f"第{random_index}话" if index.result == "抽取" else index.result
        urls: list[str] = await get_wiki_urls_from_title(title)
        if len(urls):
            url: str = urls[0]
            imgs_url: list[str] = await get_img_from_url(url)
            if len(imgs_url):
                if plugin_config.loading_switch:
                    pre_msg = await get_manga.send("请稍等喵~")
                msg: UniMessage[Image] = UniMessage()
                for img_url in imgs_url:
                    msg.append(Image(url=img_url))
                await get_manga.send(msg)
                if plugin_config.loading_switch:
                    await bot.delete_msg(message_id=pre_msg["message_id"])
                await get_manga.finish()
            else:
                await get_manga.finish("加载漫画出错了🥺")
        else:
            await get_manga.finish("是找不到的话数呢～")
