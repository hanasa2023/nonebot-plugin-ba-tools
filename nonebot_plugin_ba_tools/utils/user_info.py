from typing import Union, Dict

from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent

from ..config import SUPERUSERS


async def get_group_user_info(bot: Bot, user_id: int, group_id: int, no_cache: bool = False):
    try:
        user_info = await bot.get_group_member_info(user_id=user_id, group_id=group_id, no_cache=no_cache)
        return user_info
    except Exception as e:
        logger.exception(e)
    return {"card": "未知用户", "nickname": str(user_id), "role": "none"}


def is_group_owner(user_info: Dict) -> bool:
    return user_info.get("role") == "owner"


def is_group_admin(user_info: Dict) -> bool:
    return user_info.get("role") == "admin"


def is_superuser(user_id: Union[int, str]) -> bool:
    return user_id in SUPERUSERS
