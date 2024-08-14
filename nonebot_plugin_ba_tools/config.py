from pathlib import Path
from typing import List, Set

from nonebot import require, get_plugin_config, get_driver
from pydantic import BaseModel

require("nonebot_plugin_localstore")

from nonebot_plugin_localstore import get_plugin_cache_dir, get_plugin_data_dir  # noqa: E402


class Config(BaseModel):
    """Plugin Config Here"""

    # 资源文件路径
    assert_path: Path = get_plugin_cache_dir() / "asserts"
    # 设置文件路径
    setting_path: Path = get_plugin_data_dir() / "setting"
    # 订阅推送消息的群聊列表
    send_daily_info_group_list: List[str] = []


plugin_config = get_plugin_config(Config)

DRIVER = get_driver()

config = DRIVER.config

SUPERUSERS: Set[str] = config.superusers
