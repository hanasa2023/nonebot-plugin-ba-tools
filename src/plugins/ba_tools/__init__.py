from pathlib import Path
from nonebot import get_plugin_config, load_plugins
from nonebot.plugin import PluginMetadata

from .config import Config
from .send_birthday_info import send_birthday_info


__version__ = "0.1.0"
__plugin_meta__ = PluginMetadata(
    name="ba-tools",
    description="BlueArchive的工具箱",
    usage="推送每日学生生日信息等",
    type="application",
    homepage="https://github.com/hanasa2023/ba-tools#readme",
    config=Config,
    supported_adapters={"~onebot.v11"},
    extra={"version": __version__, "author": "hanasa2023 <hanasakayui2022@gmail.com>"},
)

config = get_plugin_config(Config)

sub_plugins = load_plugins(str(Path(__file__).parent.joinpath("plugins").resolve()))
