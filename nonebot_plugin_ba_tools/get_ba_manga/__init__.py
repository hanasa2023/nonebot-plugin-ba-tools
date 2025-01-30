from __future__ import annotations

import random
from typing import Any

from nonebot import require

from ..config import ConfigManager
from ..utils.wiki import get_img_from_url, get_max_manga_index, get_wiki_urls_from_title

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

manga: Alconna[Any] = Alconna("ba漫画", Args["index", str])
get_manga: type[AlconnaMatcher] = on_alconna(manga, use_cmd_start=True)


@get_manga.assign("index")
async def _(index: Match) -> None:
    if index.available:
        pre_msg: Receipt | None = None
        max_index: int = (await get_max_manga_index()) - 1
        random_index: int = random.randint(0, max_index)
        title: str = f"第{random_index}话" if index.result == "抽取" else index.result
        urls: list[str] = await get_wiki_urls_from_title(title)
        if len(urls):
            url: str = urls[0]
            imgs_url: list[str] = await get_img_from_url(url)
            if len(imgs_url):
                if ConfigManager.get().pic.loading_switch:
                    pre_msg = await UniMessage.text("请稍等喵~").send()
                msg: UniMessage[Image] = UniMessage()
                for img_url in imgs_url:
                    msg.append(Image(url=img_url))
                await get_manga.send(msg)
                if ConfigManager.get().pic.loading_switch and pre_msg:
                    await pre_msg.recall()
                await get_manga.finish()
            else:
                await get_manga.finish("加载漫画出错了🥺")
        else:
            await get_manga.finish("是找不到的话数呢～")
