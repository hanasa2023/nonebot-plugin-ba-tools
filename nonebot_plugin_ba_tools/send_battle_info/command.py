import json
from pathlib import Path
from typing import Any

from nonebot import logger, require
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent

from ..config import DRIVER, plugin_config
from ..utils.constants import BATTLE_INFO_CONFIG_FILE
from ..utils.user_info import (
    get_group_user_info,
    is_group_admin,
    is_group_owner,
    is_superuser,
)
from .utils.common import BattleConfig, save_battle_config
from .utils.services import BilibiliService

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import (  # noqa: E402
    Alconna,
    AlconnaMatcher,
    Args,
    Match,
    on_alconna,
)

battle_info: Alconna[Any] = Alconna("ba总力战订阅", Args["status", str])
battle_info_switch: type[AlconnaMatcher] = on_alconna(battle_info, use_cmd_start=True)

SERVICE: BilibiliService = BilibiliService()
BATTLE_CONFIG: BattleConfig


@DRIVER.on_startup
async def _() -> None:
    logger.debug("读取总力/大决战推送群列表")
    global BATTLE_CONFIG
    full_path: Path = plugin_config.setting_path / BATTLE_INFO_CONFIG_FILE
    if not full_path.exists():
        if not plugin_config.setting_path.exists():
            plugin_config.setting_path.mkdir(parents=True, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write("""{
                    "group_list": [],
                    "last_dynamic_id": ""
            }""")
        return
    global SERVICE
    await SERVICE.initialize()
    with open(full_path, "r", encoding="utf-8") as f:
        BATTLE_CONFIG = json.load(f)
        logger.debug(f"battle_info group list is: {BATTLE_CONFIG}")


@battle_info_switch.assign("status")
async def _(bot: Bot, event: GroupMessageEvent, status: Match[str]) -> None:
    global SERVICE
    # 群主、管理员、SUPERUSER可以使用此命令
    user_info = await get_group_user_info(bot, event.user_id, event.group_id)
    if (
        is_group_owner(user_info)
        or is_group_admin(user_info)
        or is_superuser(event.user_id)
    ):
        if status.available:
            if status.result == "开启":
                if event.group_id not in SERVICE.battle_config.group_list:
                    SERVICE.battle_config.group_list.append(event.group_id)
                    save_battle_config(SERVICE.battle_config)
                    await battle_info_switch.finish("已开启总力战/大决战推送")
                else:
                    await battle_info_switch.finish("已开启总力战/大决战推送")
            elif status.result == "关闭":
                if event.group_id in SERVICE.battle_config.group_list:
                    SERVICE.battle_config.group_list.remove(event.group_id)
                    save_battle_config(SERVICE.battle_config)
                    await battle_info_switch.finish("已关闭总力战/大决战推送")
                else:
                    await battle_info_switch.finish("已关闭总力战/大决战推送")
            else:
                await battle_info_switch.finish("无效的指令")
    else:
        await battle_info_switch.finish("权限不足")
