import asyncio
import time
import urllib.parse
from functools import reduce
from hashlib import md5

import httpx
from nonebot import logger
from pydantic import BaseModel

from .common import BattleConfig, load_battle_config, save_battle_config
from .reponse.dynamic_list import DynamicListResponse

BASE_URL = "https://api.bilibili.com"
mixinKeyEncTab: list[int] = [
    46,
    47,
    18,
    2,
    53,
    8,
    23,
    32,
    15,
    50,
    10,
    31,
    58,
    3,
    45,
    35,
    27,
    43,
    5,
    49,
    33,
    9,
    42,
    19,
    29,
    28,
    14,
    39,
    12,
    38,
    41,
    13,
    37,
    48,
    7,
    16,
    24,
    55,
    40,
    61,
    26,
    17,
    0,
    1,
    60,
    51,
    30,
    4,
    22,
    25,
    54,
    21,
    56,
    59,
    6,
    63,
    57,
    62,
    11,
    36,
    20,
    34,
    44,
    52,
]


class BilibiliServiceException(Exception):
    """Custom exception class for BilibiliService errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class DynamicInfo(BaseModel):
    desc: str
    draws_url: list[str]


class BilibiliService:
    """Bilibili的api接口服务"""

    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "initialized"):
            self.img_key: str = ""
            self.sub_key: str = ""
            self.cookie: str = ""
            self.battle_config: BattleConfig = BattleConfig(
                group_list=[], last_dynamic_id=""
            )
            self.initialized: bool = False

    async def initialize(self) -> None:
        async with self._lock:
            if not self.initialized:
                self.img_key, self.sub_key = await self.getWbiKeys()
                self.cookie = await self.get_cookie()
                self.battle_config = await load_battle_config()
                self.initialized = True

    def getMixinKey(self, orig: str) -> str:
        "对 imgKey 和 subKey 进行字符顺序打乱编码"
        return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, "")[:32]

    def encWbi(self, params: dict, img_key: str, sub_key: str) -> dict[str, str]:
        "为请求参数进行 wbi 签名"
        mixin_key = self.getMixinKey(img_key + sub_key)
        curr_time = round(time.time())
        params["wts"] = curr_time  # 添加 wts 字段
        params = dict(sorted(params.items()))  # 按照 key 重排参数
        # 过滤 value 中的 "!'()*" 字符
        params = {
            k: "".join(filter(lambda chr: chr not in "!'()*", str(v)))
            for k, v in params.items()
        }
        query = urllib.parse.urlencode(params)  # 序列化参数
        wbi_sign = md5((query + mixin_key).encode()).hexdigest()  # 计算 w_rid
        params["w_rid"] = wbi_sign
        return params

    async def getWbiKeys(self) -> tuple[str, str]:
        "获取最新的 img_key 和 sub_key"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Referer": "https://www.bilibili.com/",
        }
        async with httpx.AsyncClient() as ctx:
            resp: httpx.Response = await ctx.get(
                url="https://api.bilibili.com/x/web-interface/nav", headers=headers
            )
            resp.raise_for_status()
            json_content = resp.json()
            img_url: str = json_content["data"]["wbi_img"]["img_url"]
            sub_url: str = json_content["data"]["wbi_img"]["sub_url"]
            img_key: str = img_url.rsplit("/", 1)[1].split(".")[0]
            sub_key: str = sub_url.rsplit("/", 1)[1].split(".")[0]
            return img_key, sub_key

    async def get_cookie(self) -> str:
        """获取网页cookie

        Returns:
            str: cookie
        """
        async with httpx.AsyncClient() as ctx:
            response: httpx.Response = await ctx.get(
                url="https://www.bilibili.com/",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
                },
            )
            headers: httpx.Headers = response.headers
            return headers["set-cookie"]

    async def get_user_dynamic(self, uid: str) -> DynamicListResponse:
        """获取用户动态列表

        Args:
            uid (str): 用户uid

        Returns:
            DynamicListResponse: 动态列表的响应
        """
        logger.debug("Start to get user dynamic")
        async with httpx.AsyncClient() as ctx:
            params: dict[str, str] = {"host_mid": uid}
            signed_params: dict[str, str] = self.encWbi(
                params, self.img_key, self.sub_key
            )
            response: httpx.Response = await ctx.get(
                url=f"{BASE_URL}/x/polymer/web-dynamic/v1/feed/space",
                params=signed_params,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
                    "cookie": self.cookie,
                    "Referer": "https://www.bilibili.com/",
                },
            )

            if response.json()["code"] == -352:
                logger.info("风控校验失败")
                logger.info("尝试重新获取cookie")
                self.cookie = await self.get_cookie()

            dynamic_list: DynamicListResponse = DynamicListResponse(**response.json())
            return dynamic_list

    async def get_dynamic_info(self, data: DynamicListResponse) -> list[DynamicInfo]:
        """获取动态信息

        Args:
            data (DynamicListResponse): 动态列表数据

        Returns:
            list[DynamicInfo]: 动态列表信息列表
        """
        logger.debug("Start to get dynamic info")
        # 如果首次运行插件，则手动添加最后一条动态的id
        if self.battle_config.last_dynamic_id == "":
            self.battle_config.last_dynamic_id = data.data.items[-1].id_str
            logger.debug(f"init last_dynamic_id: {self.battle_config.last_dynamic_id}")
        logger.debug(f"last_dynamic_id is {self.battle_config.last_dynamic_id}")

        dynamic_info: list[DynamicInfo] = []
        # 过滤置顶信息
        current_last_dynamic_id: str = data.data.items[1].id_str
        logger.debug(f"items len is {len(data.data.items)}")
        for item in data.data.items:
            logger.debug(f"now at {item.id_str}")
            # 获取最后的动态id
            if self.battle_config.last_dynamic_id == item.id_str:
                self.battle_config.last_dynamic_id = current_last_dynamic_id
                await save_battle_config(self.battle_config)
                logger.debug(
                    f"In the last update dynamic: {self.battle_config.last_dynamic_id}"
                )
                break
            desc: str = item.modules.module_dynamic.desc.text
            draws_url: list[str] = []
            if (
                item.modules.module_dynamic.major
                and item.modules.module_dynamic.major.draw
            ):
                for item1 in item.modules.module_dynamic.major.draw.items:
                    draws_url.append(item1.src)

            dynamic_info.append(DynamicInfo(desc=desc, draws_url=draws_url))

        return dynamic_info
