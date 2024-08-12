from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

from .config import Config
from .send_birthday_info import send_birthday_info

__version__ = "0.1.7"
__plugin_meta__ = PluginMetadata(
    name="ba-tools",
    description="BlueArchive的工具箱",
    usage="推送每日学生生日信息等",
    type="application",
    homepage="https://github.com/hanasa2023/ba-tools#readme",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={
        "version": __version__,
        "authors": [
            "hanasa2023 <hanasakayui2022@gmail.com>",
            "TheresaKugua <2277044081@qq.com>",
            "kawaiior <703360843@qq.com>",
        ],
    },
)

config = get_plugin_config(Config)
