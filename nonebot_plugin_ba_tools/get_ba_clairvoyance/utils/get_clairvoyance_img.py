from multiprocessing.context import ProcessError
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from nonebot import require

from nonebot_plugin_ba_tools.utils.constants import ASSERTS_CLAIRVOYANCE_IMG_PATH

from ...config import plugin_config
from ...utils.common import get_data_from_html

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import Image, UniMessage  # noqa: E402


async def create_clairvoyance_img(url: str) -> UniMessage[Image]:
    """创建千里眼图片，若本地不存在，则从wiki缓存到本地

    Args:
        url (str): 千里眼的 wiki url

    Returns:
        UniMessage[Image]: image消息
    """
    text = await get_data_from_html(url)
    soup = BeautifulSoup(text, "html.parser")
    imgs = soup.select(".div-img > img")
    src = imgs[3].get("src") if len(imgs) >= 3 else imgs[0].get("src")
    if isinstance(src, str):
        img_path: Path = (
            plugin_config.assert_path
            / ASSERTS_CLAIRVOYANCE_IMG_PATH
            / f"{src.split('/')[-1]}.png"
        )
        if not img_path.exists():
            # 若父文件夹不存在则创建文件夹
            folder = img_path.parent
            if not folder.exists():
                folder.mkdir(parents=True, exist_ok=True)
            # 获取图片
            async with httpx.AsyncClient() as ctx:
                response: httpx.Response = await ctx.get(f"https:{src}")
                if response.status_code == 200:
                    with open(file=img_path, mode="wb") as f:
                        f.write(response.content)
        msg: UniMessage[Image] = UniMessage(Image(path=img_path))
        return msg
    else:
        raise ProcessError("获取图片失败")
