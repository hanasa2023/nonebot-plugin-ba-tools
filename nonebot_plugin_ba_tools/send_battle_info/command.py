from typing import Any

from nonebot import require
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent

from ..utils.user_info import (
    get_group_user_info,
    is_group_admin,
    is_group_owner,
    is_superuser,
)
from .utils.common import save_battle_config
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


@battle_info_switch.assign("status")
async def _(bot: Bot, event: GroupMessageEvent, status: Match[str]) -> None:
    service: BilibiliService = BilibiliService()
    await service.initialize()
    # 群主、管理员、SUPERUSER可以使用此命令
    user_info = await get_group_user_info(bot, event.user_id, event.group_id)
    if (
        is_group_owner(user_info)
        or is_group_admin(user_info)
        or is_superuser(event.user_id)
    ):
        if status.available:
            if status.result == "开启":
                if event.group_id not in service.battle_config.group_list:
                    service.battle_config.group_list.append(event.group_id)
                    await save_battle_config(service.battle_config)
                    await battle_info_switch.finish("已开启总力战/大决战推送")
                else:
                    await battle_info_switch.finish("已开启总力战/大决战推送")
            elif status.result == "关闭":
                if event.group_id in service.battle_config.group_list:
                    service.battle_config.group_list.remove(event.group_id)
                    await save_battle_config(service.battle_config)
                    await battle_info_switch.finish("已关闭总力战/大决战推送")
                else:
                    await battle_info_switch.finish("已关闭总力战/大决战推送")
            else:
                await battle_info_switch.finish("无效的指令")
    else:
        await battle_info_switch.finish("权限不足")
