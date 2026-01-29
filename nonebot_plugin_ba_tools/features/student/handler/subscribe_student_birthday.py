from typing import Literal

from nonebot.params import Depends
from nonebot_plugin_alconna import (
    Alconna,
    AlconnaMatcher,
    Args,
    Match,
    on_alconna,
)
from nonebot_plugin_uninfo import ADMIN, Uninfo

from nonebot_plugin_ba_tools.features.student.application import (
    StudentSubscriptionUseCase,
)
from nonebot_plugin_ba_tools.features.student.dependency import (
    get_student_subscription_use_case,
)

_birthday_subscriber = Alconna(
    "ba学生生日订阅",
    Args["status", Literal["开启", "关闭", "open", "close", "开", "关"]],
)
birthday_subscriber: type[AlconnaMatcher] = on_alconna(
    _birthday_subscriber, use_cmd_start=True, permission=ADMIN()
)


@birthday_subscriber.handle()
async def _(
    status: Match[str],
    session: Uninfo,
    subscription_use_case: StudentSubscriptionUseCase = Depends(
        get_student_subscription_use_case
    ),
) -> None:
    group_id = session.scene.id

    if status.result in ("开启", "open", "开"):
        _, message = await subscription_use_case.enable_birthday_subscription(group_id)
    elif status.result in ("关闭", "close", "关"):
        _, message = await subscription_use_case.disable_birthday_subscription(group_id)
    else:
        message = "参数错误，请使用: 开启/关闭/open/close/开/关"

    await birthday_subscriber.finish(message)
