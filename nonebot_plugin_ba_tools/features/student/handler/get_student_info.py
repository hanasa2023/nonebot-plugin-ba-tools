from arclet.alconna import Args
from nonebot.params import Depends
from nonebot_plugin_alconna import Alconna, Match, UniMessage, on_alconna

from nonebot_plugin_ba_tools.features.student.application.student_information_use_case import (
    StudentInformationUseCase,
)
from nonebot_plugin_ba_tools.features.student.dependency import (
    get_student_information_use_case,
)

_student_info = Alconna("ba学生信息", Args["name", str])

student_info_matcher = on_alconna(_student_info, use_cmd_start=True)


@student_info_matcher.assign("name")
async def handle_student_info(
    name: Match[str],
    use_case: StudentInformationUseCase = Depends(get_student_information_use_case),
) -> None:
    if not name.available:
        await student_info_matcher.finish("请输入要查询的学生姓名")

    await student_info_matcher.send("正在生成学生信息卡……")
    image_bytes = await use_case.generate_student_info_card(name.result)

    if image_bytes is None:
        await student_info_matcher.finish(f"未找到学生: {name.result}")

    msg = UniMessage.image(raw=image_bytes)
    await student_info_matcher.send(msg)
