from datetime import date

from arclet.alconna import Args
from nonebot.params import Depends
from nonebot_plugin_alconna import Alconna, Match, Subcommand, UniMessage, on_alconna

from nonebot_plugin_ba_tools.features.student.application.student_information_use_case import (
    StudentInformationUseCase,
)
from nonebot_plugin_ba_tools.features.student.dependency import (
    get_student_information_use_case,
)
from nonebot_plugin_ba_tools.features.student.domain.model import birthday

_birthday = Alconna(
    "ba学生生日",
    Subcommand(
        "生日表",
        Args["month?", str],
    ),
    Subcommand("热力图"),
)

birthday_matcher = on_alconna(
    _birthday,
    use_cmd_start=True,
)


@birthday_matcher.assign("生日表")
async def birthday_table_handler(
    month: Match[str],
    student_infomation_usecase: StudentInformationUseCase = Depends(
        get_student_information_use_case
    ),
) -> None:
    await birthday_matcher.send("正在生成生日表……")
    m = month.result if month.available else str(date.today().month)
    image_bytes = await student_infomation_usecase.generate_birthday_calendar(m)
    msg = UniMessage.image(raw=image_bytes)
    await birthday_matcher.send(msg)


@birthday_matcher.assign("热力图")
async def birthday_distribution_handler(
    student_infomation_usecase: StudentInformationUseCase = Depends(
        get_student_information_use_case
    ),
) -> None:
    await birthday_matcher.send("正在生成热力图……")
    msg = UniMessage.image(
        raw=await student_infomation_usecase.generate_birthday_heatmap()
    )
    await birthday_matcher.send(msg)
