from pathlib import Path

from nonebot import get_driver, get_plugin_config, require
from pydantic import BaseModel

require("nonebot_plugin_localstore")

from nonebot_plugin_localstore import (  # noqa: E402
    get_plugin_cache_dir,
    get_plugin_data_dir,
)


class Config(BaseModel):
    """Plugin Config Here"""

    # 资源文件路径
    assert_path: Path = get_plugin_cache_dir() / "asserts"
    # 设置文件路径
    setting_path: Path = get_plugin_data_dir() / "setting"
    # 图片加载通知开关
    loading_switch: bool = False


plugin_config = get_plugin_config(Config)

DRIVER = get_driver()

config = DRIVER.config

SUPERUSERS: set[str] = config.superusers
