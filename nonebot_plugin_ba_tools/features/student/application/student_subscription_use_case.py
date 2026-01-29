from nonebot import logger

from nonebot_plugin_ba_tools.shared.domain.model.subscription import (
    SubscriptionNotificationType,
)
from nonebot_plugin_ba_tools.shared.domain.repository.subscribe_repository import (
    SubscribeRepository,
)


class StudentSubscriptionUseCase:
    """学生订阅管理用例

    协调订阅仓库的交互，完成学生相关通知的订阅/取消订阅流程。
    """

    def __init__(self, subscribe_repository: SubscribeRepository) -> None:
        """初始化学生订阅用例

        Args:
            subscribe_repository: 订阅仓库（本地数据库）
        """
        self.subscribe_repository = subscribe_repository

    async def enable_birthday_subscription(self, group_id: str) -> tuple[bool, str]:
        """启用生日通知订阅

        Args:
            group_id: 群组ID

        Returns:
            tuple: (成功标志, 消息)
                - success: 是否操作成功
                - message: 描述性消息
        """
        try:
            # 获取已订阅的群组列表
            subscriptions = await self.subscribe_repository.get_subscribed_groups(
                SubscriptionNotificationType.BIRTHDAY
            )
            subscribed_group_ids = [sub.group_id for sub in subscriptions]

            # 检查是否已订阅
            if group_id in subscribed_group_ids:
                msg = "生日信息推送已开启"
                logger.info(f"群组 {group_id} 生日订阅已存在: {msg}")
                return False, msg

            # 添加订阅
            await self.subscribe_repository.add_subscribe(
                group_id=group_id,
                notification_type=SubscriptionNotificationType.BIRTHDAY,
            )
            msg = "已开启生日信息推送"
            logger.info(f"群组 {group_id} 生日订阅已启用")

        except Exception as e:
            error_msg = f"启用生日订阅失败: {e}"
            logger.error(error_msg, exc_info=True)
            return False, f"❌ 操作失败: {e}"
        return True, msg

    async def disable_birthday_subscription(self, group_id: str) -> tuple[bool, str]:
        """禁用生日通知订阅

        Args:
            group_id: 群组ID

        Returns:
            tuple: (成功标志, 消息)
                - success: 是否操作成功
                - message: 描述性消息
        """
        try:
            # 获取已订阅的群组列表
            subscriptions = await self.subscribe_repository.get_subscribed_groups(
                SubscriptionNotificationType.BIRTHDAY
            )
            subscribed_group_ids = [sub.group_id for sub in subscriptions]

            # 检查是否未订阅
            if group_id not in subscribed_group_ids:
                msg = "生日信息推送已是关闭状态"
                logger.info(f"群组 {group_id} 生日订阅不存在: {msg}")
                return False, msg

            # 移除订阅
            await self.subscribe_repository.remove_subscribe(
                group_id=group_id,
                notification_type=SubscriptionNotificationType.BIRTHDAY,
            )
            msg = "已关闭生日信息推送"
            logger.info(f"群组 {group_id} 生日订阅已禁用")

        except Exception as e:
            error_msg = f"禁用生日订阅失败: {e}"
            logger.error(error_msg, exc_info=True)
            return False, f"❌ 操作失败: {e}"
        return True, msg

    async def get_birthday_subscription_status(self, group_id: str) -> tuple[bool, str]:
        """获取生日通知订阅状态

        Args:
            group_id: 群组ID

        Returns:
            tuple: (是否已订阅, 状态描述)
                - subscribed: 群组是否已订阅生日通知
                - status: 描述性状态消息
        """
        try:
            subscriptions = await self.subscribe_repository.get_subscribed_groups(
                SubscriptionNotificationType.BIRTHDAY
            )
        except Exception as e:
            error_msg = f"获取订阅状态失败: {e}"
            logger.error(error_msg, exc_info=True)
            return False, f"❌ 查询失败: {e}"

        subscribed_group_ids = [sub.group_id for sub in subscriptions]

        is_subscribed = group_id in subscribed_group_ids
        status = "已开启" if is_subscribed else "已关闭"

        return is_subscribed, f"生日信息推送: {status}"
