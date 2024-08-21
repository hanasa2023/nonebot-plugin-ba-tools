from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from httpx import AsyncClient
from nonebot import get_plugin_config, logger

from ..config import Config
from ..utils.types import Student, Students
from .constants import ASSERTS_URL

plugin_config = get_plugin_config(Config)


class DataLoadError(Exception):
    pass


class DataLoader:
    """数据加载器，如果指定路径的文件不存在，则通过网络下载"""

    def __init__(self, _path: str):
        self.file_path: Path = plugin_config.assert_path / _path
        self.file_url: str = ASSERTS_URL + _path

    def read(self) -> Any:
        logger.debug(f"尝试从文件中加载数据，文件路径：{self.file_path}")
        with open(self.file_path, mode="r", encoding="utf-8") as f:
            data = json.loads(f.read())
        return data

    def write(self, data):
        with open(self.file_path, mode="w", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))

    async def download(self) -> Any:
        async with AsyncClient() as client:
            response = await client.get(self.file_url)
            response.raise_for_status()
            data = response.json()
        return data

    async def load(self) -> Any:
        # 如果文件存在，则从文件中读取数据
        if self.file_path.exists():
            return self.read()
        else:
            # 如果文件夹不存在，则创建文件夹
            folder = self.file_path.parent
            if not folder.exists():
                folder.mkdir(parents=True, exist_ok=True)
            # 从网络下载文件
            logger.debug(
                f"数据文件不存在，尝试通过网络下载，文件路径：{self.file_path}"
            )
            data = await self.download()
            self.write(data)
            return data


class StudentDataLoader(DataLoader):
    def __init__(self, _path: str):
        super().__init__(_path)

    async def load_students(self) -> list[Student]:
        data: Any | None = None
        try:
            data = await self.load()
        except Exception as e:
            logger.exception(e)
        finally:
            return Students.model_validate(data).root
