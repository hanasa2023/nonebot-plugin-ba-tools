from pathlib import Path

from nonebot import get_driver, get_plugin_config, require
from pydantic import BaseModel

require("nonebot_plugin_localstore")

from nonebot_plugin_localstore import (
    get_plugin_cache_dir,
    get_plugin_data_dir,
)


class Config(BaseModel):
    """Plugin Config Here"""

    # 资源文件路径
    assert_path: Path = get_plugin_cache_dir() / "asserts"
    # 设置文件路径
    setting_path: Path = get_plugin_data_dir() / "setting"
    # llm 会话/配置文件
    llm_path: Path = get_plugin_data_dir() / "llm"
    # 图片加载通知开关
    loading_switch: bool = False
    # 单次最大获取的图片数量
    ba_max_pic_num: int = 10
    # pixiv图床反代
    pixiv_nginx: str = "https://i.pixiv.re"
    # 发送涩图时是否发送图片信息
    send_pic_info: bool = False
    # r18开关，防爆按钮
    r18_switch: bool = False
    # lmm chat开关
    chat_switch: bool = False
    # openai api key
    openai_api_key: str = ""
    # openai base url
    openai_base_url: str = ""
    # llm model
    llm_model: str = ""


plugin_config = get_plugin_config(Config)

DRIVER = get_driver()

config = DRIVER.config

SUPERUSERS: set[str] = config.superusers
