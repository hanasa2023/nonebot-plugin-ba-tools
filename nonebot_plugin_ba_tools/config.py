from typing import List
from pathlib import Path
from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""

    # 资源文件路径
    assert_path: Path = Path(__file__).resolve().parents[1] / "asserts"
    # 订阅推送消息的群聊列表
    send_daily_info_group_list: List[str] = ["414151515"]
