import re
from datetime import datetime

import httpx
from bs4 import BeautifulSoup, NavigableString, ResultSet, Tag
from nonebot import require

from ..config import plugin_config
from .common import get_data_from_html
from .constants import ACTIVITYT_HTML_PATH, BA_WIKI_URL, WIKI_BASE_URL

require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import get_new_page  # noqa: E402


async def get_wiki_url_from_title(title: str) -> str | None:
    """通过title属性查找bawiki上对应的网页链接

    Args:
        title (str): 对应的title名

    Returns:
        str | None: 对应title的url
    """
    async with httpx.AsyncClient() as ctx:
        response: httpx.Response = await ctx.get(BA_WIKI_URL)
        response.encoding = "utf-8"
        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
        tag: Tag | NavigableString | None = soup.find("a", {"title": title})
        if isinstance(tag, Tag):
            href: str | list[str] | None = tag.get("href")
            if isinstance(href, str):
                return WIKI_BASE_URL + href
            else:
                return None
        else:
            return None


async def get_activity_table(url: str, index: int):
    """从指定活动url获取相应活动的表格

    Args:
        url (str): 指定的活动url
        index (int): 指定的table索引

    Returns:
        Tag | None: Tag元素
    """
    if url:
        text: str = await get_data_from_html(url)
        soup: BeautifulSoup = BeautifulSoup(text, "html.parser")
        tags: ResultSet[Tag] = soup.find_all("table")
        if index < len(tags):
            return tags[index]
        else:
            return None


async def create_activity_html(tag: Tag):
    """从html元素创建一个html网页

    Args:
        tag (Tag): html元素数据
    """
    soup = BeautifulSoup("", "html.parser")
    # 创建head和body标签
    html5: Tag = soup.new_tag("html")
    head: Tag = soup.new_tag("head")
    body: Tag = soup.new_tag("body")
    body.attrs = {"style": "margin: 0px"}

    # 创建title标签并添加到head中
    title: Tag = soup.new_tag("title")
    title.string = "Sample HTML Document"
    head.append(title)

    body.append(tag)
    html5.append(head)
    html5.append(body)
    soup.append(html5)
    imgs: ResultSet[Tag] = soup.find_all("img")
    for img in imgs:
        src: str | list[str] | None = img.get("src")
        if isinstance(src, str):
            new_src: str = "https:" + src
            img["src"] = new_src
    html: str = soup.prettify()
    with open(
        plugin_config.assert_path / ACTIVITYT_HTML_PATH, "w", encoding="utf-8"
    ) as f:
        f.write(html)


def get_table_size(table: Tag) -> tuple[int, int]:
    """从table中获取table宽高

    Args:
        table (Tag): 获取的活动表数据

    Returns:
        tuple[int, int]: 该表的宽和高
    """
    width: float = 0.0
    height: float = 0.0
    style_width: str | list[str] | None = table.get("style")
    if isinstance(style_width, str):
        match_width: re.Match[str] | None = re.search(
            r"width\s*:\s*(\d+(\.\d+)?)px", style_width
        )
        if match_width:
            _w: str = match_width.group(1)
            width += float(_w)
    trs: ResultSet[Tag] = table.find_all("tr")
    for tr in trs:
        style_height: str | list[str] | None = tr.get("style")
        if isinstance(style_height, str):
            match_height: re.Match[str] | None = re.search(
                r"height\s*:\s*(\d+(\.\d+)?)px", style_height
            )
            if match_height:
                _h: str = match_height.group(1)
                height += float(_h)
    res: tuple[int, int] = (round(width), round(height))
    return res


async def create_activity_pic(url: str, base_year: int) -> bytes | None:
    """
    从指定网页创建活动图片

    Args:
        url(str): 指定的网页url
        base_year(int): 开服年份
    Returns:
        bytes | None: 图片数据
    """
    current_year: int = datetime.now().year
    table: Tag | None = await get_activity_table(url, current_year - base_year)
    if table:
        await create_activity_html(table)
        width, height = get_table_size(table)
        async with get_new_page(viewport={"width": width, "height": height}) as page:
            await page.goto(
                f"file://{plugin_config.assert_path / ACTIVITYT_HTML_PATH}",
                wait_until="networkidle",
            )
            return await page.screenshot(full_page=True)
    else:
        return None


async def get_walkthrough_img(url: str) -> list[str]:
    """从网页获取关卡攻略

    Args:
        url (int): 网页url
    Returns:
        list[str]: 关卡攻略url列表
    """
    imgs_url: list[str] = []
    text = await get_data_from_html(url)
    soup = BeautifulSoup(text, "html.parser")
    imgs: ResultSet[Tag] = soup.css.select(".div-img > img")
    for img in imgs:
        img_src = img.get("src")
        if isinstance(img_src, str):
            img_url = "https:" + img_src
            imgs_url.append(img_url)
    return imgs_url
