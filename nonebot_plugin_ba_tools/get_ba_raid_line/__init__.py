from __future__ import annotations

from typing import Any

import httpx
from nonebot import logger, require

from ..config import ConfigManager
from ..utils.constants import ARONA_API_URL, ARONA_CDN_URL, BOSS_TRANSLATE

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import (
    Alconna,
    AlconnaMatcher,
    Args,
    Arparma,
    Image,
    Match,
    Text,
    UniMessage,
    on_alconna,
)
from nonebot_plugin_alconna.uniseg import Receipt

_rank1: Alconna[Any] = Alconna("ba总力战档线", Args["server", str])
get_rank1_charts: type[AlconnaMatcher] = on_alconna(_rank1, use_cmd_start=True)

_score_change: Alconna[Any] = Alconna("ba总力战档线变化", Args["server", str])
get_score_charts: type[AlconnaMatcher] = on_alconna(_score_change, use_cmd_start=True)

_member_change: Alconna[Any] = Alconna("ba总力战人数变化", Args["server", str])
get_member_charts: type[AlconnaMatcher] = on_alconna(_member_change, use_cmd_start=True)

_score: Alconna[Any] = Alconna(
    "ba总力战分数计算",
    Args["server", str],
    Args["boss_name", str],
    Args["time", int],
    Args["hard", str],
)
calc_score: type[AlconnaMatcher] = on_alconna(_score, use_cmd_start=True)

_time: Alconna[Any] = Alconna("ba总力战时间计算", Args["server", str], Args["boss_name", str], Args["point", int])
calc_time: type[AlconnaMatcher] = on_alconna(_time, use_cmd_start=True)

_boss: Alconna[Any] = Alconna("ba可用boss")
get_boss_list: type[AlconnaMatcher] = on_alconna(_boss, use_cmd_start=True)


@get_rank1_charts.assign("server")
async def _(server: Match[str]) -> None:
    if server.available:
        server_id: int = 0
        if "官服" in server.result:
            server_id = 1
        elif "b服" in server.result or "B服" in server.result:
            server_id = 2
        elif "日服" in server.result:
            server_id = 3
        else:
            await get_rank1_charts.finish("未知的服务器")
        pre_msg: Receipt | None = None
        msg: UniMessage[Image] | None = None
        async with httpx.AsyncClient() as ctx:
            response: httpx.Response = await ctx.get(f"{ARONA_API_URL}/api/raid/line/{server_id}")
            logger.debug(response.status_code)
            if response.status_code == 200:
                msg = UniMessage.image(url=response.json()["data"]["imgUrl"])
        if msg:
            if ConfigManager.get().pic.loading_switch:
                pre_msg = await UniMessage.text("正在努力查询……").send()
            await get_rank1_charts.send(msg)
            if ConfigManager.get().pic.loading_switch and pre_msg:
                await pre_msg.recall()
            await get_rank1_charts.finish()
        else:
            await get_rank1_charts.finish("该服务器(暂)不支持查询总力战档线")


@get_score_charts.assign("server")
async def _(server: Match[str]) -> None:
    if server.available:
        server_id: int = 0
        if "官服" in server.result:
            server_id = 1
        elif "b服" in server.result or "B服" in server.result:
            server_id = 2
        elif "日服" in server.result:
            server_id = 3
        else:
            await get_score_charts.finish("未知的服务器")
        pre_msg: Receipt | None = None
        msg: UniMessage[Image] | None = None
        async with httpx.AsyncClient() as ctx:
            response: httpx.Response = await ctx.get(f"{ARONA_API_URL}/api/lineChange/{server_id}")
            logger.debug(response.status_code)
            if response.status_code == 200:
                msg = UniMessage.image(url=response.json()["data"]["imgUrl"])
        if msg:
            if ConfigManager.get().pic.loading_switch:
                pre_msg = await UniMessage.text("正在努力查询……").send()
            await get_score_charts.send(msg)
            if ConfigManager.get().pic.loading_switch and pre_msg:
                await pre_msg.recall()
            await get_score_charts.finish()
        else:
            await get_score_charts.finish("该服务器(暂)不支持查询档线变化")


@get_member_charts.assign("server")
async def _(server: Match[str]) -> None:
    if server.available:
        server_id: int = 0
        if "官服" in server.result:
            server_id = 1
        elif "b服" in server.result or "B服" in server.result:
            server_id = 2
        elif "日服" in server.result:
            server_id = 3
        else:
            await get_member_charts.finish("未知的服务器")
        pre_msg: Receipt | None = None
        msg: UniMessage[Image] | None = None
        async with httpx.AsyncClient() as ctx:
            response: httpx.Response = await ctx.get(f"{ARONA_API_URL}/api/raid/memberChange/{server_id}")
            logger.debug(response.status_code)
            if response.status_code == 200:
                msg = UniMessage.image(url=response.json()["data"]["imgUrl"])
        if msg:
            if ConfigManager.get().pic.loading_switch:
                pre_msg = await UniMessage.text("正在努力查询……").send()
            await get_member_charts.send(msg)
            if ConfigManager.get().pic.loading_switch and pre_msg:
                await pre_msg.recall()
            await get_member_charts.finish()
        else:
            await get_member_charts.finish("该服务器(暂)不支持查询总力战人数变化")


@calc_score.handle()
async def _(results: Arparma) -> None:
    server: str = results.query("server", "官服")
    boss_name: str = results.query("boss_name", "")
    time: int = results.query("time", 0)
    hard: str = results.query("hard", "EX")
    server_id: int = 0
    if server == "官服":
        server_id = 1
    elif server == "b服" or server == "B服":
        server_id = 2
    elif server == "日服":
        server_id = 3
    else:
        await get_member_charts.finish("未知的服务器")
    pre_msg: Receipt | None = None
    msg: UniMessage[Text] | None = None
    async with httpx.AsyncClient() as ctx:
        response: httpx.Response = await ctx.get(
            f"{ARONA_API_URL}/api/raid/calculate/score/{server_id}/{BOSS_TRANSLATE[boss_name]}/{time}/{hard}"
        )
        if response.status_code == 200:
            data = response.json()
            msg = UniMessage.text(f"对应的分数为: {data['data']['score']}")
    if msg:
        if ConfigManager.get().pic.loading_switch:
            pre_msg = await UniMessage.text("正在努力查询……").send()
        await get_member_charts.send(msg)
        if ConfigManager.get().pic.loading_switch and pre_msg:
            await pre_msg.recall()
        await get_member_charts.finish()
    else:
        await get_member_charts.finish("该服务器(暂)不支持分数计算")


@calc_time.handle()
async def _(results: Arparma) -> None:
    server: str = results.query("server", "官服")
    boss_name: str = results.query("boss_name", "")
    point: int = results.query("point", 0)
    server_id: int = 0
    if server == "官服":
        server_id = 1
    elif server == "b服" or server == "B服":
        server_id = 2
    elif server == "日服":
        server_id = 3
    else:
        await get_member_charts.finish("未知的服务器")
    pre_msg: Receipt | None = None
    msg: UniMessage[Text] | None = None
    async with httpx.AsyncClient() as ctx:
        response: httpx.Response = await ctx.get(
            f"{ARONA_API_URL}/api/raid/calculate/point/{server_id}/{BOSS_TRANSLATE[boss_name]}/{point}"
        )
        if response.status_code == 200:
            data = response.json()
            msg = UniMessage.text(f"对应的时间为: {data['data']['time']}")
    if msg:
        if ConfigManager.get().pic.loading_switch:
            pre_msg = await UniMessage.text("正在努力查询……").send()
        await get_member_charts.send(msg)
        if ConfigManager.get().pic.loading_switch and pre_msg:
            await pre_msg.recall()
        await get_member_charts.finish()
    else:
        await get_member_charts.finish("该服务器(暂)不支持时间计算")


@get_boss_list.handle()
async def _() -> None:
    async with httpx.AsyncClient() as ctx:
        response: httpx.Response = await ctx.get(f"{ARONA_CDN_URL}/data/available-list.json")
        if response.status_code == 200:
            walkthroughs: list[str] = response.json()["boss"]
            msg = "可用的攻略有：\n"
            for name in walkthroughs:
                msg += f"- {name}\n"

            await get_boss_list.finish(msg)
    await get_boss_list.finish("获取出错了")
