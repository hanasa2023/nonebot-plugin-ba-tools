from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .ba_clairvoyance import get_ba_clairvoyance  # noqa: F401
from .config import Config
from .get_activity_info import get_ba_activity_info  # noqa: F401
from .send_birthday_info import birthday_info_switch, send_birthday_info  # noqa: F401

__version__ = "0.2.2"
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
            "kawaiior <kawaiiorv@gmail.com>",
        ],
    },
)

config: Config = get_plugin_config(Config)
