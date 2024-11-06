from pathlib import Path

import httpx
from nonebot import logger, require

from ...config import plugin_config
from ...utils.constants import ASSERTS_CLAIRVOYANCE_IMG_PATH

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import Image, UniMessage  # noqa: E402


async def get_img(server: str) -> UniMessage[Image] | None:
    """创建千里眼图片，若本地不存在，则从wiki缓存到本地

    Args:
        server (str): 服务器名(国际服/国服)

    Returns:
        UniMessage[Image] | None: 若获取到千里眼信息，则返回image消息否则返回None
    """
    url: str = f"https://tutorial.arona.diyigemt.com/api/v2/image?name={server}未来视"
    async with httpx.AsyncClient() as ctx:
        response: httpx.Response = await ctx.get(url)
        if response.status_code == 200:
            res_json = response.json()
            hash = res_json["data"][0]["hash"]
            if hash:
                img_path: Path = (
                    plugin_config.assert_path
                    / ASSERTS_CLAIRVOYANCE_IMG_PATH
                    / f"{hash}.png"
                )
                if not img_path.exists():
                    logger.debug(f"千里眼图片不存在，正在从网络下载至{img_path}……")
                    # 若父文件夹不存在则创建文件夹
                    folder: Path = img_path.parent
                    if not folder.exists():
                        folder.mkdir(parents=True, exist_ok=True)
                    # 获取图片
                    async with httpx.AsyncClient() as ctx:
                        res: httpx.Response = await ctx.get(
                            f"https://arona.cdn.diyigemt.com/image/some/{server}未来视.png?{hash}"
                        )
                        if res.status_code == 200:
                            with open(file=img_path, mode="wb") as f:
                                f.write(res.content)

                logger.debug(f"从{img_path}加载图片……")
                return UniMessage.image(path=img_path)
    return None
