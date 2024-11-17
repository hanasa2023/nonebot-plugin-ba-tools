from __future__ import annotations

import random
from typing import Any, Literal

import httpx
from nonebot import logger, require

from ..config import plugin_config
from ..utils.constants import BA_PIC_BASE_URL, BA_PIX_PIC_BASE_URL
from .utils.models import Content, FileInfo, Illust

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import (  # noqa: E402
    Alconna,
    AlconnaMatcher,
    Args,
    Arparma,
    Image,
    Match,
    Option,
    Text,
    UniMessage,
    on_alconna,
)

_pic: Alconna[Any] = Alconna(
    "ba涩图",
    Option("num", Args["v", int]),
    Option("tags", Args["v", list[str]]),
    Option("isAI", Args["v", bool]),
    Option("restrict", Args["v", Literal["safe", "r18"]]),
)
get_pic: type[AlconnaMatcher] = on_alconna(_pic, use_cmd_start=True)

_u_pic: Alconna[Any] = Alconna("ba涩图上传", Args["pid", int])
upload_pic: type[AlconnaMatcher] = on_alconna(_u_pic, use_cmd_start=True)

meme: Alconna[Any] = Alconna("bameme", Option("num", Args["v", int]))
get_meme: type[AlconnaMatcher] = on_alconna(meme, use_cmd_start=True)


@get_pic.handle()
async def _(result: Arparma):
    pic_num: int = result.query("num.v", 1)
    tags: list[str] = result.query("tags.v", [])
    is_ai: bool = result.query("isAI.v", False)
    restrict: str = result.query("restrict.v", "safe")
    if restrict == "r18" and not plugin_config.r18_switch:
        restrict = "safe"
        await get_pic.send("r18涩图已关闭，请联系管理员开启")
    if pic_num > plugin_config.ba_max_pic_num:
        pic_num = plugin_config.ba_max_pic_num
    illust_list: list[Illust] = []
    async with httpx.AsyncClient() as ctx:
        try:
            await get_pic.send("正在获取中，请稍等喵~")
            response: httpx.Response = await ctx.post(
                url=f"{BA_PIX_PIC_BASE_URL}/api/illust/get_illust",
                json={
                    "num": pic_num,
                    "tags": tags,
                    "isAI": is_ai,
                    "restrict": restrict,
                },
            )
            if response.status_code == 200:
                logger.debug(response.json())
                if response.json()["message"] != "success":
                    await get_pic.finish(response.json()["message"])
                illust_list.extend(
                    [Illust(**illust) for illust in response.json()["data"]["illusts"]]
                )
                for illust in illust_list:
                    pic: UniMessage[Image | Text] = UniMessage.image(
                        url=illust.image_url
                    )
                    if plugin_config.send_pic_info:
                        msg = pic + UniMessage.text(
                            f"🎨 pid: {illust.pid}\n🧐 uid: {illust.uid}"
                        )
                    else:
                        msg = pic
                    await get_pic.send(msg)
            else:
                await get_pic.finish("网络出问题了，请稍后再试……")
        except Exception as e:
            await get_pic.finish(str(e))
        finally:
            await get_pic.finish()


@upload_pic.handle()
async def _(pid: Match[int]):
    if pid.available:
        async with httpx.AsyncClient() as ctx:
            try:
                await upload_pic.send("正在上传中，请稍等喵~")
                response: httpx.Response = await ctx.post(
                    url=f"{BA_PIX_PIC_BASE_URL}/api/illust/set_illust",
                    json={
                        "pid": pid.result,
                    },
                )
                if response.status_code == 200:
                    logger.debug(response.json())
                    msg = UniMessage.text(response.json()["message"])
                    await upload_pic.send(msg)
                else:
                    await upload_pic.finish("网络出问题了，请稍后再试……")
            except Exception as e:
                await upload_pic.finish(str(e))
            finally:
                await upload_pic.finish()


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
