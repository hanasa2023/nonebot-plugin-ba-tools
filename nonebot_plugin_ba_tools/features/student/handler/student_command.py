from datetime import date
from typing import Literal

from nonebot import logger
from nonebot.params import Depends
from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Field,
    Match,
    Subcommand,
    UniMessage,
    on_alconna,
)
from nonebot_plugin_uninfo import Uninfo

from nonebot_plugin_ba_tools.features.student.application import (
    StudentBirthdayUseCase,
    StudentDataSynchronizer,
    StudentInformationUseCase,
    StudentSubscriptionUseCase,
)
from nonebot_plugin_ba_tools.features.student.dependency import (
    get_student_birthday_use_case,
    get_student_data_synchronizer,
    get_student_information_use_case,
    get_student_subscription_use_case,
)

_student_cmd = Alconna(
    "ba学生",
    Subcommand(
        "信息",
        Args["name", str, Field(completion=lambda: "请输入学生姓名")],
    ),
    Subcommand(
        "生日",
        Subcommand(
            "日历",
            Args[
                "month",
                str,
                Field(completion=lambda: "请输入月份（如: 1、一月、01）"),
            ],
        ),
        Subcommand("热力图"),
    ),
    Subcommand(
        "生日订阅",
        Args[
            "status",
            Literal["开启", "关闭", "open", "close", "开", "关"],
            Field(completion=lambda: "请输入 开启/关闭"),
        ],
    ),
    Subcommand("更新"),
)

student_matcher = on_alconna(
    _student_cmd, use_cmd_start=True, comp_config={"lite": True}, skip_for_unmatch=False
)


@student_matcher.assign("信息")
async def handle_student_info(
    name: Match[str],
    use_case: StudentInformationUseCase = Depends(get_student_information_use_case),
) -> None:
    if not name.available:
        await student_matcher.finish("请输入要查询的学生姓名")

    await student_matcher.send("正在生成学生信息卡……")
    image_bytes = await use_case.generate_student_info_card(name.result)

    if image_bytes is None:
        await student_matcher.finish(f"未找到学生: {name.result}")

    msg = UniMessage.image(raw=image_bytes)
    await student_matcher.send(msg)


@student_matcher.assign("生日.日历")
async def handle_birthday_calendar(
    month: Match[str],
    use_case: StudentBirthdayUseCase = Depends(get_student_birthday_use_case),
) -> None:
    await student_matcher.send("正在生成生日表……")
    m = month.result if month.available else str(date.today().month)
    image_bytes = await use_case.generate_birthday_calendar(m)
    msg = UniMessage.image(raw=image_bytes)
    await student_matcher.send(msg)


@student_matcher.assign("生日.热力图")
async def handle_birthday_heatmap(
    use_case: StudentBirthdayUseCase = Depends(get_student_birthday_use_case),
) -> None:
    await student_matcher.send("正在生成热力图……")
    msg = UniMessage.image(raw=await use_case.generate_birthday_heatmap())
    await student_matcher.send(msg)


@student_matcher.assign("生日订阅")
async def handle_birthday_subscription(
    status: Match[str],
    session: Uninfo,
    subscription_use_case: StudentSubscriptionUseCase = Depends(
        get_student_subscription_use_case
    ),
) -> None:
    # 手动检查管理员权限
    scene = session.scene
    member = session.member

    is_admin = False
    if member and member.role:
        is_admin = member.role.level >= 4

    if not is_admin:
        await student_matcher.finish("权限不足，仅管理员可操作生日订阅")

    group_id = scene.id

    if status.result in ("开启", "open", "开"):
        _, message = await subscription_use_case.enable_birthday_subscription(group_id)
    elif status.result in ("关闭", "close", "关"):
        _, message = await subscription_use_case.disable_birthday_subscription(group_id)
    else:
        message = "参数错误，请使用: 开启/关闭/open/close/开/关"

    await student_matcher.finish(message)


@student_matcher.assign("更新")
async def handle_update_student_info(
    synchronizer: StudentDataSynchronizer = Depends(get_student_data_synchronizer),
) -> None:
    try:
        await student_matcher.send("正在从 SchaleDB 获取学生数据...")
        message = await synchronizer.synchronize()

    except Exception as e:
        error_msg = f"❌ 学生数据更新失败: {e!s}"
        logger.error(f"处理更新学生数据命令异常: {e}", exc_info=True)
        await student_matcher.finish(error_msg)

    await student_matcher.finish(message)
