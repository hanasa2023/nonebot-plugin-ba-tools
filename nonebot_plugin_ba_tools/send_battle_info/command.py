from typing import Any

from nonebot import require
from nonebot_plugin_uninfo import SceneType, Uninfo

from ..utils.user_info import is_superuser
from .utils.common import save_battle_config
from .utils.services import BilibiliService

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import (
    Alconna,
    AlconnaMatcher,
    Args,
    Match,
    on_alconna,
)

battle_info: Alconna[Any] = Alconna("ba总力战订阅", Args["status", str])
battle_info_switch: type[AlconnaMatcher] = on_alconna(battle_info, use_cmd_start=True)


@battle_info_switch.assign("status")
async def _(status: Match[str], session: Uninfo) -> None:
    if session.scene.type == SceneType.GROUP:
        service: BilibiliService = BilibiliService()
        await service.initialize()
        is_group_owner = session.member and session.member.role and session.member.role.id == "OWNER"
        is_group_admin = session.member and session.member.role and session.member.role.id == "ADMINISTRATOR"
        if is_group_owner or is_group_admin or is_superuser(session.user.id):
            if status.available:
                if status.result == "开启":
                    if session.scene.id not in service.battle_config.group_list:
                        service.battle_config.group_list.append(int(session.scene.id))
                        await save_battle_config(service.battle_config)
                        await battle_info_switch.finish("已开启总力战/大决战推送")
                    else:
                        await battle_info_switch.finish("已开启总力战/大决战推送")
                elif status.result == "关闭":
                    if session.scene.id in service.battle_config.group_list:
                        service.battle_config.group_list.remove(int(session.scene.id))
                        await save_battle_config(service.battle_config)
                        await battle_info_switch.finish("已关闭总力战/大决战推送")
                    else:
                        await battle_info_switch.finish("已关闭总力战/大决战推送")
                else:
                    await battle_info_switch.finish("无效的指令")
