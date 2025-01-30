from __future__ import annotations

from pathlib import Path

import httpx
from nonebot import logger, require

from ..config import ASSERT_DIR, ConfigManager
from ..utils.constants import ARONA_API_URL, IMG_PATH_MAP

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import Image, UniMessage


async def get_img(name: str, type: str, middle_route: str = "strategy") -> UniMessage[Image] | None:
    """创建图片，若本地不存在，则从网站缓存到本地

    Args:
        name (str): search name
        type (str): img type
        middle_route (str): middle route

    Returns:
        UniMessage[Image] | None: 若获取到信息，则返回image消息否则返回None
    """
    url: str = f"{ARONA_API_URL}/api/{middle_route}/{name}"
    logger.debug(f"url: {url}")
    async with httpx.AsyncClient() as ctx:
        response: httpx.Response = await ctx.get(url)
        if response.status_code == 200:
            res_json = response.json()
            hash = res_json["data"]["hash"]
            if hash:
                img_path: Path = ASSERT_DIR / IMG_PATH_MAP[type] / f"{hash}.png"
                if not img_path.exists():
                    logger.debug(f"{type}图片不存在，正在从网络下载至{img_path}……")
                    # 若父文件夹不存在则创建文件夹
                    folder: Path = img_path.parent
                    if not folder.exists():
                        folder.mkdir(parents=True, exist_ok=True)
                    # 获取图片
                    async with httpx.AsyncClient() as ctx:
                        res: httpx.Response = await ctx.get(res_json["data"]["imgUrl"])
                        if res.status_code == 200:
                            with open(file=img_path, mode="wb") as f:
                                f.write(res.content)

                logger.debug(f"从{img_path}加载图片……")
                return UniMessage.image(path=img_path)
                # return UniMessage.image(url=res_json["data"]["imgUrl"])
    return None
