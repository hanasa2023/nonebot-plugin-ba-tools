import asyncio
import calendar
from datetime import datetime
from pathlib import Path

import httpx
from nonebot import logger
from PIL import Image, ImageDraw, ImageFont

from ...config import plugin_config
from ...utils.constants import (
    ASSERTS_URL,
    DATA_STUDENTS_BIRTHDAY_IMG_PATH,
    DATA_STUDENTS_ICON_PATH,
    MONTH_i18N,
)
from ...utils.types import Student


def handle_student_list(
    students: list[Student],
) -> tuple[list[Student], dict[str, int]]:
    """对学生列表进行去重并排序

    Args:
        students (list[Student]): 学生列表

    Returns:
        list[Student]: 处理后的学生列表
    """
    students_sorted: list[Student] = sorted(
        students, key=lambda student: student.birthday
    )
    students_handled: list[Student] = []
    counter: dict[str, int] = {}
    hash_map: dict[str, bool] = {}
    for student in students_sorted:
        if hash_map.get(student.personal_name) is None:
            hash_map[student.personal_name] = True
            students_handled.append(student)
            if counter.get(student.birthday) is None:
                counter[student.birthday] = 1
            else:
                counter[student.birthday] += 1
    return (students_handled, counter)


async def init_birthday_img(students: list[Student], month: str):
    """初始化生日表图像，若不存在，则绘制

    Args:
        students (list[Student]): 学生列表
        month (str): 需绘制的月份
    """
    students_handled, _ = handle_student_list(students)
    for student in students_handled:
        img_path: Path = Path(
            plugin_config.assert_path / f"{DATA_STUDENTS_ICON_PATH}/{student.id}.webp"
        )
        if not img_path.exists():
            await init_student_icon(
                ASSERTS_URL + f"{DATA_STUDENTS_ICON_PATH}/{student.id}.webp", img_path
            )
    birthday_img_path: Path = (
        plugin_config.assert_path / f"{DATA_STUDENTS_BIRTHDAY_IMG_PATH}/{month}.png"
    )
    if not birthday_img_path.exists():
        logger.info("检测到生日表不存在，正在开始创建……")
        await asyncio.to_thread(draw_birthday_img, month, birthday_img_path, students)
        logger.info("已成功创建生日表")
    else:
        logger.info("已存在生日表")


def find_first_birth_index(students_list: list[Student], target_birthday: str) -> int:
    """寻找学生列表中某一生日第一次出现的索引值

    Args:
        students_list (list[Student]): 需查询的学生列表
        target_birthday (str): 目标生日

    Returns:
        int: 索引值
    """
    for index, student in enumerate(students_list):
        if student.birthday == target_birthday:
            return index
    return -1  # 如果没有找到，返回 -1


def draw_birthday_img(month: str, save_path: Path, students: list[Student]):
    """绘制某月学生生日表

    Args:
        month (str): 月份
        save_path (str): 保存路径
    """
    students_handled, counter = handle_student_list(students)
    caption_h: int = 60
    table_w: int = 120
    table_h: int = 90
    img_w: int = table_w * 7
    img_h: int = caption_h + table_h * 5
    inline_img_p: int = 15
    inline_img_size: tuple[int, int] = (60, 60)
    inline_img_p2: int = 4
    inline_img_size2: tuple[int, int] = (
        (inline_img_size[0] - inline_img_p2) // 2,
        (inline_img_size[1] - inline_img_p2) // 2,
    )
    img: Image.Image = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    zh_font: ImageFont.FreeTypeFont = ImageFont.truetype(
        Path(__file__).parents[1] / "fonts/miaozi-meiweiti-2.ttf", 24
    )
    en_font: ImageFont.FreeTypeFont = ImageFont.truetype(
        Path(__file__).parents[1] / "fonts/ComicShannsMonoNerdFont-Regular.otf", 16
    )
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)
    # 绘制表头区域
    draw.rounded_rectangle([0, 0, img_w, img_h], radius=16, fill="#ffc0cb")
    # 绘制表体区域
    draw.rounded_rectangle(
        xy=[0, 0, img_w, caption_h],
        radius=16,
        fill="#fe8ea2",
        corners=(True, True, False, False),
    )
    # 绘制分割线
    for i in range(1, 7):
        draw.line(
            xy=[(i * table_w, caption_h), (i * table_w, img_h)], fill="#ffffff", width=1
        )
    for i in range(1, 5):
        draw.line(
            xy=[(0, i * table_h + caption_h), (img_w, i * table_h + caption_h)],
            fill="#ffffff",
            width=1,
        )
    # 绘制表名
    draw.text(
        xy=(img_w / 2, caption_h / 2),
        text=f"{MONTH_i18N[month]}月学生生日表",
        font=zh_font,
        anchor="mm",
        fill="#83f5eb",
    )
    # 绘制日期
    date: datetime = datetime.now()
    day_in_month: int = calendar.monthrange(date.year, date.month)[1]
    for i in range(1, day_in_month + 1):
        row: int = i // 7 if i % 7 != 0 else i // 7 - 1
        col: int = (i % 7) - 1 if i % 7 > 0 else 6
        draw.text(
            xy=(
                col * table_w + (table_w - inline_img_size[0] - inline_img_p) / 2,
                row * table_h + table_h / 2 + caption_h,
            ),
            text=str(i),
            font=en_font,
            anchor="mm",
        )
        for index, student in enumerate(students_handled):
            if student.birthday == f"{month}月{i}日":
                if counter[student.birthday] == 1:
                    with Image.open(
                        plugin_config.assert_path
                        / f"{DATA_STUDENTS_ICON_PATH}/{student.id}.webp"
                    ) as im:
                        img.paste(
                            im=im.resize(inline_img_size),
                            box=(
                                (col + 1) * table_w - inline_img_p - inline_img_size[0],
                                row * table_h + inline_img_p + caption_h,
                            ),
                        )
                # 偷个懒，目前最多2名学生同一天生日
                elif counter[student.birthday] == 2:
                    if index == find_first_birth_index(
                        students_handled, student.birthday
                    ):
                        with Image.open(
                            plugin_config.assert_path
                            / f"{DATA_STUDENTS_ICON_PATH}/{student.id}.webp"
                        ) as im:
                            img.paste(
                                im=im.resize(inline_img_size2),
                                box=(
                                    (col + 1) * table_w
                                    - inline_img_p
                                    - inline_img_size[0],
                                    row * table_h
                                    + inline_img_p
                                    + caption_h
                                    + (inline_img_size[1] - inline_img_size2[1]) // 2,
                                ),
                            )
                    else:
                        with Image.open(
                            plugin_config.assert_path
                            / f"{DATA_STUDENTS_ICON_PATH}/{student.id}.webp"
                        ) as im:
                            img.paste(
                                im=im.resize(inline_img_size2),
                                box=(
                                    (col + 1) * table_w
                                    - inline_img_p
                                    - inline_img_size2[0],
                                    row * table_h
                                    + inline_img_p
                                    + caption_h
                                    + (inline_img_size[1] - inline_img_size2[1]) // 2,
                                ),
                            )
    if not save_path.exists():
        save_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(
        save_path,
        "PNG",
    )


async def init_student_icon(url: str, path: Path):
    """初始化学生头像，若不存在，则从网络获取并保存到本地

    Args:
        url (str): 获取头像的url
        path (Path): 存储路径
    """
    if path.exists():
        logger.debug("该头像已存在")
        return
    logger.debug("该头像不存在，正在尝试从网络获取")
    folder: Path = path.parent
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
    async with httpx.AsyncClient() as ctx:
        response: httpx.Response = await ctx.get(url)
        if response.status_code == 200:
            logger.info("获取icon成功")
            with open(path, mode="wb") as f:
                f.write(response.content)
    logger.debug("获取成功")
