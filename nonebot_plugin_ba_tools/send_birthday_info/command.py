import json
from pathlib import Path
from typing import Any

# from arclet.alconna import Alconna
from nonebot import get_driver, logger, require

from ..config import SETTING_DIR, ConfigManager
from ..utils.constants import BIRTHDAY_INFO_GROUP_LIST_FILE
from ..utils.user_info import is_superuser

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import (
    Alconna,
    AlconnaMatcher,
    Args,
    Match,
    on_alconna,
)

require("nonebot_plugin_uninfo")
from nonebot_plugin_uninfo import SceneType, Uninfo

GROUP_LIST: list[int] = []


def save_group_list() -> None:
    full_path: Path = SETTING_DIR / BIRTHDAY_INFO_GROUP_LIST_FILE
    if not SETTING_DIR.exists():
        SETTING_DIR.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(GROUP_LIST, f, ensure_ascii=False, indent=4)


@get_driver().on_startup
async def _() -> None:
    logger.debug("读取生日信息推送群列表")
    global GROUP_LIST
    full_path: Path = SETTING_DIR / BIRTHDAY_INFO_GROUP_LIST_FILE
    if not full_path.exists():
        if not SETTING_DIR.exists():
            SETTING_DIR.mkdir(parents=True, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write("[]")
        return
    with open(full_path, encoding="utf-8") as f:
        GROUP_LIST = json.load(f)
        logger.debug(f"group list is: {GROUP_LIST}")


# TODO: 添加命令别名
birthday_info: Alconna[Any] = Alconna("ba学生生日订阅", Args["status", str])
birthday_info_switch: type[AlconnaMatcher] = on_alconna(birthday_info, use_cmd_start=True)


@birthday_info_switch.assign("status")
async def _(status: Match[str], session: Uninfo) -> None:
    global GROUP_LIST
    if session.scene.type == SceneType.GROUP:
        logger.info(f"session: {session.scene.id}")
        is_group_owner = session.member and session.member.role and session.member.role.id == "OWNER"
        is_group_admin = session.member and session.member.role and session.member.role.id == "ADMINISTRATOR"
        if is_group_owner or is_group_admin or is_superuser(session.user.id):
            if status.available:
                if status.result == "开启":
                    if session.scene.id not in GROUP_LIST:
                        GROUP_LIST.append(int(session.scene.id))
                        save_group_list()
                        await birthday_info_switch.finish("已开启生日信息推送")
                    else:
                        await birthday_info_switch.finish("已开启生日信息推送")
                elif status.result == "关闭":
                    if session.scene.id in GROUP_LIST:
                        GROUP_LIST.remove(int(session.scene.id))
                        save_group_list()
                        await birthday_info_switch.finish("已关闭生日信息推送")
                    else:
                        await birthday_info_switch.finish("已关闭生日信息推送")
                else:
                    await birthday_info_switch.finish("无效的指令")
            else:
                await birthday_info_switch.finish("无效的指令")
        else:
            await birthday_info_switch.finish("无效的指令")
