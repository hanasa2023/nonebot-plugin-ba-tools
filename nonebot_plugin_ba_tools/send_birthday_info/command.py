import json
from typing import List

from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot

from ..config import plugin_config, DRIVER
from ..utils.constants import BIRTHDAY_INFO_GROUP_LIST_FILE
from ..utils.user_info import is_group_owner, is_group_admin, is_superuser, get_group_user_info

GROUP_LIST: List[int] = []

def save_group_list():
    full_path = plugin_config.setting_path / BIRTHDAY_INFO_GROUP_LIST_FILE
    if not plugin_config.setting_path.exists():
        plugin_config.setting_path.mkdir(parents=True, exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(GROUP_LIST, f, ensure_ascii=False, indent=4)


@DRIVER.on_startup
async def _():
    logger.debug("读取生日信息推送群列表")
    global GROUP_LIST
    full_path = plugin_config.setting_path / BIRTHDAY_INFO_GROUP_LIST_FILE
    if not full_path.exists():
        if not plugin_config.setting_path.exists():
            plugin_config.setting_path.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write('[]')
        return
    with open(full_path, 'r', encoding='utf-8') as f:
        GROUP_LIST = json.load(f)


# TODO: 添加命令别名
birthday_info_on = on_command("birthday_info_on")
@birthday_info_on.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    # 群主、管理员、SUPERUSER可以使用此命令
    user_info = await get_group_user_info(bot, event.user_id, event.group_id)
    if (
        not is_group_owner(user_info)
        and not is_group_admin(user_info)
        and not is_superuser(event.user_id)
    ):
        return await birthday_info_on.finish("权限不足")
    if event.group_id not in GROUP_LIST:
        GROUP_LIST.append(event.group_id)
        save_group_list()
        await birthday_info_on.finish("已开启生日信息推送")
    else:
        await birthday_info_on.finish("已开启生日信息推送")


birthday_info_off = on_command("birthday_info_off")
@birthday_info_off.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    # 群主、管理员、SUPERUSER可以使用此命令
    user_info = await get_group_user_info(bot, event.user_id, event.group_id)
    if (
        not is_group_owner(user_info)
        and not is_group_admin(user_info)
        and not is_superuser(event.user_id)
    ):
        return await birthday_info_on.finish("权限不足")
    if event.group_id in GROUP_LIST:
        GROUP_LIST.remove(event.group_id)
        save_group_list()
        await birthday_info_off.finish("已关闭生日信息推送")
    else:
        await birthday_info_off.finish("已关闭生日信息推送")
