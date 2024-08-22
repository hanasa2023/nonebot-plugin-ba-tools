from typing import Any

from nonebot import require
from nonebot.adapters.onebot.v11 import Bot

from ..config import plugin_config
from ..utils.wiki import create_activity_pic, get_wiki_url_from_title

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import (  # noqa: E402
    Alconna,
    AlconnaMatcher,
    Args,
    Image,  # noqa: E402
    Match,  # noqa: E402
    UniMessage,
    on_alconna,
)

activity: Alconna[Any] = Alconna("ba活动一览", Args["server", str])
get_ba_activity_info: type[AlconnaMatcher] = on_alconna(activity, use_cmd_start=True)


@get_ba_activity_info.assign("server")
async def _(bot: Bot, server: Match[str]) -> None:
    if server.available:
        pre_msg: dict[str, int] = {"message_id": -1}
        if server.result == "国服":
            url = await get_wiki_url_from_title("国服活动一览")
            if url:
                pic = await create_activity_pic(url, 2022)
                if pic:
                    if plugin_config.loading_switch:
                        pre_msg = await get_ba_activity_info.send("正在加载图片……")
                    msg = UniMessage(Image(raw=pic))
                    await get_ba_activity_info.send(msg)
                    if plugin_config.loading_switch:
                        await bot.delete_msg(message_id=pre_msg["message_id"])
                    await get_ba_activity_info.finish()
                else:
                    await get_ba_activity_info.finish("获取图片失败")
        elif server.result == "国际服":
            url = await get_wiki_url_from_title("国际活动一览")
            if url:
                pic = await create_activity_pic(url, 2021 + 1)
                if pic:
                    if plugin_config.loading_switch:
                        pre_msg = await get_ba_activity_info.send("正在加载图片……")
                    msg = UniMessage(Image(raw=pic))
                    await get_ba_activity_info.send(msg)
                    if plugin_config.loading_switch:
                        await bot.delete_msg(message_id=pre_msg["message_id"])
                    await get_ba_activity_info.finish()
                else:
                    await get_ba_activity_info.finish("获取图片失败")
        elif server.result == "日服":
            url = await get_wiki_url_from_title("日服活动一览")
            if url:
                pic = await create_activity_pic(url, 2021)
                if pic:
                    if plugin_config.loading_switch:
                        pre_msg = await get_ba_activity_info.send("正在加载图片……")
                    msg = UniMessage(Image(raw=pic))
                    await get_ba_activity_info.send(msg)
                    if plugin_config.loading_switch:
                        await bot.delete_msg(message_id=pre_msg["message_id"])
                    await get_ba_activity_info.finish()
                else:
                    await get_ba_activity_info.finish("获取图片失败")
        else:
            await get_ba_activity_info.finish("不支持的服务器哦～")
