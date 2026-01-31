from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_orm")
require("nonebot_plugin_localstore")
require("nonebot_plugin_alconna")
require("nonebot_plugin_uninfo")

from .config import Config
from .config import ConfigManager as ConfigManager
from .features.student import (
    Students,
    birthday_matcher,
    birthday_subscriber,
    send_birthday_info,
    student_info_matcher,
    update_student_info_matcher,
)
from .shared import Subscriptions, get_subscribe_repository

__all__ = [
    "Students",
    "Subscriptions",
    "birthday_matcher",
    "birthday_subscriber",
    "get_subscribe_repository",
    "send_birthday_info",
    "student_info_matcher",
    "update_student_info_matcher",
]

__version__ = "0.5.9.post3"
__plugin_meta__ = PluginMetadata(
    name="ba-tools",
    description="BlueArchive的工具箱",
    usage="推送学生生日信息，获取千里眼……",
    type="application",
    homepage="https://github.com/hanasa2023/ba-tools#readme",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={
        "version": __version__,
        "authors": [
            "hanasa2023 <hanasakayui2022@gmail.com>",
            "kawaiior <kawaiiorv@gmail.com>",
        ],
    },
)
