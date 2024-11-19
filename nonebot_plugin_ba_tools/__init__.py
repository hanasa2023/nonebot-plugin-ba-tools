from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

from .config import Config
from .get_ba_activity_info import get_activity_info as get_activity_info
from .get_ba_better_student import get_better_student as get_better_student
from .get_ba_clairvoyance import get_clairvoyance as get_clairvoyance
from .get_ba_gear_line import get_rank1_charts as get_rank1_charts
from .get_ba_manga import get_manga as get_manga
from .get_ba_pics import get_pic as get_pic
from .get_ba_pics import upload_pic as upload_pic
from .get_ba_pics import get_meme as get_meme
from .get_ba_simple_appraise import get_simple_appraise as get_simple_appraise
from .get_ba_student_birthday import (
    get_student_birthday_list as get_student_birthday_list,
)
from .get_ba_walkthrough import get_walkthrough as get_walkthrough
from .send_battle_info import (
    battle_info_switch as battle_info_switch,
)
from .send_battle_info import (
    send_battle_info as send_battle_info,
)
from .send_birthday_info import (
    birthday_info_switch as birthday_info_switch,
)
from .send_birthday_info import (
    send_birthday_info as send_birthday_info,
)

__version__ = "0.4.0-beta"
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

config: Config = get_plugin_config(Config)
