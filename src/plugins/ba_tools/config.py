import os
from typing import List
from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""

    # 资源文件路径
    assert_path: str = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../asserts")
    )
    # 订阅推送消息的群聊列表
    send_daily_info_group_list: List[str] = ["414151515"]
