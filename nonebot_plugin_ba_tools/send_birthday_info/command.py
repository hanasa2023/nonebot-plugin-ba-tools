import json

from arclet.alconna import Alconna, Subcommand
from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot_plugin_alconna import Arparma, on_alconna

from ..config import DRIVER, plugin_config
from ..utils.constants import BIRTHDAY_INFO_GROUP_LIST_FILE
from ..utils.user_info import (
    get_group_user_info,
    is_group_admin,
    is_group_owner,
    is_superuser,
)

GROUP_LIST: list[int] = []


def save_group_list():
    full_path = plugin_config.setting_path / BIRTHDAY_INFO_GROUP_LIST_FILE
    if not plugin_config.setting_path.exists():
        plugin_config.setting_path.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(GROUP_LIST, f, ensure_ascii=False, indent=4)


@DRIVER.on_startup
async def _():
    logger.debug("读取生日信息推送群列表")
    global GROUP_LIST
    full_path = plugin_config.setting_path / BIRTHDAY_INFO_GROUP_LIST_FILE
    if not full_path.exists():
        if not plugin_config.setting_path.exists():
            plugin_config.setting_path.mkdir(parents=True, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write("[]")
        return
    with open(full_path, "r", encoding="utf-8") as f:
        GROUP_LIST = json.load(f)
        logger.debug(f"group list is: {GROUP_LIST}")


birthday_info = Alconna("ba_birthday_info", Subcommand("on"), Subcommand("off"))
birthday_info_switch = on_alconna(birthday_info, use_cmd_start=True)


# TODO: 添加命令别名
@birthday_info_switch.handle()
async def _(bot: Bot, event: GroupMessageEvent, result: Arparma):
    global GROUP_LIST
    # 群主、管理员、SUPERUSER可以使用此命令
    user_info = await get_group_user_info(bot, event.user_id, event.group_id)
    if (
        is_group_owner(user_info)
        or is_group_admin(user_info)
        or is_superuser(event.user_id)
    ):
        if result.find("on"):
            if event.group_id not in GROUP_LIST:
                GROUP_LIST.append(event.group_id)
                save_group_list()
                await birthday_info_switch.finish("已开启生日信息推送")
            else:
                await birthday_info_switch.finish("已开启生日信息推送")
        elif result.find("off"):
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
