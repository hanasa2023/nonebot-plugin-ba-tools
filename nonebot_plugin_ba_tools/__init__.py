from nonebot.plugin import PluginMetadata, inherit_supported_adapters

from .config import Config
from .config import ConfigManager as ConfigManager
from .get_ba_activity_info import get_activity_info as get_activity_info
from .get_ba_better_student import get_better_student as get_better_student
from .get_ba_clairvoyance import get_clairvoyance as get_clairvoyance
from .get_ba_manga import get_manga as get_manga
from .get_ba_pics import get_meme as get_meme
from .get_ba_pics import get_pic as get_pic
from .get_ba_pics import upload_pic as upload_pic
from .get_ba_raid_line import calc_score as calc_score
from .get_ba_raid_line import calc_time as calc_time
from .get_ba_raid_line import get_boss_list as get_boss_list
from .get_ba_raid_line import get_member_charts as get_member_charts
from .get_ba_raid_line import get_rank1_charts as get_rank1_charts
from .get_ba_raid_line import get_score_charts as get_score_charts
from .get_ba_simple_appraise import get_simple_appraise as get_simple_appraise
from .get_ba_student_birthday import get_birthday_map as get_birthday_map
from .get_ba_student_birthday import (
    get_student_birthday_list as get_student_birthday_list,
)
from .get_ba_student_info import _get_skill_info as _get_skill_info
from .get_ba_student_info import _get_student_info as _get_student_info
from .get_ba_student_info import _get_student_list as _get_student_list
from .get_ba_walkthrough import get_walkthrough as get_walkthrough
from .get_ba_walkthrough import get_walkthrough_list as get_walkthrough_list
from .llm import chat as chat
from .llm import chat_commands as chat_commands
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
from .webui import app as app

__version__ = "0.5.5"
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
