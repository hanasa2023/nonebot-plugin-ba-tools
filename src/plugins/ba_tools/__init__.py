from pathlib import Path
from nonebot import get_plugin_config, load_plugins
from nonebot.plugin import PluginMetadata

from .config import Config
from .send_birthday_info import send_birthday_info


__version__ = "0.0.1"
__plugin_meta__ = PluginMetadata(
    name="ba-tools",
    description="BlueArchive的工具箱",
    usage="推送每日学生生日信息等",
    type="application",
    homepage="https://github.com/hanasa2023/ba-tools#readme",
    config=Config,
    supported_adapters={"~onebot.v11"},
    extra={
        "version": __version__,
        "authors": [
            "hanasa2023 <hanasakayui2022@gmail.com>",
            "TheresaKugua <2277044081@qq.com>",
        ],
    },
)

config = get_plugin_config(Config)
