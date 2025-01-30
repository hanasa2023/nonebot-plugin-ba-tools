from __future__ import annotations

import random
from typing import Any, Literal

import httpx
from nonebot import logger, require

from ..config import ConfigManager
from ..utils.constants import ARONA_API_URL
from .models import Illust, MemeInfo

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import (
    Alconna,
    AlconnaMatcher,
    Args,
    Arparma,
    CustomNode,
    Image,
    Match,
    MsgTarget,
    Option,
    Reference,
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

meme: Alconna[Any] = Alconna("bameme", Args["num?", int])
get_meme: type[AlconnaMatcher] = on_alconna(meme, use_cmd_start=True)


@get_pic.handle()
async def _(result: Arparma, target: MsgTarget):
    pic_num: int = result.query("num.v", 1)
    tags: list[str] = result.query("tags.v", [])
    is_ai: bool = result.query("isAI.v", False)
    restrict: str = result.query("restrict.v", "safe")
    if restrict == "r18" and not ConfigManager.get().pic.r18_switch:
        restrict = "safe"
        await get_pic.send("r18涩图已关闭，请联系管理员开启")
    if pic_num > ConfigManager.get().pic.max_pic_num:
        pic_num = ConfigManager.get().pic.max_pic_num
    illust_list: list[Illust] = []
    async with httpx.AsyncClient() as ctx:
        try:
            await get_pic.send("正在获取中，请稍等喵~")
            response: httpx.Response = await ctx.post(
                url=f"{ARONA_API_URL}/api/illusts/getIllusts",
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
                illust_list.extend([Illust(**illust) for illust in response.json()["data"]["illusts"]])
                for illust in illust_list:
                    pic: UniMessage[Image | Text] = UniMessage.image(url=illust.image_url)
                    if ConfigManager.get().pic.send_pic_info:
                        m = pic + UniMessage.text(
                            f"""
                            🎨 pid: {illust.pid}
                            🧐 uid: {illust.uid}
                            🥰 like:{illust.love_members}
                            😨 dislike: {illust.hate_memebers}
                            """
                        )
                    else:
                        m = pic
                    if ConfigManager.get().pic.max_pic_num >= 10:
                        nodes = [CustomNode(uid=str(target.self_id), name="", content=m)]
                        msg: Reference | UniMessage[Any] = Reference(nodes=nodes)
                    else:
                        msg = m
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
                    url=f"{ARONA_API_URL}/api/illusts/setIllusts",
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
    meme_num: int = result.query("num", 1)
    if meme_num > ConfigManager.get().pic.max_pic_num:
        meme_num = ConfigManager.get().pic.max_pic_num
    async with httpx.AsyncClient() as ctx:
        try:
            r: httpx.Response = await ctx.get(f"{ARONA_API_URL}/api/meme")
            if r.status_code == 200:
                data: list[MemeInfo] = r.json()["data"]
                random.shuffle(data)
                await get_pic.send("正在获取中，请稍等喵~")
                _max_send = len(data) if len(data) < meme_num else meme_num
                for i in range(_max_send):
                    _meme = UniMessage.image(url=f"{data[i].url}")
                    await get_meme.send(_meme)
            else:
                await get_pic.finish("网络出问题了，请稍后再试……")
        except Exception as e:
            logger.error(e)
        finally:
            await get_meme.finish()
