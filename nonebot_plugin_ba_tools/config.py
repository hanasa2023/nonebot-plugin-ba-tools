from __future__ import annotations

from pathlib import Path
from shutil import copyfile
from typing import Literal

import yaml
from deepdiff.diff import DeepDiff
from nonebot import get_driver, logger, require
from nonebot.compat import model_dump, type_validate_python
from pydantic import BaseModel, Field

require("nonebot_plugin_localstore")
from nonebot_plugin_localstore import (
    get_plugin_cache_dir,
    get_plugin_config_dir,
    get_plugin_data_dir,
)

# 配置文件路径
CONFIG_DIR: Path = get_plugin_config_dir()
# 资源文件夹路径
ASSERT_DIR: Path = get_plugin_cache_dir() / "asserts"
# 设置文件夹路径
SETTING_DIR: Path = get_plugin_data_dir() / "setting"
# llm 会话/配置文件夹
LLM_DIR: Path = get_plugin_data_dir() / "llm"

config = get_driver().config
SUPERUSERS: set[str] = config.superusers

try:
    config_path: Path = Path(config.ba_tools_config_path)
except Exception:
    logger.info("未找到用户自定义配置文件路径，使用默认路径")
    config_path = CONFIG_DIR / "config.yaml"


if not config_path.exists():
    logger.info(f"配置文件不存在，正在创建默认配置文件至{config_path}, 请修改配置文件后重启")
    copyfile(Path(__file__).parent / "default_config.yaml", config_path)


class ChatModel(BaseModel):
    """聊天模型"""

    name: str
    base_url: str
    api_key: str


class PicConfig(BaseModel):
    """图片配置"""

    # 图片加载通知开关
    loading_switch: bool = Field(
        default=True,
        title="图片加载通知开关",
        description="是否开启图片加载通知",
    )
    # 单次最大获取的图片数量
    max_pic_num: int = Field(
        default=5,
        title="单次最大获取的图片数量",
        description="单次最大获取的图片数量",
    )
    # pixiv图床反代
    pixiv_nginx: str = Field(
        default="https://i.pixiv.re",
        title="pixiv图床反代",
        description="pixiv图床反代",
    )
    # 发送涩图时是否发送图片信息
    send_pic_info: bool = Field(
        default=True,
        title="发送涩图时是否发送图片信息",
        description="发送涩图时是否发送图片信息",
    )
    # r18开关，防爆按钮
    r18_switch: bool = Field(
        default=False,
        title="R18开关",
        description="是否开启R18",
    )


class ChatConfig(BaseModel):
    """聊天配置"""

    # lmm chat开关
    enable: bool = Field(
        default=False,
        title="LLM Chat开关",
        description="是否开启LLM Chat",
    )
    current_model: str = Field(
        default="",
        title="当前模型",
        description="当前模型",
    )
    # llm models
    models: list[ChatModel] = Field(
        default=[],
        title="LLM Model",
        description="LLM Model",
    )
    # 回复模式
    reply_mode: Literal["text", "image"] = Field(
        default="text",
        title="回复模式",
        description="回复模式",
    )


class WebUIConfig(BaseModel):
    """WebUI配置"""

    enable: bool = Field(
        default=True,
        title="启用 WebUI",
        description="是否启用 BA Tools WebUI",
    )

    path: str = Field(
        default="batools",
        title="WebUI 路径",
        description="WebUI 路径",
    )

    api_access_token: str = Field(
        default="",
        title="WebUI 访问令牌",
        description="WebUI 访问令牌",
    )

    username: str = Field(
        default="admin",
        title="WebUI 用户名",
        description="WebUI 用户名",
    )

    password: str = Field(
        default="admin",
        title="WebUI 密码",
        description="WebUI 密码",
    )


class Config(BaseModel):
    """插件配置"""

    # 图片配置
    pic: PicConfig = PicConfig()
    # 聊天配置
    chat: ChatConfig = ChatConfig()
    # WebUI配置
    webui: WebUIConfig = WebUIConfig()


class ConfigManager:
    _config: Config = Config()

    @classmethod
    def get(cls) -> Config:
        return cls._config

    @classmethod
    def set(cls, cfg: Config | None = None, show_diff: bool = True):
        cls._config = cfg or cls._config
        old_config = cls._load_config_file()
        if config_diff := DeepDiff(
            cls._config,
            old_config,
            ignore_order=True,
        ).get("values_changed", {}):
            if show_diff:
                for k, v in config_diff.items():
                    logger.info(f"{k}: {v['new_value']} -> {v['old_value']}")
            logger.info("配置文件已更新")
            config_path.write_text(
                yaml.safe_dump(
                    model_dump(
                        cls._config,
                    ),
                    indent=2,
                    allow_unicode=True,
                )
            )

    @classmethod
    def reset(cls):
        cls.set(
            type_validate_python(
                Config,
                yaml.safe_load(
                    (Path(__file__).parent / "default_config.yaml").read_text(encoding="utf-8"),
                ),
            )
        )

    @staticmethod
    def _load_config_file() -> Config:
        return type_validate_python(
            Config,
            yaml.safe_load(
                config_path.read_text(encoding="utf-8"),
            ),
        )


ConfigManager.set(ConfigManager._load_config_file(), show_diff=False)
