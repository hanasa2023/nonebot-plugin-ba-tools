import json
from pathlib import Path
from typing import Any

from arclet.alconna import Alconna
from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot_plugin_alconna import AlconnaMatcher, Args, Match, on_alconna

from ..config import DRIVER, plugin_config
from ..utils.constants import BIRTHDAY_INFO_GROUP_LIST_FILE
from ..utils.user_info import (
    get_group_user_info,
    is_group_admin,
    is_group_owner,
    is_superuser,
)

GROUP_LIST: list[int] = []


def save_group_list() -> None:
    full_path: Path = plugin_config.setting_path / BIRTHDAY_INFO_GROUP_LIST_FILE
    if not plugin_config.setting_path.exists():
        plugin_config.setting_path.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(GROUP_LIST, f, ensure_ascii=False, indent=4)


@DRIVER.on_startup
async def _() -> None:
    logger.debug("读取生日信息推送群列表")
    global GROUP_LIST
    full_path: Path = plugin_config.setting_path / BIRTHDAY_INFO_GROUP_LIST_FILE
    if not full_path.exists():
        if not plugin_config.setting_path.exists():
            plugin_config.setting_path.mkdir(parents=True, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write("[]")
        return
    with open(full_path, "r", encoding="utf-8") as f:
        GROUP_LIST = json.load(f)
        logger.debug(f"group list is: {GROUP_LIST}")


# TODO: 添加命令别名
birthday_info: Alconna[Any] = Alconna("ba学生生日订阅", Args["status", str])
birthday_info_switch: type[AlconnaMatcher] = on_alconna(
    birthday_info, use_cmd_start=True
)


@birthday_info_switch.assign("status")
async def _(bot: Bot, event: GroupMessageEvent, status: Match[str]) -> None:
    global GROUP_LIST
    # 群主、管理员、SUPERUSER可以使用此命令
    user_info = await get_group_user_info(bot, event.user_id, event.group_id)
    if (
        is_group_owner(user_info)
        or is_group_admin(user_info)
        or is_superuser(event.user_id)
    ):
        if status.available:
            if status.result == "开启":
                if event.group_id not in GROUP_LIST:
                    GROUP_LIST.append(event.group_id)
                    save_group_list()
                    await birthday_info_switch.finish("已开启生日信息推送")
                else:
                    await birthday_info_switch.finish("已开启生日信息推送")
            elif status.result == "关闭":
                if event.group_id in GROUP_LIST:
                    GROUP_LIST.remove(event.group_id)
                    save_group_list()
                    await birthday_info_switch.finish("已关闭生日信息推送")
                else:
                    await birthday_info_switch.finish("已关闭生日信息推送")
            else:
                await birthday_info_switch.finish("无效的指令")
    else:
        await birthday_info_switch.finish("权限不足")
