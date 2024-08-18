from nonebot import require

from ..utils.wiki import create_activity_pic, get_wiki_url_from_title

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import Image  # noqa: E402
from nonebot_plugin_alconna import Match  # noqa: E402
from nonebot_plugin_alconna import Alconna, Args, UniMessage, on_alconna  # noqa: E402

activity = Alconna("ba活动一览", Args["server", str])
get_ba_activity_info = on_alconna(activity, use_cmd_start=True)


@get_ba_activity_info.assign("server")
async def _(server: Match[str]):
    if server.available:
        if server.result == "国服":
            url = await get_wiki_url_from_title("国服活动一览")
            if url:
                pic = await create_activity_pic(url, 2022)
                if pic:
                    msg = UniMessage(Image(raw=pic))
                    await get_ba_activity_info.finish(msg)
                else:
                    await get_ba_activity_info.finish("获取图片失败")
        elif server.result == "国际服":
            url = await get_wiki_url_from_title("国际活动一览")
            if url:
                pic = await create_activity_pic(url, 2021 + 1)
                if pic:
                    msg = UniMessage(Image(raw=pic))
                    await get_ba_activity_info.finish(msg)
                else:
                    await get_ba_activity_info.finish("获取图片失败")
        elif server.result == "日服":
            url = await get_wiki_url_from_title("日服活动一览")
            if url:
                pic = await create_activity_pic(url, 2021)
                if pic:
                    msg = UniMessage(Image(raw=pic))
                    await get_ba_activity_info.finish(msg)
                else:
                    await get_ba_activity_info.finish("获取图片失败")
        else:
            await get_ba_activity_info.finish("不支持的服务器哦～")
