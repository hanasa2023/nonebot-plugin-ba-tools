from nonebot import require

from ..utils.wiki import get_walkthrough_img, get_wiki_url_from_title

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import Image  # noqa: E402
from nonebot_plugin_alconna import Match  # noqa: E402
from nonebot_plugin_alconna import Alconna, Args, UniMessage, on_alconna  # noqa: E402

# TODO: 添加命令别名
walkthrough = Alconna("ba关卡攻略", Args["index", str])
get_walkthrough = on_alconna(walkthrough, use_cmd_start=True)


@get_walkthrough.assign("index")
async def _(index: Match[str]):
    if index.available:
        url: str | None = await get_wiki_url_from_title(index.result)
        if url:
            imgs_url: list[str] = await get_walkthrough_img(url)
            if len(imgs_url):
                msg: UniMessage[Image] = UniMessage()
                for img_url in imgs_url:
                    msg.append(Image(url=img_url))
                await get_walkthrough.finish(msg)
            else:
                await get_walkthrough.finish("获取攻略失败惹🥺")
        else:
            await get_walkthrough.finish("未找到对应关卡攻略哦～")
