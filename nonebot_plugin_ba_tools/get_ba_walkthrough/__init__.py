from nonebot import require
from nonebot.adapters.onebot.v11.bot import Bot

from ..config import plugin_config
from ..utils.wiki import get_img_from_url, get_wiki_url_from_title

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import Image  # noqa: E402
from nonebot_plugin_alconna import Match  # noqa: E402
from nonebot_plugin_alconna import Alconna, Args, UniMessage, on_alconna  # noqa: E402

# TODO: 添加命令别名
walkthrough = Alconna("ba关卡攻略", Args["index", str])
get_walkthrough = on_alconna(walkthrough, use_cmd_start=True)


@get_walkthrough.assign("index")
async def _(bot: Bot, index: Match[str]):
    if index.available:
        pre_msg: dict[str, int] = {"message_id": -1}
        url: str | None = await get_wiki_url_from_title(index.result)
        if url:
            imgs_url: list[str] = await get_img_from_url(url)
            if len(imgs_url):
                if plugin_config.is_open_notice:
                    pre_msg = await get_walkthrough.send("总之你先别急!")
                msg: UniMessage[Image] = UniMessage()
                for img_url in imgs_url:
                    msg.append(Image(url=img_url))
                await get_walkthrough.send(msg)
                if plugin_config.is_open_notice:
                    await bot.delete_msg(message_id=pre_msg["message_id"])
                await get_walkthrough.finish()
            else:
                await get_walkthrough.finish("获取攻略失败惹🥺")
        else:
            await get_walkthrough.finish("未找到对应关卡攻略哦~")
