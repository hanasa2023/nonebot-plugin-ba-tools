import json
from pathlib import Path

import aiofiles
from pydantic import BaseModel

from ...config import plugin_config
from ...utils.constants import BATTLE_INFO_CONFIG_FILE


class BattleConfig(BaseModel):
    group_list: list[int]
    last_dynamic_id: str


async def load_battle_config() -> BattleConfig:
    """获取配置文件信息

    Returns:
        BattleConfig: 配置文件提取出来的模型
    """
    full_path: Path = plugin_config.setting_path / BATTLE_INFO_CONFIG_FILE
    if not full_path.exists():
        if not plugin_config.setting_path.exists():
            plugin_config.setting_path.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(full_path, "w", encoding="utf-8") as f:
            await f.write(
                BattleConfig(group_list=[], last_dynamic_id="").model_dump_json(
                    indent=2
                )
            )
        return BattleConfig(group_list=[], last_dynamic_id="")
    async with aiofiles.open(full_path, "r", encoding="utf-8") as f:
        content = await f.read()
        return BattleConfig(**json.loads(content))


async def save_battle_config(battle_config: BattleConfig) -> None:
    """保存配置文件

    Args:
        battle_config (BattleConfig): 需要保存的模型
    """
    full_path: Path = plugin_config.setting_path / BATTLE_INFO_CONFIG_FILE
    if not plugin_config.setting_path.exists():
        plugin_config.setting_path.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(full_path, "w", encoding="utf-8") as f:
        await f.write(battle_config.model_dump_json(indent=2))
