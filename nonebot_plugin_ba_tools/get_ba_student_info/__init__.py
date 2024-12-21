from typing import Any

import httpx
from nonebot import require

from ..utils.constants import STUDENT_TRANSLATE

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import (  # noqa: E402
    Alconna,
    AlconnaMatcher,
    Args,
    Arparma,
    UniMessage,
    on_alconna,
)

_student_info: Alconna[Any] = Alconna(
    "ba学生信息", Args["name", str], Args["level?", int]
)
_get_student_info: type[AlconnaMatcher] = on_alconna(_student_info, use_cmd_start=True)

_skill_info: Alconna[Any] = Alconna("ba学生技能", Args["name", str])
_get_skill_info: type[AlconnaMatcher] = on_alconna(_skill_info, use_cmd_start=True)


@_get_student_info.handle()
async def _(result: Arparma) -> None:
    student_name: str = result.query("name", "")
    level: int = result.query("level", 1)
    if student_name == "":
        await _get_student_info.finish("请输入要查询的学生姓名")

    if not STUDENT_TRANSLATE.get(student_name):
        await _get_student_info.finish(f"学生'{student_name}'不存在，或别名不存在。")

    url: str = f"https://arona.hanasaki.tech/api/student/info/{STUDENT_TRANSLATE[student_name]}/{level}"

    try:
        async with httpx.AsyncClient() as ctx:
            response: httpx.Response = await ctx.get(url)
            if response.status_code == 200:
                data = response.json()["data"]
                img = UniMessage.image(url=data["imgUrl"])
                await _get_student_info.send(img)

            else:
                await _get_student_info.send(response.json()["message"])
    except httpx.ReadTimeout:
        await _get_student_info.send(
            "获取超时（请求的信息很可能是第一次生成），请稍后重试……"
        )

    finally:
        await _get_student_info.finish()


@_get_skill_info.handle()
async def _(result: Arparma) -> None:
    student_name: str = result.query("name", "")

    if student_name == "":
        await _get_skill_info.finish("请输入要查询的学生姓名")

    if not STUDENT_TRANSLATE.get(student_name):
        await _get_skill_info.finish(f"学生'{student_name}'不存在，或别名不存在。")

    url: str = f"https://arona.hanasaki.tech/api/student/skills/{STUDENT_TRANSLATE[student_name]}"

    try:
        async with httpx.AsyncClient() as ctx:
            response: httpx.Response = await ctx.get(url)
            if response.status_code == 200:
                data = response.json()["data"]
                img = UniMessage.image(url=data["imgUrl"])
                await _get_skill_info.send(img)

            else:
                await _get_skill_info.send(response.json()["message"])
    except httpx.ReadTimeout:
        await _get_skill_info.send(
            "获取超时（请求的信息很可能是第一次生成），请稍后重试……"
        )

    finally:
        await _get_skill_info.finish()
