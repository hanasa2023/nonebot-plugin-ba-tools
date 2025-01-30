from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import aiofiles
from httpx import AsyncClient
from nonebot import logger

from ..config import ASSERT_DIR, Config
from ..utils.types import Student, Students
from .constants import ARONA_CDN_URL


class DataLoadError(Exception):
    pass


class DataLoader:
    """数据加载器，如果指定路径的文件不存在，则通过网络下载"""

    def __init__(self, _path: str):
        self.file_path: Path = ASSERT_DIR / _path
        self.file_url: str = ARONA_CDN_URL + _path

    async def read(self) -> Any:
        logger.debug(f"尝试从文件中加载数据，文件路径：{self.file_path}")
        async with aiofiles.open(self.file_path, encoding="utf-8") as f:
            data = json.loads(await f.read())
        return data

    async def write(self, data):
        async with aiofiles.open(self.file_path, mode="w", encoding="utf-8") as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=4))

    async def download(self) -> Any:
        logger.debug(f"download url is {self.file_url}")
        async with AsyncClient() as client:
            response = await client.get(self.file_url)
            response.raise_for_status()
            data = response.json()
            return data

    async def load(self) -> Any:
        # 如果文件存在，则从文件中读取数据
        if self.file_path.exists():
            return await self.read()
        else:
            # 如果文件夹不存在，则创建文件夹
            folder = self.file_path.parent
            if not folder.exists():
                folder.mkdir(parents=True, exist_ok=True)
            # 从网络下载文件
            logger.debug(f"数据文件不存在，尝试通过网络下载，文件路径：{self.file_path}")
            data = await self.download()
            await self.write(data)
            return data


class StudentDataLoader(DataLoader):
    def __init__(self, _path: str):
        super().__init__(_path)

    async def load_students(self) -> list[Student]:
        data: Any | None = None
        try:
            data = await self.load()
            logger.debug(type(data))
            logger.debug(data)
        except Exception as e:
            logger.exception(e)
        finally:
            if isinstance(data, list):
                return Students(root=[Student(**item) for item in data]).root
            else:
                raise DataLoadError("Loaded data is not a list")
