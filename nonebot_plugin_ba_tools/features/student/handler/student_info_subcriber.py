from nonebot import logger
from nonebot.params import Depends
from nonebot_plugin_alconna import Target, UniMessage
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_orm import get_session

from nonebot_plugin_ba_tools.features.student.application import (
    StudentInformationUseCase,
)
from nonebot_plugin_ba_tools.features.student.dependency import (
    get_student_information_use_case,
)
from nonebot_plugin_ba_tools.shared import get_subscribe_repository
from nonebot_plugin_ba_tools.shared.domain.model.subscription import (
    SubscriptionNotificationType,
)
from nonebot_plugin_ba_tools.shared.domain.repository.subscribe_repository import (
    SubscribeRepository,
)


# TODO: fix: 计划任务中拿不到依赖注入实例
@scheduler.scheduled_job("cron", hour=0, minute=0, id="send_birthday_info")
async def send_birthday_info(
    student_info_use_case: StudentInformationUseCase = Depends(
        get_student_information_use_case
    ),
    subscribe_repository: SubscribeRepository = Depends(get_subscribe_repository),
) -> None:
    """定时推送生日信息

    每天午夜（00:00）触发一次，检查当天有生日的学生，
    并向所有订阅了生日通知的群组推送信息。
    """
    try:
        logger.info("开始执行生日信息推送任务")

        # 获取当天过生日的学生
        students = await student_info_use_case.get_birthday_students_today()

        if not students:
            logger.debug("今天没有学生过生日")
            return

        # 获取订阅了生日通知的群组
        subscriptions = await subscribe_repository.get_subscribed_groups(
            SubscriptionNotificationType.BIRTHDAY
        )

        if not subscriptions:
            logger.debug("没有群组订阅了生日通知")
            return

        # 为每个过生日的学生推送消息
        for student in students:
            try:
                # 构建消息
                msg = (
                    UniMessage.text(
                        f"今天是{student.name}的生日哦，"
                        f"在学生值日的前提下，切换为非l2d的值日模式，"
                        f"可以听到特殊语音哦。"
                        f"让我们一起祝福{student.name}生日快乐吧!"
                    )
                    .emoji(id="144")
                    .image(
                        url=f"https://schaledb.com/images/student/l2d/{student.id}.webp"
                    )
                )

                # 推送给所有订阅的群组
                for subscription in subscriptions:
                    try:
                        await msg.send(Target(id=subscription.group_id))
                        logger.debug(
                            f"成功推送 {student.name} 的生日信息到群组 "
                            f"{subscription.group_id}"
                        )
                    except Exception as e:
                        logger.error(
                            f"推送生日信息到群组 {subscription.group_id} 失败: {e}",
                            exc_info=True,
                        )
                        continue

            except Exception as e:
                logger.error(
                    f"处理学生 {student.name} 的生日信息失败: {e}",
                    exc_info=True,
                )
                continue

        logger.info(f"生日信息推送任务完成，推送了 {len(students)} 名学生的生日信息")

    except Exception as e:
        logger.error(f"生日信息推送任务执行异常: {e}", exc_info=True)
