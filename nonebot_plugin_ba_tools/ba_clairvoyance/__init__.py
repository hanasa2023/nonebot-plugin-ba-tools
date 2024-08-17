from bs4 import BeautifulSoup
from nonebot import require

from ..utils.common import get_data_from_html, get_wiki_url_from_title

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import Image  # noqa: E402
from nonebot_plugin_alconna import Match  # noqa: E402
from nonebot_plugin_alconna import Alconna, Args, UniMessage, on_alconna  # noqa: E402

# TODO:命令别名
clairvoyance = Alconna("ba千里眼", Args["server", str])
get_ba_clairvoyance = on_alconna(clairvoyance, use_cmd_start=True)


@get_ba_clairvoyance.assign("server")
async def _(server: Match[str]):
    if server.available:
        if server.result == "国际服":
            url = await get_wiki_url_from_title("国际服千里眼")
            if url:
                text = await get_data_from_html(url)
                soup = BeautifulSoup(text, "html.parser")
                imgs = soup.css.select(".div-img > img")
                src = imgs[3].get("src")
                msg = UniMessage([Image(url=f"https:{src}")])
                await get_ba_clairvoyance.finish(msg)
        elif server.result == "国服":
            url = await get_wiki_url_from_title("国服卡池千里眼")
            if url:
                text = await get_data_from_html(url)
                soup = BeautifulSoup(text, "html.parser")
                imgs = soup.css.select(".preview-image")
                src = imgs[0].get("src")
                msg = UniMessage([Image(url=f"https:{src}")])
                await get_ba_clairvoyance.finish(msg)
        else:
            await get_ba_clairvoyance.finish("不支持的服务器哦～")
