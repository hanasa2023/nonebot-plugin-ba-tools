import json
from pathlib import Path

from pydantic import BaseModel

from ...config import plugin_config
from ...utils.constants import BATTLE_INFO_CONFIG_FILE


class BattleConfig(BaseModel):
    group_list: list[int]
    last_dynamic_id: str


def load_battle_config() -> BattleConfig:
    """
    获取配置信息
    """
    full_path: Path = plugin_config.setting_path / BATTLE_INFO_CONFIG_FILE
    with open(full_path, "r", encoding="utf-8") as f:
        battle_config: BattleConfig = json.load(f)
        return battle_config


def save_battle_config(battle_config: BattleConfig) -> None:
    full_path: Path = plugin_config.setting_path / BATTLE_INFO_CONFIG_FILE
    if not plugin_config.setting_path.exists():
        plugin_config.setting_path.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(battle_config, f, ensure_ascii=False, indent=4)
