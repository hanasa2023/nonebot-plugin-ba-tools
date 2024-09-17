from typing import Any

from nonebot import require

from .command import battle_info_switch  # noqa: F401
from .utils.reponse.dynamic_list import DynamicListResponse
from .utils.services import BilibiliService, DynamicInfo

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import Target, UniMessage  # noqa: E402

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler  # noqa: E402


@scheduler.scheduled_job("interval", seconds=10)
async def send_battle_info() -> None:
    # TODO:进一步完善功能
    service: BilibiliService = BilibiliService()
    await service.initialize()

    dynamic_list: DynamicListResponse = await service.get_user_dynamic("436037759")

    dynamic_infos: list[DynamicInfo] = await service.get_dynamic_info(dynamic_list)
    msg: UniMessage[Any] = UniMessage()
    for info in dynamic_infos:
        if "总力战" in info.desc or "大决战" in info.desc:
            msg.text(info.desc)
            for url in info.draws_url:
                msg.image(url=url)
            for group in service.battle_config.group_list:
                target: Target = Target(id=str(group))
                await msg.send(target=target)
