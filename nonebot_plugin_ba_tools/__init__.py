from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config
from .get_activity_info import get_ba_activity_info  # noqa: F401
from .get_ba_clairvoyance import get_ba_clairvoyance  # noqa: F401
from .get_ba_manga import get_manga as get_manga
from .get_ba_walkthrough import get_walkthrough  # noqa: F401
from .get_student_birthday import get_student_birthday_list  # noqa: F401
from .send_battle_info import battle_info_switch, send_battle_info  # noqa: F401
from .send_birthday_info import birthday_info_switch, send_birthday_info  # noqa: F401

__version__ = "0.2.8"
__plugin_meta__ = PluginMetadata(
    name="ba-tools",
    description="BlueArchive的工具箱",
    usage="推送学生生日信息，获取千里眼……",
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
