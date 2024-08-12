from pathlib import Path
from typing import List

from nonebot import require
from pydantic import BaseModel

require("nonebot_plugin_localstore")

from nonebot_plugin_localstore import get_plugin_cache_dir  # noqa: E402


class Config(BaseModel):
    """Plugin Config Here"""

    # 资源文件路径
    assert_path: Path = get_plugin_cache_dir() / "asserts"
    # 订阅推送消息的群聊列表
    send_daily_info_group_list: List[str] = ["414151515"]
