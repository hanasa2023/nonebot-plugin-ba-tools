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
    AlconnaMatcher,
    Args,
    Arparma,
    Option,
    UniMessage,
    on_alconna,
)

pic: Alconna[Any] = Alconna("ba涩图", Option("num", Args["v", int]))
get_pic: type[AlconnaMatcher] = on_alconna(pic, use_cmd_start=True)

meme: Alconna[Any] = Alconna("bameme", Option("num", Args["v", int]))
get_meme: type[AlconnaMatcher] = on_alconna(meme, use_cmd_start=True)


@get_pic.handle()
async def _(result: Arparma):
    pic_num: int = result.query("num.v", 1)
    if pic_num > plugin_config.ba_max_pic_num:
        pic_num = plugin_config.ba_max_pic_num
    pic_list: list[FileInfo] = []
    async with httpx.AsyncClient() as ctx:
        try:
            headers: httpx.Headers = httpx.Headers({"Host": "cloudisk.hanasaki.tech"})
            r_ph: httpx.Response = await ctx.post(
                f"{BA_PIC_BASE_URL}/api/fs/list",
                json={"path": "/aliyun-oss/BAArts/phone", "password": ""},
                headers=headers,
            )
            if r_ph.status_code == 200:
                for c in r_ph.json()["data"]["content"]:
                    f_ph: Content = Content(**c)
                    pic_list.append(FileInfo(name=f"phone/{f_ph.name}", sign=f_ph.sign))

            r_p: httpx.Response = await ctx.post(
                f"{BA_PIC_BASE_URL}/api/fs/list",
                json={"path": "/aliyun-oss/BAArts/pc", "password": ""},
                headers=headers,
            )
            if r_p.status_code == 200:
                for c_p in r_p.json()["data"]["content"]:
                    f: Content = Content(**c_p)
                    pic_list.append(FileInfo(name=f"pc/{f.name}", sign=f.sign))
            if len(pic_list) == 0:
                await get_pic.finish("网络出问题了，请稍后再试……")
            random.shuffle(pic_list)
            await get_pic.send("正在获取中，请稍等喵~")
            _max_send = len(pic_list) if len(pic_list) < pic_num else pic_num
            for i in range(_max_send):
                pic = UniMessage.image(
                    url=f"{BA_PIC_BASE_URL}/d/aliyun-oss/BAArts/{pic_list[i].name}?sign={pic_list[i].sign}"
                )
                await get_pic.send(pic)
        except Exception as e:
            logger.error(e)
        finally:
            await get_pic.finish()


@get_meme.handle()
async def _(result: Arparma):
    meme_num: int = result.query("num.v", 1)
    if meme_num > plugin_config.ba_max_pic_num:
        meme_num = plugin_config.ba_max_pic_num
    meme_list: list[FileInfo] = []
    async with httpx.AsyncClient() as ctx:
        try:
            headers: httpx.Headers = httpx.Headers({"Host": "cloudisk.hanasaki.tech"})
            r: httpx.Response = await ctx.post(
                f"{BA_PIC_BASE_URL}/api/fs/list",
                json={"path": "/aliyun-oss/BAArts/emoji&meme", "password": ""},
                headers=headers,
            )
            if r.status_code == 200:
                for c in r.json()["data"]["content"]:
                    con: Content = Content(**c)
                    meme_list.append(FileInfo(name=con.name, sign=con.sign))
            if len(meme_list) == 0:
                await get_pic.finish("网络出问题了，请稍后再试……")
            random.shuffle(meme_list)
            await get_pic.send("正在获取中，请稍等喵~")
            _max_send = len(meme_list) if len(meme_list) < meme_num else meme_num
            for i in range(_max_send):
                _meme_url = UniMessage.image(
                    url=f"{BA_PIC_BASE_URL}/d/aliyun-oss/BAArts/emoji&meme/{meme_list[i].name}?sign={meme_list[i].sign}"
                )
                await get_meme.send(_meme_url)
        except Exception as e:
            logger.error(e)
        finally:
            await get_meme.finish()
