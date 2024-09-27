import random
from typing import Any

import httpx
from nonebot import logger, require

from ..config import plugin_config
from ..utils.constants import BA_PIC_BASE_URL
from .utils.models import Content, FileInfo

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import (  # noqa: E402
    Alconna,
    AlconnaMatch,
    AlconnaMatcher,
    Args,
    Image,
    Match,
    Option,
    UniMessage,
    on_alconna,
)

pic: Alconna[Any] = Alconna("ba涩图", Option("num", Args["num", int]))
get_pic: type[AlconnaMatcher] = on_alconna(pic, use_cmd_start=True)


@get_pic.handle()
async def _(num: Match[int] = AlconnaMatch("num")):
    pic_num: int = 1
    if num.available:
        pic_num = num.result
    if pic_num > plugin_config.ba_max_pic_num:
        pic_num = plugin_config.ba_max_pic_num
    pic_list: list[FileInfo] = []
    async with httpx.AsyncClient() as ctx:
        try:
            r_ph: httpx.Response = await ctx.post(
                f"{BA_PIC_BASE_URL}/api/fs/list",
                json={"path": "/BaiduNetdisk/BAArts/phone", "password": ""},
            )
            if r_ph.status_code == 200:
                for c in r_ph.json()["data"]["content"]:
                    f_ph: Content = Content(**c)
                    pic_list.append(FileInfo(name=f"phone/{f_ph.name}", sign=f_ph.sign))

            r_p: httpx.Response = await ctx.post(
                f"{BA_PIC_BASE_URL}/api/fs/list",
                json={"path": "/BaiduNetdisk/BAArts/pc", "password": ""},
            )
            if r_p.status_code == 200:
                for c_p in r_p.json()["data"]["content"]:
                    f: Content = Content(**c_p)
                    pic_list.append(FileInfo(name=f"pc/{f.name}", sign=f.sign))
            random.shuffle(pic_list)
            await get_pic.send("正在获取中，请稍等喵~")
            for i in range(pic_num):
                pic: httpx.Response = await ctx.get(
                    f"{BA_PIC_BASE_URL}/d/BaiduNetdisk/BAArts/{pic_list[i].name}?sign={pic_list[i].sign}"
                )
                if pic.status_code == 200:
                    pic_data: UniMessage[Image] = UniMessage().image(raw=pic.content)
                    await get_pic.send(pic_data)
        except Exception as e:
            logger.error(e)
        finally:
            await get_pic.finish()


meme: Alconna[Any] = Alconna("bameme", Option("num", Args["num", int]))
get_meme: type[AlconnaMatcher] = on_alconna(meme, use_cmd_start=True)


@get_meme.handle()
async def _(num: Match[int] = AlconnaMatch("num")):
    meme_num: int = 1
    if num.available:
        meme_num = num.result
    if meme_num > plugin_config.ba_max_pic_num:
        meme_num = plugin_config.ba_max_pic_num
    meme_list: list[FileInfo] = []
    async with httpx.AsyncClient() as ctx:
        try:
            r: httpx.Response = await ctx.post(
                f"{BA_PIC_BASE_URL}/api/fs/list",
                json={"path": "/BaiduNetdisk/BAArts/emoji & meme", "password": ""},
            )
            if r.status_code == 200:
                for c in r.json()["data"]["content"]:
                    con: Content = Content(**c)
                    meme_list.append(FileInfo(name=f"meme/{con.name}", sign=con.sign))
            random.shuffle(meme_list)
            await get_pic.send("正在获取中，请稍等喵~")
            for i in range(meme_num):
                _meme: httpx.Response = await ctx.get(
                    f"{BA_PIC_BASE_URL}/d/BaiduNetdisk/BAArts/{meme_list[i].name}?sign={meme_list[i].sign}"
                )
                _meme_raw: UniMessage[Image] = UniMessage().image(raw=_meme.content)
                await get_meme.send(_meme_raw)
        except Exception as e:
            logger.error(e)
        finally:
            await get_meme.finish()
